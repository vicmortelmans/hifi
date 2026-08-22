#!/bin/bash
# geometry width '999' is measured in characters, so it means "full width"
cd scripts
xfce4-terminal -e "cava -p cava-config" --hide-menubar --hide-borders --hide-toolbar --hide-scrollbar --geometry=999x10+0-0 --color-bg=black &
wmctrl -r 'xfce4-terminal' -b add,above
picom --config /dev/null
