/*
  The Sand Table controller.

  Board:   Raspberry Pi Pico (RP2040). The plain Pico, NOT the Pico W: no radio.
  Core:    "Raspberry Pi Pico/RP2040" by Earle Philhower, in the Arduino IDE
           (Boards Manager URL: https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json)

  It listens on one wire and never talks back. From the meter it receives short lines:
    V<0-100>  a task ended; how settled the agent was (100 = completely settled)
    W1 / W0   the model is working / has stopped
    T         the model made a tool call
    H1 / H0   heartbeat: machine on / machine on but resting
  No heartbeat for 20 s means the machine is off.

  It drives the brass plate through an I2S DAC and an amplifier: always the household's own
  figure (one resonant note, chosen at setup), with clarity = how settled the agent was.
  Unsettled adds noise and a slight wander to the drive, so the figure smears and the
  tone goes grainy. The same vibration makes the sound and the figure.

  Pins (all 3.3 V logic):
    GP1   one-way wire in (UART0 RX). GP0 is NOT connected.
    GP20  I2S BCK   GP21 I2S LRCK   GP22 I2S DIN     -> PCM5102A DAC -> amplifier -> driver
    GP10  TASKS counter     (through a logic-level MOSFET to the 24 V counter coil)
    GP11  UNSETTLED counter (same)
    GP12  WORKING telltale LED      GP13 TOOL telltale LED
    GP14  gap light (MOSFET, PWM)   GP15 raking light (MOSFET, PWM)
    GP18  heartbeat pilot LED (the small blink when the machine is off)
    GP16  SETUP button to ground    GP17 LIGHTS switch to ground = all lights off
*/
#include <I2S.h>
#include <EEPROM.h>

// ------------------------------------------------------------ limits set at the desk test
const float MAX_DRIVE   = 0.30f;   // fraction of full scale: start here, raise to match your desk test. Also cap the amplifier's own gain.
const float F_LO = 80.0f, F_HI = 1200.0f;
const uint32_t RATE = 32000;

// ------------------------------------------------------------ pins
const int P_TASKS = 10, P_UNSET = 11, P_WORK = 12, P_TOOL = 13, P_GAP = 14, P_RAKE = 15,
          P_SETUP = 16, P_LIGHTS = 17, P_PILOT = 18;

// ------------------------------------------------------------ saved settings
struct Saved { uint32_t magic; float f0; int thresh; uint32_t verdicts; } saved;
const uint32_t MAGIC = 0x53414E44;  // "SAND"
void loadSaved() {
  EEPROM.begin(256); EEPROM.get(0, saved);
  if (saved.magic != MAGIC) { saved = {MAGIC, 0.0f, 50, 0}; }
}
void storeSaved() { EEPROM.put(0, saved); EEPROM.commit(); }

// ------------------------------------------------------------ shared with the audio core
volatile float vFreq = 0, vUnsettled = 0, vLevel = 0;   // level 0..1, already enveloped

// ------------------------------------------------------------ audio core (core 1)
I2S i2s(OUTPUT);
int16_t sine[1024];
uint32_t rng = 2463534242u;
inline float noise() { rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5; return (int32_t)rng / 2147483648.0f; }

void setup1() {
  for (int i = 0; i < 1024; i++) sine[i] = (int16_t)(32767 * sinf(2 * PI * i / 1024));
  i2s.setBCLK(20); i2s.setDATA(22); i2s.setBitsPerSample(16);
  i2s.begin(RATE);
}
void loop1() {
  static uint32_t phase = 0; static float lp = 0, wander = 0; static int n = 0;
  float f = vFreq, u = vUnsettled, lvl = vLevel;
  if (++n >= 256) { n = 0; wander += 0.08f * noise(); wander *= 0.98f; }     // slow random wander
  float fe = f * (1.0f + u * 0.012f * wander);
  phase += (uint32_t)(fe * 4294967296.0f / RATE);
  float s = sine[phase >> 22] / 32768.0f;
  lp += 0.15f * (noise() - lp);                                              // softened noise
  float out = lvl * MAX_DRIVE * ((1.0f - 0.6f * u) * s + 0.6f * u * lp * 2.0f);
  int16_t v = (int16_t)(constrain(out, -MAX_DRIVE, MAX_DRIVE) * 32767);   // a real ceiling: noise peaks are clipped, never louder
  i2s.write16(v, v);
}

// ------------------------------------------------------------ verdicts and envelopes
enum Mode { IDLE, VERDICT, SWEEP, FINE, HOLD } mode = IDLE;
uint32_t t0 = 0, lastHeart = 0, toolUntil = 0, pulseEnd[2] = {0, 0};
bool heartResting = false, working = false;
float sweepF = F_LO, fineCenter = 0;

void pulse(int which) {                 // one count on a mechanical counter
  int pin = which == 0 ? P_TASKS : P_UNSET;
  digitalWrite(pin, HIGH); pulseEnd[which] = millis() + 120;
}

void verdict(int settled) {
  if (saved.f0 <= 0) return;             // no figure chosen yet: do nothing rather than guess
  vFreq = saved.f0; vUnsettled = constrain((100 - settled) / 100.0f, 0.0f, 1.0f);
  mode = VERDICT; t0 = millis();
  saved.verdicts++; storeSaved();
  pulse(0); if (settled < saved.thresh) pulse(1);
}

