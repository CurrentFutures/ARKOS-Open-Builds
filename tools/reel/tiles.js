// Tiles: no 3D model exists; capture the mood board page as stills and a full-length image for a pan.
const {chromium} = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 1920, height: 1080}, deviceScaleFactor: 1});
  await p.route('**/*', r => { const u = r.request().url(); (u.startsWith('file:') || u.startsWith('data:')) ? r.continue() : r.abort(); });
  await p.goto('file://' + path.join(__dirname, 'cap-tiles.html')); await p.waitForTimeout(1500);
  await p.screenshot({path: path.join(__dirname, 'out', 'tiles-full.png'), fullPage: true});
  await p.screenshot({path: path.join(__dirname, 'out', 'tiles-still-top.png')});
  const lab = await p.$('#labh');
  if (lab) { await lab.scrollIntoViewIfNeeded(); await p.evaluate(() => window.scrollBy(0, -40)); await p.waitForTimeout(500); await p.screenshot({path: path.join(__dirname, 'out', 'tiles-still-try.png')}); }
  console.log('height', await p.evaluate(() => document.documentElement.scrollHeight));
  await b.close();
})();
