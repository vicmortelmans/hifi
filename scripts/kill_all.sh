#!/usr/bin/env bash
# Kill remaining mpv or chromium processes
killall mpv
killall chromium  # dashboard is respawned automatically (see startup_hifi.sh)!
