#!/usr/bin/env python3
import eventlet
eventlet.monkey_patch()  # REQUIRED to prevent freeze

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import eventlet.green.subprocess as subprocess  # to prevent freeze
import time
import re
import subprocess
import numpy as np
import yaml
import tempfile
from pathlib import Path



app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

with open("components.yaml", "r") as f:
    config = yaml.safe_load(f)
    components = config["components"]

def is_component_running(c):
    # check if a window exists for the component
    name = f"component{c}"
    try:
        output = subprocess.check_output(["wmctrl", "-lx"], text=True)
        for line in output.splitlines():
            if name in line:
                return True
    except:
        pass
    return False


def is_component_selected(c):
    """
    Returns True if the given component is currently linked to the router_sink (both FL and FR),
    False otherwise. Handles the two-line format of 'pw-link -l'.
    """
    router_sink_name="router_sink"

    try:
        output = subprocess.check_output(["pw-link", "-l"], text=True)
    except subprocess.CalledProcessError as e:
        print("Error running pw-link:", e)
        return False

    output = output.replace('\n  |',"")
    lines = output.splitlines()
    fl_linked = False
    fr_linked = False

    for line in lines:
        if f"component{c}:monitor_FL" in line and f"{router_sink_name}:playback_FL" in line:
            fl_linked = True
        if f"component{c}:monitor_FR" in line and f"{router_sink_name}:playback_FR" in line:
            fr_linked = True
        if fl_linked and fr_linked:
            return True
    return False


def get_audio_level_for_sink(c, blocksize=4096):
    """
    Reads a short audio block from a PulseAudio monitor source
    and returns RMS level (0-100).
    """
    try:
        # 16-bit stereo: 2 bytes per sample per channel
        bytes_to_read = blocksize * 2 * 2  # blocksize samples, 2 bytes/sample, 2 channels

        # Start parec as a subprocess
        proc = subprocess.Popen(
            ["parec", "-d", f"component{c}.monitor", "--format=s16le", "--channels=2", "--rate=44100"],
            stdout=subprocess.PIPE
        )

        # Read a fixed number of bytes
        raw = proc.stdout.read(bytes_to_read)

        # Kill the process immediately to avoid streaming forever
        proc.kill()
        proc.wait()

        # Convert to numpy array
        data = np.frombuffer(raw, dtype=np.int16)
        if data.size == 0:
            return 0

        # RMS calculation
        rms = np.sqrt(np.mean(data.astype(np.float32) ** 2))
        level = min(int(rms / 32768 * 400), 100)  # was * 100
        return level

    except Exception as e:
        print(f"Error reading component{c}: {e}")
        return 0


def launch_component(c):
    component = components[c-1]

    # Load template
    template = Path(f"scripts/launch_component_{component["type"]}.sh").read_text()

    # Substitute values
    script = template.format(name=f"component{c}", source=component["source"])

    # Write temporary script
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as f:
        f.write(script)
        temp_path = f.name

    # Make executable
    Path(temp_path).chmod(0o755)

    # Run script
    subprocess.run([temp_path])

    print(f"Launched ({temp_path}):")
    print(script)

########################################
# Background thread: Streams updates
########################################

def ws_update_loop():
    while True:
        try:
            running = {c: is_component_running(c) for c in range(1,len(components)+1)}
            selected = {c: is_component_selected(c) for c in range(1,len(components)+1)}
            vu = {c: get_audio_level_for_sink(c) for c in range(1,len(components)+1)}

            # Push to all connected clients
            socketio.emit("status_update", {
                "running": running,
                "selected": selected,
                "vu": vu
            })

        except Exception as e:
            print("Error in ws_update_loop:", e)

        socketio.sleep(0.05)  # 20 updates per second (adjustable)


########################################
# Routes
########################################

@app.route("/")
def index():
    return render_template("index.html", components=components)

@app.route("/select/<int:c>")
def select_component(c):
    if not is_component_running(c):
        launch_component(c)
        # small delay to allow window to appear before selecting
    subprocess.Popen(["./scripts/select_component.sh", str(c)])
    return jsonify(success=True)

@app.route("/toggle/<int:c>")
def toggle_component(c):
    if is_component_running(c):
        subprocess.Popen(["./scripts/kill_component.sh", str(c)])
    else:
        launch_component(c)
        # small delay to allow window to appear before selecting
        subprocess.Popen(["./scripts/select_component.sh", str(c)])
    return jsonify(success=True)

@app.route("/kill_all")
def kill_all():
    for n in range(1, len(components)+1):
        subprocess.Popen(["./scripts/kill_component.sh", str(n)])
    subprocess.Popen(["./scripts/touch_sleep.sh"])
    return jsonify(success=True)

########################################
# Run background thread + server
########################################

if __name__ == "__main__":
    socketio.start_background_task(ws_update_loop)
    socketio.run(app, host="0.0.0.0", port=5000)

