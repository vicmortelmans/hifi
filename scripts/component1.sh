#!/bin/bash
URL="https://www.mixcloud.com/"

SCRIPT_NAME=$(basename "$0" .sh)
PULSE_SINK=$SCRIPT_NAME chromium \
  --app="$URL" \
  --window-size=1920,780 \
  --window-position=0,0 \
  --class=$SCRIPT_NAME \
  --name=$SCRIPT_NAME \
  --user-data-dir=$HOME/.hifi/$SCRIPT_NAME \
  --disable-background-media-suspend \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --disable-features=TranslateUI \
  --disable-extensions \
  --no-first-run &

