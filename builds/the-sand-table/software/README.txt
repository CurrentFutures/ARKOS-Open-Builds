THE SAND TABLE: SOFTWARE

Three machines, three jobs, and they never share one:

  agent box (Raspberry Pi 5)    the agent: its loop, its tools, its files. Thinks by asking the Mac.
  Mac Studio                    the model and the meter. Nothing else. No account for the agent.
  controller (Raspberry Pi Pico, no radio, in the tray)
                                turns one number into the sand figure. Listens; never talks back.

  agent box --one Ethernet cable--> Mac (firewall: model requests only)
  Mac --one-way serial wire--> controller (the adapter's receive wire is cut)

Files
  meter.py                         the meter. Runs on the Mac as user "meter".
  mac/org.sandtable.model.plist    starts llama-server for the meter's user, on this Mac only
  mac/org.sandtable.meter.plist    starts the meter
  mac/pf-sandtable.conf            firewall for the cable to the agent box
  pi/act-allowed.sh                reads the key's ACT position on the agent box
  sandtable-controller/            firmware for the Pico (Arduino IDE)
  MAC-SETUP.txt, AGENT-BOX-SETUP.txt, CONTROLLER-SETUP.txt   step by step

The number
  For every reply the model gives (a tool call or an answer), the meter looks at the
  shakiest 10% of its words: how spread the model's probability was over its top 10
  choices. A task's number is its WORST reply, so one torn step can't hide inside a
  confident task. 100 = settled, 0 = unsettled.

  Settled is not the same as right. The figure shows how the model behaved, not
  whether its work was correct. The log (~meter/sandtable-log.csv) has an empty
  column for a person to mark whether each task was actually right; over months that
  shows what a crisp figure is worth in your house.

  The agent can't shape what's measured. The meter takes only the conversation, the
  tools and a length limit from the agent's request, and sets every sampling setting
  itself (temperature, logit bias, grammar and format are dropped).

  Worth watching: the fixed parts of a tool call (its brackets and field names) are
  forced by the format, so they read as very settled. The shakiest-10% rule mostly
  handles that, but check the log's tool_calls column: if tool-heavy tasks come out
  crisper than they deserve, that's a calibration finding.

Not tested on hardware yet: the meter was tested against a stand-in model server;
the firmware has not been compiled. Do both on the bench (guide, section 7).
