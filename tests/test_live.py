#!/usr/bin/env python3
"""
Live test script for the Warwick Room Booking Bot.
This tests the actual HTTP requests but mocks email sending for safety.
"""

import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import check_wrb2526


def test_live_check():
    """Test the actual page checking functionality without sending emails."""
    print("🧪 Running live test of the Warwick Room Booking Bot...")
    print(f"📡 Checking URL: {check_wrb2526.URL}")
    
    # Mock email sending to prevent accidental sends
    with patch('check_wrb2526.send_email') as mock_send_email:
        try:
            # Run the actual check_page function
            check_wrb2526.check_page()
            
            # Report results
            if mock_send_email.called:
                args, kwargs = mock_send_email.call_args
                print(f"✅ Bot would have sent email with status: '{args[0]}'")
                print("📧 Email sending was mocked - no actual email sent")
            else:
                print("ℹ️  No email would be sent (page still unavailable)")
                
        except Exception as e:
            print(f"❌ Error during page check: {e}")
            return False
    
    print("✅ Live test completed successfully!")
    return True


def test_email_configuration():
    """Test that email configuration is properly set up."""
    print("\n🔧 Testing email configuration...")
    
    import os
    from check_wrb2526 import EMAIL_USER, EMAIL_PASS, TO_EMAIL
    
    if not EMAIL_USER:
        print("⚠️  EMAIL_USER not configured")
        return False
    if not EMAIL_PASS:
        print("⚠️  EMAIL_PASS not configured")
        return False
    if not TO_EMAIL:
        print("⚠️  TO_EMAIL not configured")
        return False
    
    print(f"✅ EMAIL_USER: {EMAIL_USER}")
    print(f"✅ EMAIL_PASS: {'*' * len(EMAIL_PASS) if EMAIL_PASS else 'Not set'}")
    print(f"✅ TO_EMAIL: {TO_EMAIL}")
    return True


def test_smtp_connection():
    """Test SMTP connection without sending email."""
    print("\n🔗 Testing SMTP connection...")
    
    from check_wrb2526 import SMTP_SERVER, SMTP_PORT, EMAIL_USER, EMAIL_PASS
    import smtplib
    
    if not EMAIL_USER or not EMAIL_PASS:
        print("⚠️  Email credentials not configured, skipping SMTP test")
        return True
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            print("✅ SMTP connection successful!")
            return True
    except Exception as e:
        print(f"❌ SMTP connection failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Warwick Room Booking Bot - Live Test Suite")
    print("=" * 50)
    
    # Run all tests
    tests_passed = 0
    total_tests = 3
    
    if test_live_check():
        tests_passed += 1
        
    if test_email_configuration():
        tests_passed += 1
        
    if test_smtp_connection():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The bot is ready to run.")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
        sys.exit(1) 