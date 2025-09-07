#!/usr/bin/env python3
"""
Email testing script for the Warwick Room Booking Bot.
This script safely tests actual email sending functionality.
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables FIRST
load_dotenv()

from check_wrb2526 import send_email, EMAIL_USER, EMAIL_PASS, TO_EMAIL


def test_email_credentials():
    """Check if email credentials are properly configured."""
    print("🔧 Checking email credentials...")
    
    missing = []
    if not EMAIL_USER:
        missing.append("EMAIL_USER")
    if not EMAIL_PASS:
        missing.append("EMAIL_PASS")
    if not TO_EMAIL:
        missing.append("TO_EMAIL")
    
    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        print("\n📝 Please create a .env file with:")
        print("EMAIL_USER=your-email@gmail.com")
        print("EMAIL_PASS=your-gmail-app-password")
        print("TO_EMAIL=recipient@example.com")
        return False
    
    print(f"✅ EMAIL_USER: {EMAIL_USER}")
    print(f"✅ EMAIL_PASS: {'*' * len(EMAIL_PASS)}")
    print(f"✅ TO_EMAIL: {TO_EMAIL}")
    return True


def send_test_email():
    """Send a test email to verify functionality."""
    print("\n📧 Sending test email...")
    
    try:
        send_email("TEST - Email functionality verification")
        print("✅ Test email sent successfully!")
        print(f"📬 Check your inbox at: {TO_EMAIL}")
        return True
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        print("\n🔍 Common solutions:")
        print("1. Use Gmail App Password (not regular password)")
        print("2. Enable 2-factor authentication on Gmail")
        print("3. Check if Gmail account allows less secure apps")
        return False


def interactive_test():
    """Interactive email testing with user confirmation."""
    print("🚀 Interactive Email Test")
    print("=" * 40)
    
    if not test_email_credentials():
        return False
    
    print(f"\n⚠️  This will send a TEST EMAIL to: {TO_EMAIL}")
    response = input("Do you want to proceed? (y/N): ").strip().lower()
    
    if response not in ['y', 'yes']:
        print("❌ Test cancelled by user")
        return False
    
    return send_test_email()


def batch_test():
    """Send multiple test emails to verify different scenarios."""
    print("\n🔄 Batch Email Test")
    print("=" * 30)
    
    test_scenarios = [
        "TEST 1 - Bot detection: Redirected to login (system live)",
        "TEST 2 - Bot detection: Booking form detected", 
        "TEST 3 - Bot detection: Manual check required"
    ]
    
    print(f"⚠️  This will send {len(test_scenarios)} test emails to: {TO_EMAIL}")
    response = input("Do you want to proceed? (y/N): ").strip().lower()
    
    if response not in ['y', 'yes']:
        print("❌ Batch test cancelled by user")
        return False
    
    success_count = 0
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n📧 Sending test email {i}/{len(test_scenarios)}...")
        try:
            send_email(scenario)
            print(f"✅ Test email {i} sent successfully")
            success_count += 1
        except Exception as e:
            print(f"❌ Test email {i} failed: {e}")
    
    print(f"\n📊 Results: {success_count}/{len(test_scenarios)} emails sent successfully")
    return success_count == len(test_scenarios)


def simulate_bot_trigger():
    """Simulate what happens when the bot detects the booking system is live."""
    print("\n🤖 Simulating Bot Trigger")
    print("=" * 35)
    
    print("This simulates what happens when the bot detects the booking system is live.")
    print(f"⚠️  This will send a REALISTIC notification email to: {TO_EMAIL}")
    response = input("Do you want to proceed? (y/N): ").strip().lower()
    
    if response not in ['y', 'yes']:
        print("❌ Simulation cancelled by user")
        return False
    
    print("\n🎯 Simulating: Booking system detected as live...")
    try:
        # This is exactly what the bot would send
        send_email("Booking form detected")
        print("✅ Simulation complete!")
        print("📬 You should receive a notification email identical to what the bot would send")
        return True
    except Exception as e:
        print(f"❌ Simulation failed: {e}")
        return False


def main():
    """Main testing interface."""
    print("📧 Warwick Room Booking Bot - Email Testing Suite")
    print("=" * 55)
    
    if not test_email_credentials():
        sys.exit(1)
    
    while True:
        print("\n🔧 Test Options:")
        print("1. Send single test email")
        print("2. Send batch test emails (3 emails)")
        print("3. Simulate realistic bot notification")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            interactive_test()
        elif choice == '2':
            batch_test()
        elif choice == '3':
            simulate_bot_trigger()
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    main() 