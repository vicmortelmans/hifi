#!/bin/bash
# Usage: ./kill_component.sh 1

COMPONENTS=("component1" "component2" "component3" "component4" "component5" "component6" "component7" "component8" "component9" "component10" "component11" "component12")
SELECT=$1

if [ -z "${COMPONENTS[$((SELECT-1))]}" ]; then
    echo "Invalid component number. Choose 1-4."
    exit 1
fi

SELECTED=${COMPONENTS[$((SELECT-1))]}

for WIN_ID in $(wmctrl -lx | grep "$SELECTED" | awk '{print $1}'); do
    wmctrl -i -c "$WIN_ID"  # politely close
    # or force kill:
    # PID=$(xprop -id $WIN_ID _NET_WM_PID | awk '{print $3}')
    # kill "$PID"
done

