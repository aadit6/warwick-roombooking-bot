import os
import requests
import smtplib
from email.mime.text import MIMEText

URL = "https://abs.warwick.ac.uk/WRB2526/"
CHECK_STRING = "Application Unavailable"  # only present while closed

# read email settings from environment variables
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
TO_EMAIL = os.environ.get("TO_EMAIL")


def send_email(status: str):
    """Send email notification when the page goes live."""
    msg = MIMEText(f"The Warwick WRB 25/26 booking page is now live (status: {status}).\n\n{URL}")
    msg["Subject"] = "Warwick WRB 25/26 is LIVE!"
    msg["From"] = EMAIL_USER
    msg["To"] = TO_EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)


def check_page():
    r = requests.get(URL, allow_redirects=True)
    text = r.text

    if CHECK_STRING in text:
        print("Still unavailable.")
        return

    if "Login.aspx" in r.url or "ReturnUrl" in r.url:
        send_email("Redirected to login (system live)")
        return

    if "Web Room Booking System 2025/26" in text or "Preferred Start" in text:
        send_email("Booking form detected")
        return

    print("Page changed, but not sure what it is. Check manually.")


if __name__ == "__main__":
    check_page()
