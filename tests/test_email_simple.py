#!/usr/bin/env python3
"""
Simple email test - sends one test email quickly.
"""

import sys
import os
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables first
load_dotenv()

from check_wrb2526 import send_email, TO_EMAIL

print(f"📧 Sending test email to {TO_EMAIL}...")

try:
    send_email("QUICK TEST - Bot email functionality working!")
    print("✅ Test email sent successfully!")
    print(f"📬 Check your inbox at: {TO_EMAIL}")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
    print("💡 Tip: Make sure your .env file is configured with Gmail App Password") 