#!/usr/bin/env python3
"""
The Sand Table plate, played straight from the computer.

For the kitchen-table version (Tier 1), which has no controller: the meter plays each verdict
through a USB sound adapter into the amplifier and the driver. It makes the same sound as
the controller's firmware: the household's one note, with noise and a slight wander mixed
in when the agent was unsettled, 0.4 s up, 3.5 s hold, 0.3 s down.

Use a USB sound adapter for the plate and nothing else, so notifications, videos and other
programs never shake the sand. Set that adapter's own volume to 100% once; the ceiling is
max_drive here and the amplifier's gain knob.

Setup, by hand (python3 plate.py <command>):
  devices            list sound outputs
  use <name>         play the plate through the output whose name contains <name>
  sweep              slowly play every note from 80 to 1200 Hz (about 14 minutes).
                     Press Enter when you see a figure you like: it searches just around it.
                     Press Enter again at the crispest moment: that is your figure.
  f <hz>             hold one note until you press Enter
  save <hz>          make <hz> your figure
  drive <0-1>        loudness ceiling, as a fraction of full scale (start at 0.30)
  test <0-100>       play a verdict: 95 settled, 30 unsettled
  wav <0-100> <file> write a verdict to a WAV file instead of playing it
  show               print the settings

Needs: Python 3.9+, and sounddevice (python3 -m pip install sounddevice; on Linux also
sudo apt install libportaudio2). Writing WAV files needs nothing extra.
"""
import json, math, os, queue, sys, threading, wave

RATE = 32000
F_LO, F_HI = 80.0, 1200.0
SETTINGS = os.path.expanduser(os.environ.get("SANDTABLE_PLATE", "~/.sandtable-plate.json"))
DEFAULTS = {"device": None, "f0": 0.0, "max_drive": 0.30}


def load():
    s = dict(DEFAULTS)
    try:
        with open(SETTINGS) as f:
            s.update(json.load(f))
    except (OSError, ValueError):
        pass
    return s


def store(s):
    with open(SETTINGS, "w") as f:
        json.dump(s, f, indent=1)


class Voice:
    """The firmware's audio core: one note, with softened noise and a slow wander for unsettled."""
    def __init__(self, max_drive):
        self.max_drive, self.phase, self.lp, self.wander, self.n = max_drive, 0.0, 0.0, 0.0, 0
        self.rng = 2463534242

    def noise(self):                          # the same xorshift as the controller
        r = self.rng
        r ^= (r << 13) & 0xFFFFFFFF; r ^= r >> 17; r ^= (r << 5) & 0xFFFFFFFF
        self.rng = r
        return (r - (1 << 32) if r >= 1 << 31 else r) / 2147483648.0

    def render(self, seconds, freq, unsettled, level):
        """level: a number, or a function of time in seconds. Returns 16-bit mono samples."""
        out = bytearray()
        for i in range(int(seconds * RATE)):
            lvl = level(i / RATE) if callable(level) else level
            self.n += 1
            if self.n >= 256:
                self.n = 0
                self.wander = (self.wander + 0.08 * self.noise()) * 0.98
            fe = freq * (1.0 + unsettled * 0.012 * self.wander)
            self.phase = (self.phase + fe / RATE) % 1.0
            s = math.sin(2 * math.pi * self.phase)
            self.lp += 0.15 * (self.noise() - self.lp)
            v = lvl * self.max_drive * ((1.0 - 0.6 * unsettled) * s + 0.6 * unsettled * self.lp * 2.0)
            v = max(-self.max_drive, min(self.max_drive, v))   # a real ceiling: noise peaks are clipped
            out += int(v * 32767).to_bytes(2, "little", signed=True)
        return bytes(out)


def envelope(t):                              # 0.4 s up, 3.5 s hold, 0.3 s down
    if t < 0.4:
        return t / 0.4
    if t < 3.9:
        return 1.0
    return max(0.0, 1.0 - (t - 3.9) / 0.3)


