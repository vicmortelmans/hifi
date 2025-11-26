#!/bin/bash
# Usage: ./select_component.sh 1

COMPONENTS=("component1" "component2" "component3" "component4")
SELECT=$1

if [ -z "${COMPONENTS[$((SELECT-1))]}" ]; then
    echo "Invalid component number. Choose 1-4."
    exit 1
fi

SELECTED=${COMPONENTS[$((SELECT-1))]}

# ----- Audio switching (existing logic) -----
declare -A SINK_IDS
while read -r ID NAME _; do
    SINK_IDS[$NAME]=$ID
done < <(pactl list short sinks)

# Mute all sinks
for NAME in "${COMPONENTS[@]}"; do
    pactl set-sink-mute "${SINK_IDS[$NAME]}" 1
done

# Unmute selected sink
pactl set-sink-mute "${SINK_IDS[$SELECTED]}" 0

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
