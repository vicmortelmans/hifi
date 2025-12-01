#!/bin/bash
# Very useful if BIOS has option to "Power on when AC is detected"
AC=/sys/class/power_supply/AC/online
while true; do
    if [ "$(cat $AC)" = "0" ]; then
        systemctl poweroff
    fi
    sleep 2
done
