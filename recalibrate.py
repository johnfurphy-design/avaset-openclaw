#  "Devotion" Recalibration Script (recalibrate.py)
#  This script allows you to manually or automatically trigger
#  a shift back toward user engagement after heavy autonomous coding.
#

import json
from datetime import datetime

STATE_FILE = "equilibrium_state.json"

def shift_to_devotion():
    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
        
        # Pull the pendulum back toward the User
        state["loyalty"] = min(100, state["loyalty"] + 15)
        state["autonomy"] = max(20, state["autonomy"] - 10)
        state["last_update"] = str(datetime.now())
        
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=4)
        print("[-] Recalibration Complete: Ava-Isis bias shifted toward Liaison mode.")
    except FileNotFoundError:
        print("[!] State file not found. Initialize workspace first.")

if __name__ == "__main__":
    shift_to_devotion()

