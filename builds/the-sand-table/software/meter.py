#!/usr/bin/env python3
"""
The Sand Table meter.

Runs on the Mac Studio as its own user ("meter"), next to the model runtime it owns.
The agent lives on a separate small computer and reaches the model only through this
program, over the one cable between the two machines. The agent never sees the
probabilities, never sees the sand table, and cannot start, stop or configure the model.

What it does, in order:
  1. Passes each model request from the agent box to llama-server (local only),
     asking it for the top word probabilities at every step.
  2. For each reply (a "decision": a tool call or a final answer) it works out how
     unsettled the model was at its shakiest moments.
  3. When a task ends, it takes the WORST decision in the task, turns it into one
     number (0 = completely unsettled, 100 = completely settled) and sends it out
     the one-way serial wire to the sand table's controller.
  4. Writes one line per task to a log, with an empty column for a person to mark
     later whether the work was actually right.

It is arithmetic only. No second model, nothing that reads the meaning of the text.

Needs: Python 3.9+, and pyserial, installed where the start-up file looks (MAC-SETUP.txt, step 5).
The kitchen-table version needs sounddevice instead (see plate.py), and runs with
SANDTABLE_OUTPUT=audio SANDTABLE_LISTEN=127.0.0.1.
"""
import csv, json, math, os, sys, threading, time, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ---------------------------------------------------------------- settings
# Where the agent reaches the meter: the Mac's address on the one cable to the agent box.
# The kitchen-table version, with the agent on this same computer, uses 127.0.0.1.
LISTEN_HOST = os.environ.get("SANDTABLE_LISTEN", "10.77.0.1")
LISTEN_PORT = 8080                   # the only port the firewall opens to the agent box
MODEL_URL   = "http://127.0.0.1:8081"   # llama-server, bound to this Mac only
SERIAL_PORT = os.environ.get("SANDTABLE_SERIAL", "/dev/cu.usbserial-0001")
BAUD        = 9600
# "wire": verdicts go down the one-way wire to the controller (the full build, and Tier 2).
# "audio": no controller; this computer plays each verdict to the plate itself (plate.py).
OUTPUT      = os.environ.get("SANDTABLE_OUTPUT", "wire")
TOP_K       = 10                     # alternatives per word the meter looks at
SHAKY_SHARE = 0.10                   # a decision's score = mean of its shakiest 10% of words
TASK_IDLE_S = 120                    # no model request for this long also ends a task
MAX_TOKENS  = 8192                   # the longest reply the agent may ask for
# The only fields taken from the agent's request. Everything else it sends is dropped.
AGENT_FIELDS = ("messages", "tools", "tool_choice", "max_tokens")
# How the model runs, set by the meter on every request so the agent can't sharpen the
# probabilities it is measured by (no temperature, logit bias, grammar or format of its own).
# These are llama-server's usual defaults, written out. post_sampling_probs False asks for
# the model's own probabilities, before any sampling step.
SAMPLING = {"temperature": 0.8, "top_k": 40, "top_p": 0.95, "min_p": 0.05,
            "post_sampling_probs": False}
LOG_PATH    = os.path.expanduser("~/sandtable-log.csv")

# ---------------------------------------------------------------- the one-way wire
class Wire:
    """Writes short lines to the controller. Never reads: the adapter's receive wire is cut."""
    def __init__(self, port):
        self.port, self.s, self.lock = port, None, threading.Lock()
    def send(self, line):
        with self.lock:
            try:
                if self.s is None:
                    import serial
                    self.s = serial.Serial(self.port, BAUD, timeout=0, write_timeout=1)
                self.s.write((line + "\n").encode("ascii"))
            except Exception as e:           # unplugged: keep the model running, try again later
                self.s = None
                print("wire:", e, file=sys.stderr)

if OUTPUT == "audio":
    import plate
    wire = plate.Plate()
else:
    wire = Wire(SERIAL_PORT)

# ---------------------------------------------------------------- arithmetic
def word_unsettledness(top_logprobs):
    """0 = all probability on one word, 1 = spread evenly over the top-k and the rest."""
    ps = [math.exp(lp) for lp in top_logprobs[:TOP_K]]
    rest = max(0.0, 1.0 - sum(ps))
    if rest > 1e-9:
        ps.append(rest)
    h = -sum(p * math.log(p) for p in ps if p > 0)
    return min(1.0, h / math.log(TOP_K + 1))

def decision_unsettledness(words):
    """Mean of the shakiest share of words, so a confident ending can't hide a torn middle."""
    if not words:
        return None
    w = sorted(words, reverse=True)
    n = max(1, int(len(w) * SHAKY_SHARE))
    return sum(w[:n]) / n

