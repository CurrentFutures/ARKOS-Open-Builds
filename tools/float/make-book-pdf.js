// Prints the Float build book PDF from its print version (renders in place of the 3D model).
// usage, from tools/: node float/make-book-pdf.js
const {chromium} = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.join(__dirname, 'the-float-build-book-print.html')); await p.waitForTimeout(500);
  await p.pdf({path: path.join(__dirname, '..', '..', 'builds', 'the-float', 'the-float-build-book.pdf'), format: 'Letter', printBackground: true});
  await b.close(); console.log('the-float-build-book.pdf');
})();
