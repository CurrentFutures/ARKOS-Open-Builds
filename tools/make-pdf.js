// Prints a guide page to PDF, the way the shipped guide PDFs were made.
// usage: node make-pdf.js <page.html> <out.pdf>   (needs Playwright with Chromium)
const {chromium} = require('playwright');
const path = require('path');
(async () => {
  const [src, out] = process.argv.slice(2);
  if (!src || !out) { console.log('usage: node make-pdf.js <page.html> <out.pdf>'); process.exit(1); }
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(src)); await p.waitForTimeout(1000);
  await p.pdf({path: out, format: 'Letter', margin: {top: '14mm', bottom: '14mm', left: '14mm', right: '14mm'}, printBackground: true});
  await b.close(); console.log(out);
})();
