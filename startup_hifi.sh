#!/bin/bash
# Startup script for HiFi dashboard

# --- Paths ---
BASE_DIR="$HOME/hifi"          # change to your dashboard folder
SCRIPTS_DIR="$BASE_DIR/scripts"
DASHBOARD="$BASE_DIR/dashboard.py"
BROWSER="chromium"               # change to your preferred browser

# --- Helper: run a command in the background and redirect output ---
run_bg() {
    "$@" > $BASE_DIR/log.txt 2>&1 &
}

# --- 1. Setup virtual sinks ---
echo "Setting up virtual sinks..."
run_bg "$SCRIPTS_DIR/setup_virtual_sinks.sh"

# --- 2. Start Flask dashboard ---
echo "Starting dashboard..."
run_bg python3 "$DASHBOARD"

# Give the dashboard a few seconds to start
sleep 2

# --- 3. Monitor power ---
echo "Shut down when power is cut..."
run_bg "$SCRIPTS_DIR/shutdown_on_power_cut.sh"

# --- 4. Launch browser pointing to the dashboard ---
echo "Opening dashboard in browser..."
# Start Chromium dashboard and restart it if it exits
while true; do
    chromium \
      --app="http://localhost:5000" \
      --window-size=1920,300 \
      --window-position=0,780 \
      --class=Dashboard \
      --name=Dashboard \
      --user-data-dir=$HOME/.hifi/Dashboard \
      --disable-background-media-suspend \
      --disable-infobars \
      --disable-session-crashed-bubble \
      --disable-features=TranslateUI \
      --disable-extensions \
      --no-first-run &
    echo "HiFi system startup complete."
    wait $!
    echo "Chromium dashboard crashed or exited, restarting..."
    sleep 1
done &
