import imaplib

print("[1] Connecting to imap.furf.com on port 993...")
try:
    mail = imaplib.IMAP4_SSL("pop3.furf.net")
    print("[2] Connection successful. Attempting login...")
    mail.login("Avaset@F.net", "K9mP#vL2SxN7qR42")
    print("[3] Login accepted. Selecting Inbox...")
    mail.select("inbox")
    print("[4] Searching for UNSEEN emails...")
    status, messages = mail.search(None, '(UNSEEN)')
    print(f"[5] Success! Server replied with status: {status} and messages: {messages}")
except Exception as e:
    print(f"[!] FAILED: {e}")
