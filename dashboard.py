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


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

with open("components.yaml", "r") as f:
    config = yaml.safe_load(f)
    components = config["components"]

def is_component_running(c):
    # check if a window exists for the component
    try:
        output = subprocess.check_output(["wmctrl", "-lx"], text=True)
        for line in output.splitlines():
            if f"component{c}" in line:
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

    lines = output.splitlines()
    fl_linked = False
    fr_linked = False

    i = 0
    while i < len(lines) - 1:
        source = lines[i].strip()
        link = lines[i+1].strip()
        i += 2  # advance by 2 lines

        if source == f"component{c}:monitor_FL" and f"{router_sink_name}:playback_FL" in link:
            fl_linked = True
        elif source == f"component{c}:monitor_FR" and f"{router_sink_name}:playback_FR" in link:
            fr_linked = True

    return fl_linked and fr_linked

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

        socketio.sleep(0.1)  # 5 updates per second (adjustable)


########################################
# Routes
########################################

@app.route("/")
def index():
    return render_template("index.html", components=components)

@app.route("/select/<int:n>")
def select_component(n):
    comp_script = f"./scripts/component{n}.sh"

    if not is_component_running(n):
        subprocess.Popen([comp_script])
        # small delay to allow window to appear before selecting
    subprocess.Popen(["./scripts/select_component.sh", str(n)])
    return jsonify(success=True)

@app.route("/toggle/<int:n>")
def toggle_component(n):
    comp_script = f"./scripts/component{n}.sh"

    if is_component_running(n):
        subprocess.Popen(["./scripts/kill_component.sh", str(n)])
    else:
        subprocess.Popen([comp_script])
        # small delay to allow window to appear before selecting
        subprocess.Popen(["./scripts/select_component.sh", str(n)])
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