float verdictLevel(uint32_t ms) {        // 0.4 s up, 3.5 s hold, 0.3 s down; then the brass rings down by itself
  if (ms < 400) return ms / 400.0f;
  if (ms < 3900) return 1.0f;
  if (ms < 4200) return 1.0f - (ms - 3900) / 300.0f;
  return -1;
}

// ------------------------------------------------------------ one-way wire
String line;
void handle(const String& s) {
  if (s.length() == 0) return;
  char c = s[0]; int v = s.substring(1).toInt();
  if (c == 'V') verdict(constrain(v, 0, 100));
  else if (c == 'W') working = (v == 1);
  else if (c == 'T') toolUntil = millis() + 1500;
  else if (c == 'H') { lastHeart = millis(); heartResting = (v == 0); }
}

// ------------------------------------------------------------ setup by hand: USB, with the tray open
void usbCommand(String s) {
  s.trim();
  if (s.startsWith("f ")) { vFreq = s.substring(2).toFloat(); vUnsettled = 0; vLevel = 0.7f; mode = HOLD; Serial.println("holding"); }
  else if (s == "stop") { vLevel = 0; mode = IDLE; }
  else if (s.startsWith("save ")) { saved.f0 = s.substring(5).toFloat(); storeSaved(); Serial.println("saved"); }
  else if (s.startsWith("thresh ")) { saved.thresh = s.substring(7).toInt(); storeSaved(); Serial.println("saved"); }
  else if (s.startsWith("test ")) verdict(s.substring(5).toInt());
  else if (s == "sweep") { mode = SWEEP; sweepF = F_LO; t0 = millis(); }
  else Serial.printf("figure %.2f Hz, unsettled below %d, %lu verdicts\n", saved.f0, saved.thresh, saved.verdicts);
}

// ------------------------------------------------------------ the setup button
// Press once: the plate slowly shows every figure it can make (about 15 minutes).
// Press when you see the one you like: it searches just around it.
// Press again at the crispest moment: that is your figure. Hold 3 s at any time to cancel.
uint32_t btnDown = 0; bool btnWas = false;
void button() {
  bool down = digitalRead(P_SETUP) == LOW; uint32_t now = millis();
  if (down && !btnWas) btnDown = now;
  if (!down && btnWas) {
    uint32_t held = now - btnDown;
    if (held > 3000) { mode = IDLE; vLevel = 0; }
    else if (held > 40) {
      if (mode == SWEEP) { fineCenter = sweepF; sweepF = fineCenter * 0.985f; mode = FINE; t0 = now; }
      else if (mode == FINE) { saved.f0 = sweepF; storeSaved(); vLevel = 0; mode = IDLE; delay(800); verdict(100); }
      else { mode = SWEEP; sweepF = F_LO; t0 = now; }
    }
  }
  btnWas = down;
}

// ------------------------------------------------------------ lights
void lights() {
  uint32_t now = millis();
  bool lightsOn = digitalRead(P_LIGHTS) == HIGH;
  bool alive = lastHeart && now - lastHeart < 20000;
  int gap = 0, rake = 0, pilot = 0;
  if (lightsOn) {
    if (alive && !heartResting) { gap = 180; rake = 200; }
    else if (alive) { float b = 0.5f - 0.5f * cosf(2 * PI * (now % 6000) / 6000.0f); gap = 10 + (int)(80 * b); rake = 40; }
    else { pilot = (now % 10000) < 250 ? 255 : 0; }          // off, but not broken
  }
  analogWrite(P_GAP, gap); analogWrite(P_RAKE, rake); analogWrite(P_PILOT, pilot);
  digitalWrite(P_WORK, alive && working); digitalWrite(P_TOOL, alive && now < toolUntil);
}

void setup() {
  loadSaved();
  int outs[] = {P_TASKS, P_UNSET, P_WORK, P_TOOL, P_GAP, P_RAKE, P_PILOT};
  for (int p : outs) { pinMode(p, OUTPUT); digitalWrite(p, LOW); }
  pinMode(P_SETUP, INPUT_PULLUP); pinMode(P_LIGHTS, INPUT_PULLUP);
  analogWriteFreq(20000);
  Serial.begin(115200);                        // USB: setup by hand only
  Serial1.setRX(1); Serial1.begin(9600);       // the one-way wire
}

void loop() {
  uint32_t now = millis();
  while (Serial1.available()) { char c = Serial1.read(); if (c == '\n') { handle(line); line = ""; } else if (line.length() < 16) line += c; }
  if (Serial.available()) usbCommand(Serial.readStringUntil('\n'));
  for (int i = 0; i < 2; i++) if (pulseEnd[i] && now > pulseEnd[i]) { digitalWrite(i ? P_UNSET : P_TASKS, LOW); pulseEnd[i] = 0; }
  button();
  if (mode == VERDICT) { float l = verdictLevel(now - t0); if (l < 0) { vLevel = 0; mode = IDLE; } else vLevel = l; }
  else if (mode == SWEEP) { vUnsettled = 0; vLevel = 0.7f; vFreq = sweepF; if (now - t0 > 300) { t0 = now; sweepF *= 1.001f; if (sweepF > F_HI) { mode = IDLE; vLevel = 0; } } }
  else if (mode == FINE)  { vUnsettled = 0; vLevel = 0.7f; vFreq = sweepF; if (now - t0 > 1500) { t0 = now; sweepF *= 1.0005f; if (sweepF > fineCenter * 1.015f) sweepF = fineCenter * 0.985f; } }
  lights();
}