def verdict_clip(settled, s=None):
    s = s or load()
    if s["f0"] <= 0:
        return None                           # no figure chosen yet: do nothing rather than guess
    u = min(1.0, max(0.0, (100 - settled) / 100.0))
    return Voice(s["max_drive"]).render(4.2, s["f0"], u, envelope)


def write_wav(path, samples):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(samples)


def stream(s):
    import sounddevice as sd
    st = sd.RawOutputStream(samplerate=RATE, channels=1, dtype="int16", device=s["device"])
    st.start()
    return st


class Plate:
    """Stands in for the one-way wire in meter.py: verdicts play, everything else is ignored."""
    def __init__(self):
        self.q = queue.Queue(maxsize=4)
        threading.Thread(target=self._run, daemon=True).start()

    def send(self, line):
        if line.startswith("V"):
            try:
                self.q.put_nowait(int(line[1:]))
            except (ValueError, queue.Full):
                pass

    def _run(self):
        while True:
            settled = self.q.get()
            try:
                s = load()
                clip = verdict_clip(settled, s)
                if clip:
                    st = stream(s); st.write(clip); st.stop(); st.close()
            except Exception as e:            # no adapter plugged in: keep the meter running
                print("plate:", e, file=sys.stderr)


def wait_enter():
    flag = threading.Event()
    threading.Thread(target=lambda: (sys.stdin.readline(), flag.set()), daemon=True).start()
    return flag


def sweep(s):
    v, st = Voice(s["max_drive"]), stream(s)
    print("Sweeping 80 to 1200 Hz. Press Enter when you see a figure you like (Ctrl-C to stop).")
    f, pressed = F_LO, wait_enter()
    while f <= F_HI and not pressed.is_set():
        st.write(v.render(0.3, f, 0.0, 0.7)); f *= 1.001
    if not pressed.is_set():
        print("Sweep finished without a choice."); return
    center = f; f = center * 0.985
    print("Searching around %.1f Hz. Press Enter at the crispest moment." % center)
    pressed = wait_enter()
    while not pressed.is_set():
        st.write(v.render(1.5, f, 0.0, 0.7)); f *= 1.0005
        if f > center * 1.015:
            f = center * 0.985
    s["f0"] = round(f, 2); store(s); st.stop(); st.close()
    print("Saved: your figure is %.2f Hz. Playing a settled verdict." % s["f0"])
    st = stream(s); st.write(verdict_clip(100, s)); st.stop()


def main(a):
    s = load()
    cmd = a[0] if a else "show"
    if cmd == "devices":
        import sounddevice as sd
        print(sd.query_devices())
    elif cmd == "use":
        s["device"] = " ".join(a[1:]); store(s); print("plate output:", s["device"])
    elif cmd == "sweep":
        sweep(s)
    elif cmd == "f":
        v, st, pressed = Voice(s["max_drive"]), stream(s), wait_enter()
        print("Holding %s Hz. Press Enter to stop." % a[1])
        while not pressed.is_set():
            st.write(v.render(0.5, float(a[1]), 0.0, 0.7))
    elif cmd == "save":
        s["f0"] = float(a[1]); store(s); print("saved")
    elif cmd == "drive":
        s["max_drive"] = min(1.0, max(0.0, float(a[1]))); store(s); print("saved")
    elif cmd in ("test", "wav"):
        clip = verdict_clip(int(a[1]), s)
        if clip is None:
            print("Choose your figure first: python3 plate.py sweep"); return
        if cmd == "wav":
            write_wav(a[2], clip); print("wrote", a[2])
        else:
            st = stream(s); st.write(clip); st.stop()
    else:
        print("figure %.2f Hz, ceiling %.2f, output %s  (settings: %s)" % (s["f0"], s["max_drive"], s["device"] or "default", SETTINGS))


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print()
