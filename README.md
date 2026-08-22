Setup a touchscreen laptop with Linux Mint (22.1) and Openbox window manager as a HIFI component.

Clone this repo to `~/hifi`.

In `~/.config/openbox/autostart` add:

    ```
    cd hifi
    ./startup_hifi.sh &
    ```

In `~/.config/openbox/rc.xml` add in the `<application>` section:

    ```
      <!-- Dashboard window -->
      <application class="Dashboard">
        <decor>no</decor>
      </application>

      <!-- Component windows -->
      <application class="component01">
        <decor>no</decor>
      </application>
      <application class="component02">
        <decor>no</decor>
      </application>
      <application class="component03">
        <decor>no</decor>
      </application>
      <application class="component04">
        <decor>no</decor>
      </application>
      <application class="component05">
        <decor>no</decor>
      </application>
      <application class="component06">
        <decor>no</decor>
      </application>
      <application class="component07">
        <decor>no</decor>
      </application>
      <application class="component08">
        <decor>no</decor>
      </application>
      <application class="component09">
        <decor>no</decor>
      </application>
      <application class="component10">
        <decor>no</decor>
      </application>
      <application class="component11">
        <decor>no</decor>
      </application>
      <application class="component12">
        <decor>no</decor>
      </application>
    ```

In `components.yaml`, configure your virtual HIFI components. Sources can be of type `mpv`, `chromium` or `brave-browser`.

In BIOS, enable "Power on when AC is detected".

Make sure to `sudo apt install brightnessctl` and `sudo usermod -aG video $USER`.

To output the USB audio input as online stream, install liquidsoup, get the name of the USB audio device from `pactl list short sources` and configure it in `scripts/sonos-bridge.liq` and in `scripts/cava-config`.

The dashboard window size and position is hardcoded in `startup_hifi.sh`. The component windows size and position is hardcoded in `script/launch_component_*.sh`. The cava audio visualizer window size and position is hardcoded in `scripts/cava.sh`.
