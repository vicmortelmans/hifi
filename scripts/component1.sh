#!/bin/bash
URL="https://www.mixcloud.com/"

SCRIPT_NAME=$(basename "$0" .sh)
PULSE_SINK=$SCRIPT_NAME chromium \
  --class=$SCRIPT_NAME \
  --name=$SCRIPT_NAME \
  --user-data-dir=$HOME/.hifi/$SCRIPT_NAME \
  --disable-background-media-suspend \
  --new-window \
  $URL &
