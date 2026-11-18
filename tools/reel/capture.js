// Renders clips, stills and a GLB from a capture page, deterministically (virtual clock, one frame at a time).
// usage: node capture.js <build> [clip ...|stills|glb|test]
const {chromium} = require('playwright');
const {spawn} = require('child_process');
const fs = require('fs'), path = require('path');
const DIR = __dirname, OUT = path.join(DIR, 'out'); fs.mkdirSync(OUT, {recursive: true});
const W = 1920, H = 1080, FPS = 24;
const build = process.argv[2], want = process.argv.slice(3);

const btn = (k, v) => `.seg[data-k="${k}"] button[data-v="${v}"]`;
// Each clip: setup clicks, camera ('orbit' with turns, or a view button held), duration, and timed clicks.
const CLIPS = {
  float: {
    turntable: {setup: [btn('state', 'on')], cam: {orbit: 1}, sec: 10},
    states:    {setup: [btn('state', 'on'), btn('view', 'hero')], sec: 13, at: [[4, btn('state', 'sleep')], [8.5, btn('state', 'off')]]},
    glass:     {setup: [btn('state', 'on'), btn('view', 'hero')], sec: 10, at: [[3.5, btn('side', 'clear')], [7, btn('side', 'off')]]},
  },
  lantern: {
    turntable: {setup: ['#m-color'], cam: {orbit: 1}, sec: 10},
    modes:     {setup: ['#m-lamp', '#v-34'], sec: 15, at: [[3, '#m-evening'], [6, '#m-color'], [9, '#m-sleep'], [12, '#m-off']]},
    open:      {setup: ['#m-color', '#v-back'], sec: 14, at: [[2, '#o-drives'], [6.5, '#o-closed'], [7.5, '#o-xray'], [11, '#o-lift']]},
    top:       {setup: ['#m-color', '#v-top'], cam: {drift: .3}, sec: 8},
  },
  sand: {
    turntable: {setup: ['#runSure'], cam: {orbit: 1}, sec: 10, warm: 4},
    verdicts:  {setup: ['#v-top'], k: 1.05, sec: 16, at: [[1, '#runSure'], [6, '#runUnsure'], [11.5, '#runSure']]},
    open:      {setup: ['#o-xray'], cam: {orbit: .6}, sec: 10, at: [[7, '#o-lift']], warm: 2},
    gap:       {setup: ['#v-low', '#g-on'], k: 1.35, sec: 12, at: [[4, '#g-sleep'], [8.5, '#g-off']]},
  },
};
const DOLLY = {float: {_: 1.3, gap: 1, inside: 1.05}, lantern: {_: 1.12, top: 1.3}, sand: {_: 1.18, top: 1, back: 1.45, low: 1.35}};
const dolly = (p, k) => p.evaluate(k => { const T = window.__T, t = T.controls.target; T.camera.position.sub(t).multiplyScalar(k).add(t); }, k);
const STILLS = {float: ['hero', 'front', 'left', 'back', 'gap', 'inside'], lantern: ['q', 'front', 'right', 'back', 'top', 'low'], sand: ['q', 'top', 'front', 'low', 'back']};

