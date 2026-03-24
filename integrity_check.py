# integrity_check.py
# This script verifies that all required files exist,
#  the virtual environment is active,
#  and the state JSON is valid.

import os
import json
import sys

def check_integrity():
    required_files = [
        "SOUL.md", "equilibrium.py", "recalibrate.py", 
        "summarize_growth.py", "aisis-sync.sh", "send_alert.py", 
        "check_autonomy.sh", "equilibrium_state.json"
    ]
    
    print("--- Ava-Isis System Integrity Check ---")
    
    # 1. Check Virtual Env
    if not hasattr(sys, 'real_prefix') and not (sys.base_prefix != sys.prefix):
        print("[!] WARNING: Virtual environment NOT active. Run 'source venv/bin/activate'.")
    else:
        print("[+] Python Virtual Environment: ACTIVE")

    # 2. Check Files
    for f in required_files:
        if os.path.exists(f):
            print(f"[+] File Found: {f}")
        else:
            print(f"[!] MISSING: {f}")

    # 3. Validate JSON
    try:
        with open("equilibrium_state.json", "r") as j:
            data = json.load(j)
            print(f"[+] State Valid: Autonomy({data['autonomy']}%) Loyalty({data['loyalty']}%)")
    except Exception as e:
        print(f"[!] State Error: {e}")

if __name__ == "__main__":
    check_integrity()

