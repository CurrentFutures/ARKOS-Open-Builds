// Tiles: a clip of the "Try a tile" lab moving through its states, frame by frame, piped to ffmpeg.
const {chromium} = require('playwright');
const {spawn} = require('child_process');
const path = require('path');
const FPS = 24;
// keyframes: [seconds, temp, days, light]
const K = [[0, 32, 6, 100], [2, 32, 6, 100], [4, 40, 6, 100], [5.5, 40, 6, 100], [7.5, 20, 6, 100], [9, 20, 6, 100], [10.5, 32, 6, 100],
           [12.5, 32, 14, 100], [14, 32, 14, 100], [15.5, 32, 6, 100], [17, 32, 6, 0], [18.5, 32, 6, 0], [20, 32, 6, 100], [21, 32, 6, 100]];
const ease = u => u < .5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2;
function at(t) { for (let i = 0; i < K.length - 1; i++) { const [a, ...va] = K[i], [b, ...vb] = K[i + 1]; if (t <= b) { const u = ease((t - a) / (b - a)); return va.map((v, j) => v + (vb[j] - v) * u); } } return K[K.length - 1].slice(1); }
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 1920, height: 1080}, deviceScaleFactor: 1});
  await p.route('**/*', r => { const u = r.request().url(); (u.startsWith('file:') || u.startsWith('data:')) ? r.continue() : r.abort(); });
  await p.goto('file://' + path.join(__dirname, 'cap-tiles.html')); await p.waitForTimeout(1000);
  await p.evaluate(() => { document.body.style.zoom = '1.55'; const h = document.getElementById('labh'); const box = h.closest('section') || h.parentElement.parentElement;
    const r = box.getBoundingClientRect(); window.scrollTo(0, window.scrollY + r.top + r.height / 2 - 1080 / 1.55 / 2 - 30); });
  await p.waitForTimeout(300);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-tag:v', 'avc1', '-movflags', '+faststart', path.join(__dirname, 'out', 'tiles-lab.mov')]);
  const done = new Promise(r => ff.on('close', r));
  const N = Math.round(K[K.length - 1][0] * FPS);
  for (let f = 0; f < N; f++) {
    const [t, d, l] = at(f / FPS);
    await p.evaluate(([t, d, l]) => { [['temp', t], ['days', d], ['light', l]].forEach(([id, v]) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('input', {bubbles: true})); }); }, [t, d, l]);
    ff.stdin.write(await p.screenshot({type: 'jpeg', quality: 94}));
  }
  ff.stdin.end(); await done; console.log('tiles-lab.mov', N, 'frames'); await b.close();
})();
