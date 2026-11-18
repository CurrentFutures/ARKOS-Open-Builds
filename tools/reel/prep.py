import os
# Makes capture copies of the three model pages: three.js inlined (offline), the GLTF exporter added,
# the camera exposed, and the 3D stage filling the whole window.
import re, sys
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
LIBS = ['build/three.min.js', 'examples/js/controls/OrbitControls.js', 'examples/js/environments/RoomEnvironment.js', 'examples/js/geometries/RoundedBoxGeometry.js']
CSS = ('<style>.stage{position:fixed!important;inset:0!important;width:100vw!important;height:100vh!important;max-width:none!important;'
       'aspect-ratio:auto!important;border:0!important;border-radius:0!important;z-index:9999!important;margin:0!important}'
       '.stage .hint,.stage .fail{display:none!important}body{overflow:hidden!important}</style>')
def lib(p): return '<script>\n' + open(SP + 'vendor/package/' + p).read().replace('</script', '<\\/script') + '\n</script>'
for name, src in (('float', 'house-pc-build-book.html'), ('lantern', 'lantern-unit.html'), ('sand', 'sand-object.html')):
    s = open(SP + src).read()
    for p in LIBS:
        tag = f'<script src="https://cdn.jsdelivr.net/npm/three@0.147.0/{p}"></script>'
        if tag in s: s = s.replace(tag, lib(p))
    assert 'cdn.jsdelivr' not in s, name
    s = s.replace('<script>\n(function(){', lib('examples/js/exporters/GLTFExporter.js') + '<script>\n(function(){', 1)
    assert 'GLTFExporter' in s, name
    s = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n?', '', s)
    assert s.count('loop();') == 1, name
    s = s.replace('loop();', 'window.__T={camera:camera,controls:controls,renderer:renderer,scene:scene};loop();')
    s = s.replace('</style>', '</style>' + CSS, 1)
    open(SP + f'reel/cap-{name}.html', 'w').write(s)
    print(name, len(s))
