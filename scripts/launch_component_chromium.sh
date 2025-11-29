#!/bin/bash
SOURCE="{source}"
NAME="{name}"
PULSE_SINK=$NAME chromium \
  --app="$SOURCE" \
  --window-size=1920,780 \
  --window-position=0,0 \
  --class=$NAME \
  --name=$NAME \
  --user-data-dir=$HOME/.hifi/$NAME \
  --disable-background-media-suspend \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --disable-features=TranslateUI \
  --disable-extensions \
  --no-first-run &

