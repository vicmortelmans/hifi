#!/bin/bash
# Startup script for HiFi dashboard

# --- Paths ---
BASE_DIR="$HOME/hifi"          # change to your dashboard folder
SCRIPTS_DIR="$BASE_DIR/scripts"
DASHBOARD="$BASE_DIR/dashboard.py"
BROWSER="chromium"               # change to your preferred browser

# --- Helper: run a command in the background and redirect output ---
run_bg() {
    "$@" > /dev/null 2>&1 &
}

# --- 1. Setup virtual sinks ---
echo "Setting up virtual sinks..."
run_bg "$SCRIPTS_DIR/setup_virtual_sinks.sh"

# --- 2. Setup loopbacks ---
echo "Setting up loopbacks..."
run_bg "$SCRIPTS_DIR/setup_loopbacks.sh"

# --- 3. Start Flask dashboard ---
echo "Starting dashboard..."
run_bg python3 "$DASHBOARD"

# Give the dashboard a few seconds to start
sleep 2

# --- 4. Launch browser pointing to the dashboard ---
echo "Opening dashboard in browser..."
run_bg "$BROWSER" "http://localhost:5000"

echo "HiFi system startup complete."

