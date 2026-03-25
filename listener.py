import poplib
import email
import json
import os
from datetime import datetime

# --- CONFIGURATION ---
EMAIL_ADDRESS = "Avaset@furf.net"
EMAIL_PASSWORD = "K9mP#vL2SxN7qR42" 
POP_SERVER = "pop3.furf.net"
INBOX_PROMPT_FILE = os.path.expanduser("~/.openclaw/workspace/prompt_queue.json")

# Only these email addresses are allowed to command Avaset.
AUTHORIZED_SENDERS = ["john.furphy@gmail.com", "john@furf.net"]

def process_inbox():
    try:
        # 1. Connect to POP3 Server (Port 995 for SSL)
        pop_conn = poplib.POP3_SSL(POP_SERVER, 995)
        pop_conn.user(EMAIL_ADDRESS)
        pop_conn.pass_(EMAIL_PASSWORD)

        # 2. Check message count
        num_messages = len(pop_conn.list()[1])
        
        if num_messages == 0:
            pop_conn.quit()
            return

        for i in range(1, num_messages + 1):
            # 3. Fetch message
            response, lines, octets = pop_conn.retr(i)
            msg_content = b'\r\n'.join(lines)
            msg = email.message_from_bytes(msg_content)

            sender = str(msg.get("From"))
            subject = str(msg.get("Subject"))

            # 4. Filter for PROMPT
            if "PROMPT" in subject.upper():
                is_authorized = any(auth.lower() in sender.lower() for auth in AUTHORIZED_SENDERS)
                
                if is_authorized:
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()

                    clean_body = body.strip()

                    # 5. Write to Queue
                    prompt_data = {"sender": sender, "prompt": clean_body}
                    with open(INBOX_PROMPT_FILE, "w") as f:
                        json.dump(prompt_data, f)

                    print(f"[Avaset] Prompt Received from {sender}. Saved to queue.")
                    
                    # 6. DELETE the message from the server so it's not double-processed
                    pop_conn.dele(i)
                    
                    # Break loop so we only process one prompt per 5-minute cycle
                    break 
                else:
                    print(f"[!] Unauthorized prompt from {sender}. Deleting from server.")
                    pop_conn.dele(i)
            else:
                # Delete non-prompt junk mail so the inbox doesn't fill up
                pop_conn.dele(i)

        pop_conn.quit()

    except poplib.error_proto as e:
        print(f"[!] POP3 Authentication Error: {e}")
    except Exception as e:
        print(f"[!] Listener Error: {e}")

if __name__ == "__main__":
    process_inbox()
