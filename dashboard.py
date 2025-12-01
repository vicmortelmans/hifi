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
import subprocess
import threading


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Read config file
with open("components.yaml", "r") as f:
    config = yaml.safe_load(f)
    components = config["components"]

# VU meter setup
SAMPLE_RATE = 48000
CHANNELS = 2
BLOCK_SIZE = 4800  # 100ms
# Shared dict for latest values
latest_rms = {c: 0 for c in range(1,len(components)+1)}


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


def monitor_component(c):
    # Used as a thread
    cmd = [
        "parec",
        "--format=s16le",
        f"--rate={SAMPLE_RATE}",
        f"--channels={CHANNELS}",
        f"--device=component{c}.monitor"
    ]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=BLOCK_SIZE*CHANNELS*2) as proc:
        while True:
            raw = proc.stdout.read(BLOCK_SIZE*CHANNELS*2)
            if len(raw) < BLOCK_SIZE*CHANNELS*2:
                break
            data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
            data = data.reshape(-1, CHANNELS)
            rms = 2*np.sqrt(np.mean(data**2, axis=0)).mean()
            latest_rms[c] = int(rms*100)


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
# Background threads for VU sampling
########################################

# Start one thread per component
for c in range(1,len(components)+1):
    threading.Thread(target=monitor_component, args=(c,), daemon=True).start()


########################################
# Background thread: Streams updates
########################################

def ws_update_loop():
    while True:
        try:
            running = {c: is_component_running(c) for c in range(1,len(components)+1)}
            selected = {c: is_component_selected(c) for c in range(1,len(components)+1)}

            # Push to all connected clients
            socketio.emit("status_update", {
                "running": running,
                "selected": selected
            })

        except Exception as e:
            print("Error in ws_update_loop:", e)

        socketio.sleep(0.5)  # 2 updates per second (adjustable)


def ws_vu_loop():
    while True:
        try:
            # Push to all connected clients
            socketio.emit("vu", {
                "vu": latest_rms
            })

        except Exception as e:
            print("Error in ws_vu_loop:", e)

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
    socketio.start_background_task(ws_vu_loop)
    socketio.run(app, host="0.0.0.0", port=5000)

