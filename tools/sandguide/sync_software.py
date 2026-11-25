# Copies the software files in builds/the-sand-table/software into the model page's
# "Software" download (sand-export.js), so the download and the folder never differ.
# Run before patch_sand.py.
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SW_DIR = os.path.join(HERE, '..', '..', 'builds', 'the-sand-table', 'software')
JS = os.path.join(HERE, 'sand-export.js')
s = open(JS).read()
m = re.search(r'var SW=(\{.*?\});\n', s, re.S)
old = json.loads(m.group(1))
new = {k: open(os.path.join(SW_DIR, k.split('/', 1)[1])).read() for k in old}
s = s[:m.start(1)] + json.dumps(new) + s[m.end(1):]
open(JS, 'w').write(s)
print('updated:', [k.split('/', 1)[1] for k in old if old[k] != new[k]] or 'nothing')
