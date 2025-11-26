#!/bin/bash
MAIN_OUTPUT="alsa_output.pci-0000_03_00.6.analog-stereo"  # replace with your actual main output
SINKS=("component1" "component2" "component3" "component4")

for SINK in "${SINKS[@]}"; do
    # create loopback from component monitor to main output, initially muted
    pactl load-module module-loopback source=${SINK}.monitor sink=$MAIN_OUTPUT sink_volume=0
done

