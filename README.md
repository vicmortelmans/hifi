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

In `components.yaml`, configure your virtual HIFI components. Sources can be of type `mpv` or `chromium`.

In BIOS, enable "Power on when AC is detected".
