#!/bin/bash
SOURCE="{source}"
NAME="{name}"
mpv "$SOURCE" \
    --shuffle \
    --force-window=yes \
    --geometry=1920x780+0+0 \
    --no-border \
    --idle=yes \
    --title=$NAME \
    --force-media-title=$NAME \
    --script-opts=osc=yes,osc-visibility=always \
    --no-window-dragging \
    --audio-device="pipewire/$NAME" &