def words_from_reply(reply):
    """Reads OpenAI-style logprobs from llama-server's chat reply."""
    out = []
    try:
        content = reply["choices"][0]["logprobs"]["content"] or []
    except (KeyError, IndexError, TypeError):
        return out
    for item in content:
        alts = [a["logprob"] for a in item.get("top_logprobs", []) if "logprob" in a]
        if alts:
            out.append(word_unsettledness(sorted(alts, reverse=True)))
    return out

# ---------------------------------------------------------------- tasks
class Tasks:
    def __init__(self):
        self.lock = threading.Lock()
        self.reset()
        self.last_request = 0.0
        self.busy = 0
    def reset(self):
        self.decisions, self.tools, self.started = [], 0, None
    def decision(self, u, tool_call):
        with self.lock:
            if self.started is None:
                self.started = time.time()
            if u is not None:
                self.decisions.append(u)
            if tool_call:
                self.tools += 1
    def end(self, why):
        with self.lock:
            if self.started is None or not self.decisions:
                self.reset()
                return
            worst = max(self.decisions)
            settled = round(100 * (1 - worst))
            row = [time.strftime("%Y-%m-%d %H:%M:%S"), settled, len(self.decisions), self.tools,
                   why, round(time.time() - self.started), ""]
            self.reset()
        wire.send("V%d" % settled)
        new = not os.path.exists(LOG_PATH)
        with open(LOG_PATH, "a", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["time", "settled_0_100", "decisions", "tool_calls", "ended_by",
                            "seconds", "was_it_right (a person fills this in)"])
            w.writerow(row)

tasks = Tasks()

# ---------------------------------------------------------------- the proxy
ALLOWED = ("/v1/chat/completions", "/v1/models")

class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def log_message(self, *a):
        pass
    def _reply(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self):
        if self.path != "/v1/models":
            return self._reply(404, {"error": "not here"})
        with urllib.request.urlopen(MODEL_URL + "/v1/models", timeout=10) as r:
            self._reply(200, json.loads(r.read()))
    def do_POST(self):
        if self.path not in ALLOWED:
            return self._reply(404, {"error": "not here"})
        try:
            req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
        except Exception:
            return self._reply(400, {"error": "bad json"})
        if not isinstance(req, dict) or not isinstance(req.get("messages"), list):
            return self._reply(400, {"error": "messages required"})
        # The meter decides how the model runs. From the agent it takes only the conversation,
        # the tools it may call and a length limit; all sampling settings are the meter's own.
        req = {k: req[k] for k in AGENT_FIELDS if k in req}
        if "max_tokens" in req:
            try:
                req["max_tokens"] = max(1, min(MAX_TOKENS, int(req["max_tokens"])))
            except (TypeError, ValueError):
                del req["max_tokens"]
        req.update(SAMPLING)
        req["stream"] = False
        req["logprobs"] = True
        req["top_logprobs"] = TOP_K
        with tasks.lock:
            tasks.last_request = time.time()
            tasks.busy += 1
        wire.send("W1")
        try:
            r = urllib.request.Request(MODEL_URL + "/v1/chat/completions",
                                       data=json.dumps(req).encode(),
                                       headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(r, timeout=900) as resp:
                reply = json.loads(resp.read())
        except Exception as e:
            return self._reply(502, {"error": "model unavailable: %s" % e})
        finally:
            with tasks.lock:
                tasks.busy -= 1
                done = tasks.busy == 0
            if done:
                wire.send("W0")
        choice = (reply.get("choices") or [{}])[0]
        msg = choice.get("message") or {}
        tool_call = bool(msg.get("tool_calls"))
        if tool_call:
            wire.send("T")
        tasks.decision(decision_unsettledness(words_from_reply(reply)), tool_call)
        if choice.get("finish_reason") == "stop" and not tool_call:
            tasks.end("answer")
        choice.pop("logprobs", None)          # the agent never sees the probabilities
        self._reply(200, reply)

# ---------------------------------------------------------------- heartbeat
def heartbeat():
    while True:
        idle = time.time() - tasks.last_request
        if tasks.started is not None and tasks.busy == 0 and idle > TASK_IDLE_S:
            tasks.end("idle")
        try:
            urllib.request.urlopen(MODEL_URL + "/health", timeout=3).read()
            wire.send("H1" if idle < 600 else "H0")     # H0 = on but resting: the gap light breathes
        except Exception:
            pass                                          # no heartbeat: the controller shows "off"
        time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=heartbeat, daemon=True).start()
    print("meter listening on %s:%d, verdicts to the %s" % (LISTEN_HOST, LISTEN_PORT, "plate (audio)" if OUTPUT == "audio" else "wire"))
    ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), Handler).serve_forever()
