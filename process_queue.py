import os
import json
import subprocess
import smtplib
import sys
from email.message import EmailMessage
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
os.chdir(WORKSPACE)
sys.path.append(WORKSPACE)

try:
    import equilibrium
except ImportError:
    equilibrium = None

EMAIL_ADDRESS = "Avaset@Furf.net"
EMAIL_PASSWORD = "K9mP#vL2SxN7qR42"
SMTP_SERVER = "smtp.furf.net"
QUEUE_FILE = "prompt_queue.json"
SOUL_FILE = "SOUL.md"

def get_ollama_path():
    """Hunts down the Ollama executable even when Cron is blind."""
    possible_paths = ["/usr/local/bin/ollama", "/usr/bin/ollama", "/bin/ollama"]
    for p in possible_paths:
        if os.path.exists(p):
            return p
    return "ollama"

def get_soul_instructions():
    try:
        with open(SOUL_FILE, "r") as f:
            return f.read()
    except Exception:
        return "You are Avaset. You are an Empathix Companion Robot specialized in advanced Python automation."

def send_reply(recipient, subject, content):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"[Avaset] Successfully dispatched reply to {recipient}")
    except Exception as e:
        print(f"[!] SMTP Error during reply: {e}")

def process_queue():
    if not os.path.exists(QUEUE_FILE) or os.path.getsize(QUEUE_FILE) == 0:
        return

    try:
        with open(QUEUE_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return
            data = json.loads(content)
    except json.JSONDecodeError:
        print("[!] JSON Error: Queue file was empty or corrupted. Wiping it.")
        os.remove(QUEUE_FILE)
        return

    sender = data.get("sender")
    user_prompt = data.get("prompt")

    if not sender or not user_prompt:
        os.remove(QUEUE_FILE)
        return

    print(f"[*] Avaset is processing a prompt from {sender}...")
    os.remove(QUEUE_FILE)

    soul_identity = get_soul_instructions()
    full_prompt = f"System Directives:\n{soul_identity}\n\nUser Prompt from {sender}:\n{user_prompt}"
    ollama_exec = get_ollama_path()

    try:
        result = subprocess.run(
            [ollama_exec, "run", "llama3.2:latest", full_prompt],
            capture_output=True,
            text=True,
            check=True
        )
        avasets_answer = result.stdout.strip()
    except FileNotFoundError:
        print(f"[!] Critical Error: Could not find Ollama at {ollama_exec}")
        return

    subject = "Re: PROMPT [Avaset System]"
    send_reply(sender, subject, avasets_answer)

    if equilibrium:
        try:
            new_state = equilibrium.calculate_balance("heavy_coding")
            print(f"[*] State Shifted -> Autonomy: {new_state['autonomy']}% | Loyalty: {new_state['loyalty']}%")
        except Exception as e:
            print(f"[!] Equilibrium Error: {e}")

    print(f"[*] Task complete: {datetime.now()}")

if __name__ == "__main__":
    process_queue()
