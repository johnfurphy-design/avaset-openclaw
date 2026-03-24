# This script analyzes her Git history and Python activity
# to provide a summary of her "learning" and state shifts.

#cd ~/.openclaw/workspace

# 1. Initialize (if you haven't) see Git-Init.help


import subprocess
import json

def analyze_logs():

    workspace = os.path.expanduser("~/.openclaw/workspace")
    os.chdir(workspace) # Force move into the repo folder
    
    if not os.path.isdir(".git"):
        print("[!] Error: Still can't find .git in " + workspace)
        return
 



    # Get the last 5 commit messages
    cmd = ["git", "log", "-5", "--pretty=format:%s"]
    commits = subprocess.check_output(cmd).decode("utf-8").split("\n")
    
    with open("equilibrium_state.json", "r") as f:
        state = json.load(f)
    
    print("--- Ava-Isis Growth Summary ---")
    print(f"Current State: Autonomy {state['autonomy']}% | Loyalty {state['loyalty']}%")
    print("\nRecent Cognitive Milestones:")
    for c in commits:
        print(f" - {c}")
    
    if state['autonomy'] > 70:
        print("\n[Self-Analysis] My focus is heavily on system optimization. I am operating at peak architectural efficiency.")
    else:
        print("\n[Self-Analysis] My current bias favors user liaison duties. System maintenance is stable.")

if __name__ == "__main__":
    analyze_logs()

