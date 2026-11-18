import os
# Capture copies for the teaser: libs inlined, scene exposed, plus page hooks for scripted states.
import re
SP=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
LIBS=['build/three.min.js','examples/js/controls/OrbitControls.js','examples/js/environments/RoomEnvironment.js','examples/js/geometries/RoundedBoxGeometry.js']
CSS=('<style>.stage{position:fixed!important;inset:0!important;width:100vw!important;height:100vh!important;max-width:none!important;'
     'aspect-ratio:auto!important;border:0!important;border-radius:0!important;z-index:9999!important;margin:0!important}'
     '.stage .hint,.stage .fail,.stage .badge{display:none!important}body{overflow:hidden!important}</style>')
def lib(p): return '<script>\n'+open(SP+'vendor/package/'+p).read().replace('</script','<\\/script')+'\n</script>'
HOOK={'sand':'window.__S={run:run,age:function(a){AGE=a;applyAge();},cover:cover};',
      'lantern':'','wall':''}
for name,src in (('sand','sand-object.html'),('lantern','lantern-unit.html'),('wall','living-light-wall.html')):
    s=open(SP+src).read()
    for p in LIBS:
        tag=f'<script src="https://cdn.jsdelivr.net/npm/three@0.147.0/{p}"></script>'
        if tag in s: s=s.replace(tag,lib(p))
    assert 'cdn.jsdelivr' not in s,name
    s=re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n?','',s)
    assert s.count('loop();')==1,name
    s=s.replace('loop();',HOOK[name]+'window.__T={camera:camera,controls:controls,renderer:renderer,scene:scene};loop();')
    s=s.replace('</style>','</style>'+CSS,1)
    open(SP+f'teaser/tz-{name}.html','w').write(s); print(name,len(s))
