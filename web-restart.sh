#!/bin/bash
# Avaset Web Service Restarter

echo "[*] Restarting Avaset Streamlit UI..."
sudo systemctl restart avaset-web.service

if [ $? -eq 0 ]; then
    echo "[+] Service restarted successfully."
    # Grab just the active status line to confirm it's running
    sudo systemctl status avaset-web.service --no-pager | grep Active
else
    echo "[!] Failed to restart service. Check systemd logs."
fi
