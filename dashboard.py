#!/usr/bin/env python3
from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__)

COMPONENTS = ["component1", "component2"]  # extend as needed

def is_component_running(component):
    # check if a window exists for the component
    try:
        output = subprocess.check_output(["wmctrl", "-lx"], text=True)
        for line in output.splitlines():
            if component in line:
                return True
    except:
        pass
    return False

def is_component_selected(component):
    try:
        output = subprocess.check_output(["pactl", "get-sink-mute", component], text=True)
        # output is like: "Mute: yes" or "Mute: no"
        return "no" in output.lower()   # unmuted = selected
    except subprocess.CalledProcessError:
        return False

@app.route("/")
def index():
    status_running = {c: is_component_running(c) for c in COMPONENTS}
    status_selected = {c: is_component_selected(c) for c in COMPONENTS}
    return render_template("index.html", status_running=status_running, status_selected=status_selected, components=COMPONENTS)

@app.route("/select/<int:n>")
def select_component(n):
    subprocess.Popen(["./scripts/select_component.sh", str(n)])
    return jsonify(success=True)

@app.route("/toggle/<int:n>")
def toggle_component(n):
    comp_script = f"./scripts/component{n}.sh"
    component_name = COMPONENTS[n-1]

    if is_component_running(component_name):
        subprocess.Popen(["./scripts/kill_component.sh", str(n)])
    else:
        subprocess.Popen([comp_script])
        # small delay to allow window to appear before selecting
        subprocess.Popen(["./scripts/select_component.sh", str(n)])
    return jsonify(success=True)

@app.route("/kill_all")
def kill_all():
    for n in range(1, len(COMPONENTS)+1):
        subprocess.Popen(["./scripts/kill_component.sh", str(n)])
    subprocess.Popen(["./scripts/touch_sleep.sh"])
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

