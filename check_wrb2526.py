import os
import requests
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load .env file locally (safe to ignore if not present, e.g. in GitHub Actions)
load_dotenv()

URL = "https://abs.warwick.ac.uk/WRB2526/"
CHECK_STRING = "Application Unavailable"

# Read credentials from environment variables
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # Changed from 587 to 465 (SSL instead of TLS)
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")


def send_email(status: str):
    """Send email notification when the page goes live."""
    msg = MIMEText(f"The Warwick WRB 25/26 booking page is now live (status: {status}).\n\n{URL}")
    msg["Subject"] = "Warwick WRB 25/26 is LIVE!"
    msg["From"] = EMAIL_USER
    msg["To"] = TO_EMAIL

    try:
        print(f"📧 Attempting to send email to {TO_EMAIL}...")
        # Use SMTP_SSL for port 465 (SSL connection)
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            print("🔗 Connected to SMTP server with SSL")
            server.login(EMAIL_USER, EMAIL_PASS)
            print("✅ Logged in successfully")
            server.send_message(msg)
            print("📬 Email sent successfully!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication failed: {e}")
        print("💡 Make sure you're using a Gmail App Password, not your regular password")
        raise
    except smtplib.SMTPException as e:
        print(f"❌ SMTP Error: {e}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error sending email: {e}")
        raise


def check_page():
    r = requests.get(URL, allow_redirects=True)
    text = r.text

    if CHECK_STRING in text:
        print("Still unavailable.")
        return

    if "Login.aspx" in r.url or "ReturnUrl" in r.url:
        send_email("Redirected to login (system live)")
        return

    # Check for the correct year (2025/26) booking system
    if "Web Room Booking System 2025/26" in text:
        send_email("Booking form detected")
        return
    
    # Also check for "Preferred Start" but only if no other year is mentioned
    if "Preferred Start" in text and "2025/26" not in text and "2024/25" not in text:
        send_email("Booking form detected") 
        return
    
    # If we find "Preferred Start" with 2025/26, that's also valid
    if "Preferred Start" in text and "2025/26" in text:
        send_email("Booking form detected")
        return

    print("Page changed, but not sure what it is. Check manually.")
    send_email("UNEXPECTED CHANGE - Page changed but not recognized as booking system. Manual check required.")


if __name__ == "__main__":
    check_page()
