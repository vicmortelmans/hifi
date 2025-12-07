#!/bin/bash
# Usage: ./select_component.sh 1

COMPONENTS=("component01" "component02" "component03" "component04" "component05" "component06" "component07" "component08" "component09" "component10" "component11" "component12")
SELECT=$1

if [ -z "${COMPONENTS[$((SELECT-1))]}" ]; then
    echo "Invalid component number. Choose 1-12."
    exit 1
fi

SELECTED=${COMPONENTS[$((SELECT-1))]}

# ----- Audio switching (existing logic) -----
for COMP in "${COMPONENTS[@]}"; do
    pw-link -d $COMP:monitor_FL router_sink:playback_FL
    pw-link -d $COMP:monitor_FR router_sink:playback_FR
done
pw-link $SELECTED:monitor_FL router_sink:playback_FL
pw-link $SELECTED:monitor_FR router_sink:playback_FR

echo "Selected component: $SELECTED"

# ----- Window switching -----
# Iterate over all components
for COMP in "${COMPONENTS[@]}"; do
    if [ "$COMP" == "$SELECTED" ]; then
        # Show windows matching this component (anywhere in the line)
        wmctrl -lx | grep "$SELECTED" | awk '{print $1}' | while read WIN_ID; do
            wmctrl -i -r "$WIN_ID" -b remove,hidden
            wmctrl -i -a "$WIN_ID"
        done
    else
        # Hide windows matching this component
        wmctrl -lx | grep "$COMP" | awk '{print $1}' | while read WIN_ID; do
            wmctrl -i -r "$WIN_ID" -b add,hidden
        done
    fi
done
