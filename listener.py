# IMAP Listener script
#  once you've confirmed the email alerts are reaching your phone
# this will have Avaset listen every 5 minutes to check for a reply


# To make her "listen" for your emails automatically,
# add this to your crontab -e (checking every 5 minutes):
#  */5 * * * * cd ~/.openclaw/workspace && ./venv/bin/python3 listener.py >> listener.log 2>&1

#  The Feedback Loop:
#  To Send a Prompt: Email your account with the Subject: PROMPT.
#  Avaset's Action: She will extract the text and save it to external_prompt.txt.
#  OpenClaw: You can configure OpenClaw to check this file as an input source.
#-----------------------------------
# Updated Bash Alias
#Add this to your ~/.bashrc:
#   alias avaset-listen='python3 ~/.openclaw/workspace/listener.py'
#---------------------------
# OpenClaw Configuration Snippet
# Add this to your AGENTS.md or the main OpenClaw config file to ensure Avaset monitors her "inbox":
## Input Monitoring: External Prompts
#- **Source File:** `~/.openclaw/workspace/external_prompt.txt`
#- **Frequency:** Check every cycle.
#- **Instruction:** If `external_prompt.txt` contains data, prioritize it as the primary user command. After processing, clear the file #content (`> external_prompt.txt`) to prevent repeat execution.
#---------------------------------------
# Final Workflow
# Email your account with the Subject: PROMPT: Optimize Python Script.
#Avaset's Cron Job (running every 5 mins) detects the email.
#Avaset writes the text to external_prompt.txt and emails you back a confirmation.
#OpenClaw reads the file, executes the optimization, and logs the result in summarize_growth.py.
#-----------

import imaplib
import email
import smtplib
import json
import os
from email.message import EmailMessage
from datetime import datetime

# --- CONFIGURATION ---
EMAIL_ADDRESS = "John.Furphy@gmail.com"
EMAIL_PASSWORD = "vsdlllvfxwnzvzwc" 
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
STATE_FILE = "equilibrium_state.json"
INBOX_PROMPT_FILE = os.path.expanduser("~/.openclaw/workspace/external_prompt.txt")

# Ensure the prompt file exists before starting
if not os.path.exists(INBOX_PROMPT_FILE):
    with open(INBOX_PROMPT_FILE, "w") as f:
        f.write("")

PRIORITY_KEYWORDS = ["CRITICAL", "URGENT", "REBOOT", "HARDEN", "STATUS"]

def send_reply(subject, content):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = f"Re: {subject} [Avaset System]"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        print(f"[!] SMTP Error: {e}")

def get_current_status():
    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
            return f"Current State: Autonomy {state['autonomy']}% | Loyalty {state['loyalty']}%"
    except:
        return "State file unavailable."

def process_inbox():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")
        status, messages = mail.search(None, '(UNSEEN SUBJECT "PROMPT")')
        
        if status != "OK" or not messages:
            print("[+] Listener: No new prompts in inbox.")
            return

        if isinstance(messages[0], bytes):
            msg_list = messages[0].split()
        else:
            msg_list = messages

        for num in msg_list:
            _, data = mail.fetch(num, "(RFC822)")
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part)
                    if EMAIL_ADDRESS in msg.get("From"):
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                        else:
                            body = msg.get_payload(decode=True).decode()
                        
                        clean_body = body.strip()
                        subject = msg.get("Subject")

                        if "STATUS" in clean_body.upper() or "STATUS" in subject.upper():
                            send_reply(subject, f"Status Report:\n{get_current_status()}")
                        elif any(word in clean_body.upper() for word in PRIORITY_KEYWORDS):
                            send_reply(subject, f"Avaset has queued your Priority Prompt.")

                        with open(INBOX_PROMPT_FILE, "w") as f:
                            f.write(clean_body)
                        print(f"[Avaset] Prompt Received and written to {INBOX_PROMPT_FILE}")

        mail.close()
        mail.logout()
    except Exception as e:
        print(f"[!] Listener Error: {e}")

if __name__ == "__main__":
    process_inbox()

