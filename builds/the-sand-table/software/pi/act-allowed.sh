#!/bin/sh
# Prints "yes" if the key is in ACT, "no" otherwise. The agent's tool policy calls this
# before any action that changes something (sending, buying, deleting, writing outside its folder).
# The key's ACT contact pulls GPIO 17 to ground.
if pinctrl get 17 | grep -q " lo"; then echo yes; else echo no; fi
