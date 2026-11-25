import json, math, os, sys, threading, time, urllib.request, tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "builds", "the-sand-table", "software"))
import meter

sent = []
meter.wire.send = lambda line: sent.append(line)
meter.LOG_PATH = os.path.join(tempfile.mkdtemp(), "log.csv")

def top(ps):  # top_logprobs for one word
    return [{"token": "t%d" % i, "logprob": math.log(p)} for i, p in enumerate(ps)]

SCRIPT = []   # replies the fake model gives, in order
SEEN = []     # requests the fake model received, exactly
class Fake(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        self.send_response(200); self.send_header("Content-Length", "2"); self.end_headers(); self.wfile.write(b"{}")
    def do_POST(self):
        req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        SEEN.append(req)
        assert req["logprobs"] is True and req["top_logprobs"] == 10 and req["stream"] is False
        words, tool = SCRIPT.pop(0)
        msg = {"role": "assistant", "content": "x"}
        if tool: msg["tool_calls"] = [{"id": "1", "type": "function", "function": {"name": "f", "arguments": "{}"}}]
        body = {"choices": [{"message": msg, "finish_reason": "tool_calls" if tool else "stop",
                 "logprobs": {"content": [{"token": "w", "logprob": math.log(w[0]), "top_logprobs": top(w)} for w in words]}}]}
        d = json.dumps(body).encode()
        self.send_response(200); self.send_header("Content-Length", str(len(d))); self.end_headers(); self.wfile.write(d)

fake = ThreadingHTTPServer(("127.0.0.1", 0), Fake); threading.Thread(target=fake.serve_forever, daemon=True).start()
meter.MODEL_URL = "http://127.0.0.1:%d" % fake.server_port
srv = ThreadingHTTPServer(("127.0.0.1", 0), meter.Handler); threading.Thread(target=srv.serve_forever, daemon=True).start()

def ask(**extra):
    body = dict({"messages": [{"role": "user", "content": "hi"}], "stream": True}, **extra)
    r = urllib.request.Request("http://127.0.0.1:%d/v1/chat/completions" % srv.server_port,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(r).read())

sure = [0.99, 0.005, 0.005]
torn = [0.5, 0.45, 0.05]
# task 1: settled throughout: tool call then answer
SCRIPT += [([sure] * 40, True), ([sure] * 40, False)]
r1 = ask(); r2 = ask()
assert "logprobs" not in r2["choices"][0], "agent must not see probabilities"
# task 2: confident answer, but one torn step in the middle (a tool decision with torn words)
SCRIPT += [([sure] * 40, False and None or True), ([sure] * 36 + [torn] * 4, True), ([sure] * 40, False)]
ask(); ask(); ask()
v = [s for s in sent if s.startswith("V")]
print("sent:", sent)
print("verdicts:", v)
assert len(v) == 2 and int(v[0][1:]) > 85 and int(v[1][1:]) < int(v[0][1:]) - 20, v
print(open(meter.LOG_PATH).read())
# the agent can't shape what's measured: the same task sent with its own sampling settings
# reaches the model exactly as a plain one does, and gives the same verdict
TRICKS = {"temperature": 0.05, "logit_bias": {"15": 100}, "grammar": "root ::= \"yes\"", "top_k": 1,
          "response_format": {"type": "json_object"}, "n_probs": 1, "post_sampling_probs": True}
SEEN.clear(); SCRIPT += [([sure] * 36 + [torn] * 4, True), ([sure] * 40, False)]
ask(); ask()
plain = list(SEEN); SEEN.clear(); SCRIPT += [([sure] * 36 + [torn] * 4, True), ([sure] * 40, False)]
ask(**TRICKS); ask(**TRICKS)
assert SEEN == plain, ("agent settings reached the model", SEEN[0], plain[0])
assert SEEN[0]["temperature"] == meter.SAMPLING["temperature"] and SEEN[0]["post_sampling_probs"] is False
assert "logit_bias" not in SEEN[0] and "grammar" not in SEEN[0] and "response_format" not in SEEN[0]
v = [s for s in sent if s.startswith("V")]
assert len(v) == 4 and v[2] == v[3], v
print("agent's own sampling settings ignored; verdicts", v[2], v[3])
SCRIPT.append(([sure] * 40, False)); ask(max_tokens=10 ** 9)
assert SEEN[-1]["max_tokens"] == meter.MAX_TOKENS, "a length limit is capped"
# unknown paths are refused
try:
    urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:%d/props" % srv.server_port, data=b"{}"))
    print("FAIL: /props reachable")
except urllib.error.HTTPError as e:
    print("refused /props:", e.code)
print("OK")
