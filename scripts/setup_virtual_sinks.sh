#!/bin/bash
# Create null sinks for each component
SINKS=("component1" "component2" "component3" "component4")

for SINK in "${SINKS[@]}"; do
    pactl load-module module-null-sink sink_name=$SINK sink_properties=device.description="$SINK"
done
pactl load-module module-null-sink sink_name=router_sink sink_properties=device.description="Router Sink"
pw-link router_sink:monitor_FL ALC236\ Analog:playback_FL
pw-link router_sink:monitor_FR ALC236\ Analog:playback_FR


