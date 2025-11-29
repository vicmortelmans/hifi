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

# --- 3. Launch browser pointing to the dashboard ---
echo "Opening dashboard in browser..."
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

#run_bg "$BROWSER" "--class=Dashboard" "--name=Dashboard" "--user-data-dir=$HOME/.hifi/Dashboard" "--disable-background-media-suspend" "--new-window" "http://localhost:5000"

echo "HiFi system startup complete."

