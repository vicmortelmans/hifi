#!/bin/bash
# replace path with your LAN share
MUSIC_DIR="/home/vic/Music"

SCRIPT_NAME=$(basename "$0" .sh)
mpv "$MUSIC_DIR" \
    --shuffle \
    --force-window=yes \
    --geometry=1920x780+0+0 \
    --no-border \
    --idle=yes \
    --title=$SCRIPT_NAME \
    --force-media-title=$SCRIPT_NAME \
    --script-opts=osc=yes,osc-visibility=always \
    --no-window-dragging \
    --audio-device="pipewire/$SCRIPT_NAME" &

