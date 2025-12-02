#!/usr/bin/env bash
# touch_sleep.sh
# Fake sleep with touch-to-wake for Linux Mint (X11)

# --- CONFIGURATION ---
# Screen device name (check with `xrandr`)
SCREEN="eDP"

# Dim brightness for "sleep" (0.05 = very dark, >0 so touchscreen works)
DIM_BRIGHTNESS=0.0

# Full brightness on wake
FULL_BRIGHTNESS=1.0

# Touch device (check with `libinput list-devices` or `evtest`)
TOUCH_DEVICE="/dev/input/event8"

# --- FUNCTIONS ---

# Dim screen
dim_screen() {
    xrandr --output "$SCREEN" --brightness "$DIM_BRIGHTNESS"
}

# Restore full brightness
restore_screen() {
    xrandr --output "$SCREEN" --brightness "$FULL_BRIGHTNESS"
}

# Listen for touch events (blocking)
# IMPORTANT! if this fails, the only way to restore brightness is by a cold reboot!
# PREREQUISITES:
# 1/ the TOUCH_DEVICE is correct (do ~sudo evtest~ to get a list)
# 2/ evtest can run with sudu without entering a password (do ~sudo visudo~ and add
#    "your_username ALL=(ALL) NOPASSWD: /usr/bin/evtest"
wait_for_touch() {
    sudo evtest --grab "$TOUCH_DEVICE" | while read -r line; do
        if [[ "$line" == *"EV_ABS"* ]] || [[ "$line" == *"EV_KEY"* ]]; then
            # Touch detected
            break
        fi
    done
}

# --- MAIN ---
dim_screen
echo "Fake sleep: touch the screen to wake..."
sleep 2
wait_for_touch
restore_screen
echo "Awake!"

