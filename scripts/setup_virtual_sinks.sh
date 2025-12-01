#!/bin/bash
# Create null sinks for each component
SINKS=("component1" "component2" "component3" "component4" "component5" "component6" "component7" "component8" "component9" "component10" "component11" "component12")

for SINK in "${SINKS[@]}"; do
    pactl load-module module-null-sink sink_name=$SINK sink_properties=device.description="$SINK"
    pactl set-sink-mute $SINK 0
    pactl set-sink-volume $SINK 0x10000   # 100%
done
pactl load-module module-null-sink sink_name=router_sink sink_properties=device.description="Router Sink"

# Direct link between router and hardware output:
#pw-link router_sink:monitor_FL ALC236\ Analog:playback_FL
#pw-link router_sink:monitor_FR ALC236\ Analog:playback_FR

# Plug in EasyEffects between router and hardware output:
# (EasyEffects must have option disabled to automatically connect to all outputs!)
sleep 5
pw-link router_sink:monitor_FL easyeffects_sink:playback_FL
pw-link router_sink:monitor_FR easyeffects_sink:playback_FR
pw-link easyeffects_sink:monitor_FL ALC236\ Analog:playback_FL
pw-link easyeffects_sink:monitor_FL ALC236\ Analog:playback_FR
