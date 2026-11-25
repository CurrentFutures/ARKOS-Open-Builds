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
new = {}
for root, dirs, files in os.walk(SW_DIR):           # every file in the folder, in a stable order
    dirs[:] = sorted(d for d in dirs if d != '__pycache__')
    for name in sorted(files):
        rel = os.path.relpath(os.path.join(root, name), SW_DIR).replace(os.sep, '/')
        new['sandtable-software/' + rel] = open(os.path.join(root, name)).read()
s = s[:m.start(1)] + json.dumps(new) + s[m.end(1):]
open(JS, 'w').write(s)
print('changed:', [k.split('/', 1)[1] for k in new if old.get(k) != new[k]] or 'nothing',
      'removed:', [k.split('/', 1)[1] for k in old if k not in new] or 'nothing')
