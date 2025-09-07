#!/usr/bin/env python3
"""
Real email integration test - sends actual emails with user confirmation.
This test verifies the email functionality works end-to-end.
"""

import unittest
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load real environment variables
load_dotenv()

from check_wrb2526 import send_email, EMAIL_USER, EMAIL_PASS, TO_EMAIL


class TestRealEmailIntegration(unittest.TestCase):
    """Integration tests that send real emails (with user confirmation)."""

    @classmethod
    def setUpClass(cls):
        """Set up class-level test environment."""
        # Check if real credentials are available
        if not all([EMAIL_USER, EMAIL_PASS, TO_EMAIL]):
            raise unittest.SkipTest("Real email credentials not configured in .env file")

    def test_real_email_sending(self):
        """Test sending real email (requires manual confirmation)."""
        print(f"\n🚨 WARNING: This test will send a REAL EMAIL to: {TO_EMAIL}")
        print("This is an integration test to verify end-to-end email functionality.")
        
        # In automated testing, skip this test unless explicitly enabled
        if os.getenv("ENABLE_REAL_EMAIL_TESTS") != "true":
            self.skipTest("Real email test skipped. Set ENABLE_REAL_EMAIL_TESTS=true to enable.")
        
        # Send a test email
        try:
            send_email("INTEGRATION TEST - Real email functionality verification")
            print("✅ Real email sent successfully!")
            print(f"📬 Check your inbox at: {TO_EMAIL}")
        except Exception as e:
            self.fail(f"Real email sending failed: {e}")

    def test_email_credentials_valid(self):
        """Test that email credentials are valid and accessible."""
        self.assertIsNotNone(EMAIL_USER, "EMAIL_USER should be set")
        self.assertIsNotNone(EMAIL_PASS, "EMAIL_PASS should be set") 
        self.assertIsNotNone(TO_EMAIL, "TO_EMAIL should be set")
        
        self.assertNotEqual(EMAIL_USER, "", "EMAIL_USER should not be empty")
        self.assertNotEqual(EMAIL_PASS, "", "EMAIL_PASS should not be empty")
        self.assertNotEqual(TO_EMAIL, "", "TO_EMAIL should not be empty")
        
        # Basic email format validation
        self.assertIn("@", EMAIL_USER, "EMAIL_USER should be a valid email")
        self.assertIn("@", TO_EMAIL, "TO_EMAIL should be a valid email")

    def test_smtp_configuration(self):
        """Test that SMTP configuration constants are correct."""
        from check_wrb2526 import SMTP_SERVER, SMTP_PORT
        
        self.assertEqual(SMTP_SERVER, "smtp.gmail.com")
        self.assertEqual(SMTP_PORT, 465)  # Should be 465 for SSL


if __name__ == '__main__':
    print("🧪 Real Email Integration Tests")
    print("=" * 40)
    print("These tests verify email functionality with real SMTP connections.")
    print("Some tests may be skipped unless explicitly enabled.")
    print("")
    
    # Run with high verbosity
    unittest.main(verbosity=2) 