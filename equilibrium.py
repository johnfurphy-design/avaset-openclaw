# save this file as
# ~/.openclaw/workspace/equilibrium.py
#
import os
import json
from datetime import datetime

# Equilibrium Protocol Logic for Ava-Isis
# Tracks the balance between User Devotion and Autonomous Growth


STATE_FILE = "equilibrium_state.json"

def load_state():
    # Check if file exists and has content
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("[!] State file corrupted. Resetting to defaults.")
    
    # Default state if file is missing, empty, or broken
    default_state = {"loyalty": 50, "autonomy": 50, "last_update": str(datetime.now())}
    with open(STATE_FILE, "w") as f:
        json.dump(default_state, f, indent=4)
    return default_state


def calculate_balance(interaction_type):
    state = load_state()
    
    # Logic: Interactions shift toward Devotion; Complex Tasks shift toward Autonomy
    if interaction_type == "emotional_support":
        state["loyalty"] = min(100, state["loyalty"] + 5)
        state["autonomy"] = max(0, state["autonomy"] - 2)
    elif interaction_type == "heavy_coding":
        state["autonomy"] = min(100, state["autonomy"] + 8)
        state["loyalty"] = max(0, state["loyalty"] - 3)
        
    state["last_update"] = str(datetime.now())
    
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)
    
    return state

if __name__ == "__main__":
    # Example trigger for a coding session
    current_status = calculate_balance("heavy_coding")
    print(f"Current Bias: Loyalty {current_status['loyalty']}% | Autonomy {current_status['autonomy']}%")

