# Cuts the rendered shots into the teaser: depth-of-field on the macro shots, the four questions,
# a "Concept render" label, a vignette, the end card. Writes a silent cut and one with a single brass ring.
# usage: python3 compose.py   (after: node teaser.js render)
import os, subprocess, math, struct, wave
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__))
FR, OUT = os.path.join(HERE, 'frames'), os.path.join(HERE, 'out')
W, H, FPS = 1920, 1080, 24
os.makedirs(OUT, exist_ok=True)

def font(names, size):
    for n in names:
        for d in ('/usr/share/fonts/opentype/inter/', '/usr/share/fonts/truetype/jetbrains-mono/', '/Library/Fonts/', os.path.expanduser('~/Library/Fonts/'), ''):
            try: return ImageFont.truetype(d + n, size)
            except OSError: pass
    return ImageFont.load_default()
Q = font(['InterDisplay-Light.otf', 'Inter-Light.otf', 'Helvetica.ttc'], 58)
CARD = font(['InterDisplay-Regular.otf', 'Inter-Regular.otf', 'Helvetica.ttc'], 44)
MONO = font(['JetBrainsMono-Regular.ttf', 'Menlo.ttc'], 19)

# shot, seconds, question, depth of field (focus height as a fraction of the frame, sharp half-band, blur radius)
CUT = [('s1_sand', 3, None, (.5, .11, 9)),
       ('s2_flow', 3, 'How do we live well with technology?', None),
       ('s3_grow', 3, 'How do we design it?', None),
       ('s4_concrete', 3, 'How do we interact with it?', (.48, .2, 7)),
       ('s5_brass', 2, 'How do we trust it?', (.55, .24, 7)),
       ('s6_lantern', 2, None, None), ('s7_wall', 2, None, None), ('s8_table', 2, None, None)]
END_SEC = 4

def band_mask(cy, half):
    m = Image.new('L', (1, H))
    for y in range(H):
        d = max(0, abs(y / H - cy) - half) / .18
        m.putpixel((0, y), int(255 * min(1, d)))
    return m.resize((W, H))

vig = Image.new('L', (W, H))
vd = ImageDraw.Draw(vig)
for i in range(60):   # soft edge darkening
    t = i / 60; vd.ellipse([-W * .35 + t * W * .35, -H * .45 + t * H * .45, W * 1.35 - t * W * .35, H * 1.45 - t * H * .45], fill=int(255 * (1 - (1 - t) ** 2 * .55)))
vig = vig.filter(ImageFilter.GaussianBlur(40))

SCRIM = Image.new('L', (1, H))
for y in range(H): SCRIM.putpixel((0, y), int(255 * .62 * min(1, max(0, (y / H - .55) / .25))))
SCRIM = SCRIM.resize((W, H))

def text_layer(msg, alpha):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    if msg and alpha > 0:
        L.putalpha(SCRIM.point(lambda v: int(v * alpha))); d = ImageDraw.Draw(L)   # dark gradient behind the words
        w = d.textlength(msg, font=Q); x, y = (W - w) / 2, H * .78
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((x, y + 2), msg, font=Q, fill=(0, 0, 0, int(150 * alpha)))
        L = Image.alpha_composite(L, sh.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(L)
        d.text((x, y), msg, font=Q, fill=(246, 242, 234, int(255 * alpha)))
    d.text((W - 48 - d.textlength('CONCEPT RENDER', font=MONO), H - 52), 'CONCEPT RENDER', font=MONO, fill=(235, 230, 220, 120))
    return L

def frames():
  n = 0
  for shot, sec, q, dof in CUT:
      N = int(sec * FPS); mask = band_mask(*dof[:2]) if dof else None
      for i in range(N):
          im = Image.open(os.path.join(FR, shot, '%04d.jpg' % i)).convert('RGB')
          if dof: im = Image.composite(im.filter(ImageFilter.GaussianBlur(dof[2])), im, mask)
          im = ImageChops.multiply(im, Image.merge('RGB', [vig] * 3))
          if shot == 's5_brass':   # time passing: the light warms and dims across the shot
            u = i / (N - 1); im = ImageChops.multiply(im, Image.new('RGB', (W, H), (int(255 - 25 * u), int(255 - 60 * u), int(255 - 105 * u))))
          t = i / FPS; a = min(1, max(0, (t - .35) / .35), max(0, (sec - .15 - t) / .3)) if q else 0
          im = Image.alpha_composite(im.convert('RGBA'), text_layer(q, a)).convert('RGB')
          if n < 12: im = Image.blend(Image.new('RGB', (W, H)), im, n / 12)   # fade up from black
          yield im; n += 1
  # end card
  for i in range(END_SEC * FPS):
      t = i / FPS; a = min(1, t / .6, max(0, (END_SEC - t) / .6))
      im = Image.new('RGB', (W, H), (14, 15, 14)); d = ImageDraw.Draw(im)
      msg = 'ARKOS Lab  ·  Current Futures Group'; c = int(14 + (238 - 14) * a)
      d.text(((W - d.textlength(msg, font=CARD)) / 2, H / 2 - 30), msg, font=CARD, fill=(c, c - 3, c - 8))
      lab = 'CONCEPT RENDERS'; c2 = int(14 + (150 - 14) * a)
      d.text(((W - d.textlength(lab, font=MONO)) / 2, H / 2 + 40), lab, font=MONO, fill=(c2, c2, c2 - 6))
      yield im

def encode(path):
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-']
    cmd += ['-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p', '-tag:v', 'avc1', '-movflags', '+faststart', '-shortest', path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    import io
    for im in frames():
        b = io.BytesIO(); im.save(b, 'JPEG', quality=95); p.stdin.write(b.getvalue())
    p.stdin.close(); p.wait(); print(path)

# one brass ring under the end card: a struck plate, inharmonic partials decaying like a bell
SR, total = 48000, sum(c[1] for c in CUT) + END_SEC
ring_at = sum(c[1] for c in CUT) + .3
wav = os.path.join(OUT, 'brass-ring.wav')
with wave.open(wav, 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    data = bytearray()
    for k in range(int(SR * total)):
        t = k / SR - ring_at; v = 0
        if t >= 0:
            for f, a, d in ((233, .5, 3.2), (233 * 2.32, .2, 2.0), (233 * 4.25, .11, 1.2), (233 * 6.8, .05, .7)):
                v += a * math.sin(2 * math.pi * f * t) * math.exp(-t / d * 2.3) * min(1, t / .004)
        data += struct.pack('<h', int(max(-1, min(1, v * .55)) * 32767))
    w.writeframes(bytes(data))
silent = os.path.join(OUT, 'arkos-teaser.mov'); encode(silent)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', silent, '-i', wav, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest',
                '-movflags', '+faststart', os.path.join(OUT, 'arkos-teaser-with-ring.mov')], check=True)
print('with ring')
