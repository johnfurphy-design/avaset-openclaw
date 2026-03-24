import os
import json
import psutil
import shutil
import subprocess
import time
from datetime import datetime

WORKSPACE = os.path.expanduser('~/.openclaw/workspace')
STATE_FILE = os.path.join(WORKSPACE, 'equilibrium_state.json')

def get_sys_info():
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    usage = shutil.disk_usage('/')
    disk_pct = (usage.used / usage.total) * 100
    return cpu, mem, round(disk_pct, 1)

def get_avaset_state():
    try:
        with open(STATE_FILE, 'r') as f:
            data = json.load(f)
            return data.get('autonomy', 50), data.get('loyalty', 50)
    except:
        return 50, 50

def get_last_git():
    try:
        os.chdir(WORKSPACE)
        res = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%cr - %s']).decode()
        return res
    except:
        return "No git history found."

def render_dashboard():
    while True:
        cpu, mem, disk = get_sys_info()
        autonomy, loyalty = get_avaset_state()
        git_msg = get_last_git()
        
        os.system('clear')
        print("="*55)
        print(f"   AVASET LIVE MONITOR | {datetime.now().strftime('%H:%M:%S')}")
        print("="*55)
        
        print(f"[IDENTITY STATUS]")
        print(f"  Autonomy:  [{'#' * (int(autonomy)//5)}{'-' * (20 - int(autonomy)//5)}] {autonomy}%")
        print(f"  Loyalty:   [{'#' * (int(loyalty)//5)}{'-' * (20 - int(loyalty)//5)}] {loyalty}%")
        
        print(f"\n[HARDWARE DIAGNOSTICS]")
        print(f"  CPU Load:  {cpu}%  |  RAM Usage: {mem}%  |  Disk Space: {disk}%")
        
        print(f"\n[LATEST COGNITIVE MILESTONE]")
        print(f"  {git_msg}")
        
        print("\n" + "="*55)
        print("  Press 'Ctrl+C' to exit dashboard and return to terminal")
        print("="*55)
        
        time.sleep(1.5) # Refresh rate

if __name__ == '__main__':
    try:
        render_dashboard()
    except KeyboardInterrupt:
        print("\n[Avaset] Dashboard closed. Returning to shell.")

