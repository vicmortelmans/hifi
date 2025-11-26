#!/bin/bash
# replace path with your LAN share
MUSIC_DIR="/home/vic/Music"

SCRIPT_NAME=$(basename "$0" .sh)
mpv "$MUSIC_DIR" \
    --shuffle \
    --force-window=yes \
    --idle=yes \
    --title=$SCRIPT_NAME \
    --force-media-title=$SCRIPT_NAME \
    --script-opts=osc=yes \
    --audio-device="pipewire/$SCRIPT_NAME" \
    --geometry=800x600+200+200 &

