// ARKOS teaser: renders each storyboard shot as a JPEG frame sequence, deterministically (virtual clock).
// usage: node teaser.js test [shot...]   -> first and last frame of each shot into test/
//        node teaser.js render [shot...] -> frames/<shot>/0000.jpg ...
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
const DIR = __dirname, W = 1920, H = 1080, FPS = 24;
const [mode, ...only] = process.argv.slice(2);

// cam: from/to as [position, target]; or view (a button id) plus k (dolly factors from->to) and spin (radians over the shot)
// pre: seconds of page time before frame 0. setup/at: code run in the page.
const SHOTS = {
  s1_sand:  {page: 'sand', sec: 3, fov: 24, setup: `document.getElementById('l-rake').click();document.getElementById('gv-hide').click();__S.age(0);`,
             pre: 0.8, preAt: `__S.run(94);`,
             cam: {from: [[15, 31, 19], [-1, 25.6, -1]], to: [[10.5, 29.4, 13.5], [-1, 25.6, -1]]}},
  s2_flow:  {page: 'wall', sec: 3, fov: 26, setup: ``,
             cam: {from: [[10, 153, 62], [0, 150, 0]], to: [[6, 151.5, 47], [0, 150, 0]]}},
  s3_grow:  {page: 'wall', sec: 3, fov: 26, setup: ``,
             cam: {from: [[-30, 192, 92], [-16, 182, 0]], to: [[-25, 189, 74], [-16, 182, 0]]}},
  s4_concrete: {page: 'sand', sec: 3, fov: 22, setup: `document.getElementById('l-rake').click();document.getElementById('gv-hide').click();__S.run(94);`, pre: 4,
             cam: {from: [[52, 13, 46], [29, 10, 30]], to: [[47, 12, 41], [29, 10, 30]]}},
  s5_brass: {page: 'sand', sec: 2, fov: 20, setup: `document.getElementById('l-rake').click();__S.run(94);__S.age(0);`, pre: 4,
             cam: {from: [[38, 24, 44], [24, 21, 24]], to: [[35, 23.5, 40], [24, 21, 24]]},
             each: `__S.age(Math.min(1,Math.max(0,(u-.1)/.8))*1)`},
  s6_lantern: {page: 'lantern', sec: 2, setup: `document.getElementById('m-evening').click();document.getElementById('v-34').click();`,
             cam: {view: true, k: [.98, .9], spin: .1}},
  s7_wall:  {page: 'wall', sec: 2, setup: ``,
             cam: {from: [[110, 160, 250], [0, 140, 0]], to: [[80, 158, 235], [0, 140, 0]]}},
  s8_table: {page: 'sand', sec: 2, setup: `document.getElementById('l-rake').click();document.getElementById('v-q').click();__S.run(94);`, pre: 4,
             cam: {view: true, k: [.82, .75], spin: -.1}},
};

(async () => {
  const b = await chromium.launch({args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist']});
  const ctx = await b.newContext({viewport: {width: W, height: H}, deviceScaleFactor: 1});
  await ctx.route('**/*', r => { const u = r.request().url(); (u.startsWith('file:') || u.startsWith('data:') || u.startsWith('blob:')) ? r.continue() : r.abort(); });
  await ctx.addInitScript(() => {
    let vt = 1000, q = [];
    performance.now = () => vt;
    window.requestAnimationFrame = cb => { q.push(cb); return q.length; };
    window.__step = ms => { vt += ms; const c = q; q = []; c.forEach(f => { try { f(vt); } catch (e) { console.error(e.message); } }); };
    window.AudioContext = undefined; window.webkitAudioContext = undefined;
    try { window.matchMedia = (m => qq => { const r = m.call(window, qq); if (qq.includes('reduced-motion')) return Object.assign({}, r, {matches: false}); return r; })(window.matchMedia); } catch (e) {}
  });
  const errs = [];
  const step = (p, n, ms = 1000 / FPS) => p.evaluate(([n, ms]) => { for (let i = 0; i < n; i++) window.__step(ms); }, [n, ms]);

  async function shot(name, s, frames) {
    const p = await ctx.newPage(); p.on('pageerror', e => errs.push(name + ': ' + e.message));
    await p.goto('file://' + path.join(DIR, `tz-${s.page}.html`)); await p.waitForTimeout(800);
    await p.evaluate(() => { const T = window.__T; T.controls.enableDamping = false; T.controls.autoRotate = false;
      T.controls.update = () => { T.camera.lookAt(T.controls.target); return false; }; window.__step(16); });
    await p.evaluate(c => eval(c), s.setup || '');
    await step(p, 12, 200);                                     // view tweens and states settle
    if (s.preAt) await p.evaluate(c => eval(c), s.preAt);
    if (s.pre) await step(p, Math.round(s.pre * FPS));
    const base = await p.evaluate(fov => { const T = window.__T; if (fov) { T.camera.fov = fov; T.camera.updateProjectionMatrix(); }
      const t = T.controls.target, c = T.camera.position; return {p: [c.x, c.y, c.z], t: [t.x, t.y, t.z]}; }, s.fov || 0);
    const N = Math.round(s.sec * FPS), list = frames || [...Array(N).keys()];
    const out = mode === 'test' ? path.join(DIR, process.env.TESTDIR || 'test') : path.join(DIR, 'frames', name); fs.mkdirSync(out, {recursive: true});
    let f = 0;
    for (const target of list) {
      while (f < target) { await step(p, 1); f++; }
      await p.evaluate(([s, base, u]) => {
        const T = window.__T, e = u < .5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2, c = s.cam;
        let P, Tg;
        if (c.view) {
          const k = c.k[0] + (c.k[1] - c.k[0]) * e, a = (c.spin || 0) * (e - .5);
          const d = base.p.map((v, i) => (v - base.t[i]) * k), ca = Math.cos(a), sa = Math.sin(a);
          P = [base.t[0] + d[0] * ca - d[2] * sa, base.t[1] + d[1], base.t[2] + d[0] * sa + d[2] * ca]; Tg = base.t;
        } else { P = c.from[0].map((v, i) => v + (c.to[0][i] - v) * e); Tg = c.from[1].map((v, i) => v + (c.to[1][i] - v) * e); }
        T.camera.position.set(...P); T.controls.target.set(...Tg); T.camera.lookAt(T.controls.target);
        if (s.each) eval(s.each);
      }, [s, base, N > 1 ? f / (N - 1) : 0]);
      await step(p, 1); f++;
      const file = mode === 'test' ? path.join(out, `${name}-${target}.jpg`) : path.join(out, String(target).padStart(4, '0') + '.jpg');
      await p.screenshot({path: file, type: 'jpeg', quality: 95, timeout: 180000});
    }
    await p.close(); console.log(name, list.length, 'frames');
  }

  const names = only.length ? only : Object.keys(SHOTS);
  for (const n of names) {
    const s = SHOTS[n], N = Math.round(s.sec * FPS);
    await shot(n, s, mode === 'test' ? [0, Math.floor(N / 2), N - 1] : null);
  }
  if (errs.length) console.log('page errors:', [...new Set(errs)].slice(0, 8));
  await b.close();
})();