(async () => {
  const b = await chromium.launch({args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist']});
  const ctx = await b.newContext({viewport: {width: W, height: H}, deviceScaleFactor: 1});
  await ctx.route('**/*', r => { const u = r.request().url(); (u.startsWith('file:') || u.startsWith('data:') || u.startsWith('blob:')) ? r.continue() : r.abort(); });
  await ctx.addInitScript(() => {
    let vt = 1000, q = [];
    performance.now = () => vt;
    window.requestAnimationFrame = cb => { q.push(cb); return q.length; };
    window.__step = ms => { vt += ms; const c = q; q = []; c.forEach(f => { try { f(vt); } catch (e) { console.error(e.message); } }); };
    try { window.matchMedia = (m => qq => { const r = m.call(window, qq); if (qq.includes('reduced-motion')) return Object.assign({}, r, {matches: false}); return r; })(window.matchMedia); } catch (e) {}
  });
  const errs = [];
  async function open() {
    const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
    await p.goto('file://' + path.join(DIR, `cap-${build}.html`)); await p.waitForTimeout(800);
    await p.evaluate(() => { const T = window.__T; T.controls.enableDamping = false; T.controls.autoRotate = false;
      T.controls.update = () => { T.camera.lookAt(T.controls.target); return false; }; window.__step(16); });
    await step(p, 10, 200);
    return p;
  }
  const step = (p, n, ms = 1000 / FPS) => p.evaluate(([n, ms]) => { for (let i = 0; i < n; i++) window.__step(ms); }, [n, ms]);
  const click = (p, sel) => p.evaluate(s => { const e = document.querySelector(s); if (!e) throw new Error('no ' + s); e.click(); }, sel);

  async function clip(name, c) {
    const p = await open();
    for (const s of c.setup || []) await click(p, s);
    await step(p, Math.round((c.warm || 2) * 5), 200);          // let tweens and verdicts settle
    await dolly(p, c.k || DOLLY[build]._);
    const base = await p.evaluate(() => { const T = window.__T, t = T.controls.target, d = T.camera.position.clone().sub(t);
      return {tx: t.x, ty: t.y, tz: t.z, r: Math.hypot(d.x, d.z), y: d.y, a: Math.atan2(d.z, d.x)}; });
    const file = path.join(OUT, `${build}-${name}.mov`);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-tag:v', 'avc1', '-movflags', '+faststart', file]);
    const done = new Promise(r => ff.on('close', r));
    const N = Math.round(c.sec * FPS), at = (c.at || []).map(([t, s]) => [Math.round(t * FPS), s]);
    const t0 = Date.now();
    for (let f = 0; f < N; f++) {
      for (const [af, s] of at) if (af === f) await click(p, s);
      if (c.cam) await p.evaluate(([base, cam, u]) => { const T = window.__T;
        const a = base.a + (cam.orbit ? cam.orbit * 2 * Math.PI * u : (cam.drift || 0) * (u - .5));
        T.camera.position.set(base.tx + base.r * Math.cos(a), base.ty + base.y, base.tz + base.r * Math.sin(a)); }, [base, c.cam, f / N]);
      await step(p, 1);
      ff.stdin.write(await p.screenshot({type: 'jpeg', quality: 94, timeout: 180000}));
    }
    ff.stdin.end(); await done; await p.close();
    console.log(`${build}-${name}.mov  ${N} frames  ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  }

  async function stills() {
    const p = await open();
    const views = STILLS[build];
    for (const v of views) {
      await click(p, btn('view', v)); await step(p, 10, 200); await dolly(p, DOLLY[build][v] || DOLLY[build]._); await step(p, 1);
      await p.screenshot({path: path.join(OUT, `${build}-still-${v}.png`), timeout: 180000});
    }
    await p.close(); console.log(`${build}: ${views.length} stills`);
  }

  async function glb() {
    const p = await open();
    const b64 = await p.evaluate(() => new Promise((res, rej) => {
      const T = window.__T, g = new THREE.Group(); g.name = 'build'; g.scale.setScalar(0.01); g.updateMatrix();   // model is in cm; glTF is metres
      const kids = T.scene.children.filter(o => !o.isLight && !(o.isMesh && o.geometry && o.geometry.type === 'PlaneGeometry' && o.geometry.parameters.width > 300));
      kids.forEach(o => g.add(o));
      new THREE.GLTFExporter().parse(g, buf => {
        kids.forEach(o => T.scene.add(o));
        const u = new Uint8Array(buf); let s = ''; for (let i = 0; i < u.length; i += 0x8000) s += String.fromCharCode.apply(null, u.subarray(i, i + 0x8000));
        res(btoa(s));
      }, e => rej(String(e)), {binary: true, onlyVisible: true, trs: true});
    }));
    fs.writeFileSync(path.join(OUT, `${build}.glb`), Buffer.from(b64, 'base64'));
    await p.close(); console.log(`${build}.glb`, (b64.length * .75 / 1e6).toFixed(1), 'MB');
  }

  if (want[0] === 'test') {
    const p = await open(); const t0 = Date.now();
    for (let i = 0; i < 5; i++) { await step(p, 1); await p.screenshot({type: 'jpeg', quality: 94, path: path.join(OUT, `test-${build}.jpg`)}); }
    console.log(build, 'ms/frame', (Date.now() - t0) / 5);
  } else {
    const todo = want.length ? want : ['stills', 'glb', ...Object.keys(CLIPS[build])];
    for (const n of todo) {
      if (n === 'stills') await stills(); else if (n === 'glb') await glb(); else await clip(n, CLIPS[build][n]);
    }
  }
  if (errs.length) console.log('page errors:', [...new Set(errs)].slice(0, 5));
  await b.close();
})();
