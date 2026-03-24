#smtp_test.py

import smtplib
from email.message import EmailMessage

# --- CONFIGURATION ---
EMAIL_ADDRESS = "John.Furphy@gmail.com"
EMAIL_PASSWORD = "vsdl llvf xwnz vzwc" # Your 16-character App Password

def test_smtp_connection():
    print(f"[*] Connecting to smtp.gmail.com as {EMAIL_ADDRESS}...")
    
    msg = EmailMessage()
    msg.set_content("Avaset System Check: SMTP Connection Verified. Kernel is online.")
    msg['Subject'] = "[Avaset] SMTP Test Sync"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    try:
        # Port 465 is for SSL connections
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            print("[+] Connection established.")
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            print("[+] Login successful.")
            smtp.send_message(msg)
            print("[+] Test email sent. Check your phone's inbox!")
            return True
    except smtplib.SMTPAuthenticationError:
        print("[!] Error: Authentication failed. Verify your App Password is correct.")
    except Exception as e:
        print(f"[!] Error: {e}")
    return False

if __name__ == '__main__':
    test_smtp_connection()

