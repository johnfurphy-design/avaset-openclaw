

# Save as diagnostics.py in your workspace
import psutil
import shutil
import os

def run_diagnostics():
    print("--- Avaset System Diagnostics ---")
    
    # CPU Usage
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"[+] CPU Load: {cpu_usage}%")
    
    # RAM Usage
    memory = psutil.virtual_memory()
    print(f"[+] RAM Usage: {memory.percent}% ({memory.used // (1024**2)}MB / {memory.total // (1024**2)}MB)")
    
    # Disk Space
    total, used, free = shutil.disk_usage("/")
    print(f"[+] Disk Space: {used // (1024**3)}GB used / {free // (1024**3)}GB free")

    # Status Logic
    if cpu_usage > 80 or memory.percent > 90:
        print("[!] ALERT: System resources are critical. Avaset recommends closing background processes.")
    else:
        print("[+] System Health: Optimal.")

if __name__ == "__main__":
    run_diagnostics()

