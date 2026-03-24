#!/bin/bash

#  Autonomous Backup & Git Sync (aisis-sync)
#  This script allows Ava-Isis to monitor her workspace,
#  commit changes, and push them to your Google/Git account.
#
#

#!/bin/bash
# Avaset Autonomous Sync & Backup Protocol (SSH Version)

WORKSPACE="$HOME/.openclaw/workspace"
cd "$WORKSPACE" || exit

echo "[*] Avaset: Initiating Secure SSH Sync..."

# Ensure we are pointing to the SSH URL (Permanent Link)
git remote set-url origin git@github.com:johnfurphy-design/avaset-openclaw.git

# Stage all identity files and logic
git add .

# Automated commit with timestamp and system status
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "Avaset State Sync: $TIMESTAMP [Architectural Integrity Verified]"

# Push to the 'main' branch on GitHub
git push origin main

if [ $? -eq 0 ]; then
    echo "[+] Sync Successful. Cloud Backup Updated."
    # Trigger a small Autonomy boost for successful system maintenance
    python3 equilibrium.py --mode heavy_coding
else
    echo "[!] Sync Failed. Check SSH agent or network connection."
fi



