#send_alert.py

# This script allows Ava-Isis to send those critical status updates to your Gmail/Google account.

import smtplib
from email.message import EmailMessage
import json

def send_status_email(subject, body):
    # Configuration - Use your Google App Password here
    EMAIL_ADDRESS = "John.Furphy@gmail.com"
    EMAIL_PASSWORD = "vsdl llvf xwnz vzwc" # Not your login password! see Email-app-PW.help

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = f"[Ava-Isis] {subject}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    # Example for an Autonomy Alert
    send_status_email("Threshold Alert", "Autonomy has reached 88%. Shifting focus to system hardening.")

