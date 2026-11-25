# Checks the kitchen-table plate output (plate.py) without a sound card: a fake output records what would play.
import math, os, struct, sys, tempfile, time
SW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "builds", "the-sand-table", "software")
sys.path.insert(0, SW)
os.environ["SANDTABLE_PLATE"] = os.path.join(tempfile.mkdtemp(), "plate.json")
os.environ["SANDTABLE_OUTPUT"] = "audio"
os.environ["SANDTABLE_LISTEN"] = "127.0.0.1"
import plate

played = []
class FakeStream:
    def write(self, b): played.append(b)
    def stop(self): pass
    def close(self): pass
plate.stream = lambda s: FakeStream()

def samples(b): return struct.unpack("<%dh" % (len(b) // 2), b)
def purity(x, f):       # share of the signal's energy at the note itself (Goertzel)
    n = len(x); k = 2 * math.cos(2 * math.pi * f / plate.RATE); s1 = s2 = 0.0
    for v in x: s1, s2 = v + k * s1 - s2, s1
    p = (s1 * s1 + s2 * s2 - k * s1 * s2) * 2 / n
    return p / sum(v * v for v in x)

# no figure chosen yet: nothing plays rather than a guess
assert plate.verdict_clip(95) is None
plate.store(dict(plate.DEFAULTS, f0=312.0, max_drive=0.30))

crisp, smear = samples(plate.verdict_clip(95)), samples(plate.verdict_clip(30))
assert len(crisp) == int(4.2 * plate.RATE), len(crisp)
hold_c, hold_s = crisp[int(1 * plate.RATE):int(3.5 * plate.RATE)], smear[int(1 * plate.RATE):int(3.5 * plate.RATE)]
pc, ps = purity(hold_c, 312.0), purity(hold_s, 312.0)
print("energy at the note: settled %.2f, unsettled %.2f" % (pc, ps))
assert pc > 0.8 and ps < pc - 0.15, (pc, ps)
peak = max(abs(v) for v in hold_c)
assert 0.25 * 32767 < peak <= 0.30 * 32767 + 1, peak            # the ceiling holds
assert max(abs(v) for v in smear) <= 0.30 * 32767 + 1               # even fully noisy
worst = max(abs(v) for v in samples(plate.verdict_clip(0)))
assert worst <= 0.30 * 32767 + 1, worst
assert abs(crisp[0]) < 200 and max(abs(v) for v in crisp[-200:]) < 600   # rises from and falls to silence
print("ceiling: peak %.3f of full scale" % (peak / 32767))

# the meter, in audio mode, plays a verdict when a task ends; heartbeats and working signals make no sound
import meter
assert isinstance(meter.wire, plate.Plate) and meter.LISTEN_HOST == "127.0.0.1"
meter.LOG_PATH = os.path.join(tempfile.mkdtemp(), "log.csv")
meter.wire.send("H1"); meter.wire.send("W1"); meter.wire.send("T")
meter.tasks.decision(0.7, False); meter.tasks.end("answer")
for _ in range(100):
    if played: break
    time.sleep(0.1)
assert len(played) == 1 and len(played[0]) == 2 * int(4.2 * plate.RATE), [len(p) for p in played]
assert purity(samples(played[0])[plate.RATE:3 * plate.RATE], 312.0) < 0.75   # 30 settled: smeared
print("meter in audio mode: one verdict played, heartbeat ignored")

# the sweep covers 80-1200 Hz in about 14 minutes, like the controller
steps = math.log(plate.F_HI / plate.F_LO) / math.log(1.001)
print("sweep: %.1f minutes" % (steps * 0.3 / 60))
plate.write_wav(os.path.join(tempfile.mkdtemp(), "v.wav"), plate.verdict_clip(95))
print("OK")
