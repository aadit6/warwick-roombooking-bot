#!/usr/bin/env python3
"""
Test against the REAL 2024/25 Warwick booking page.
This tests what happens when the bot encounters the actual working 2024/25 system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from unittest.mock import patch
from check_wrb2526 import check_page
from dotenv import load_dotenv

load_dotenv()

def test_real_2425_page():
    """Test what happens when bot checks the real 2024/25 page."""
    
    real_2425_url = "https://abs.warwick.ac.uk/WRB2425/"
    
    print("🧪 TESTING REAL 2024/25 PAGE")
    print("=" * 50)
    print(f"🔗 URL: {real_2425_url}")
    
    try:
        # Get the actual 2024/25 page
        print("📥 Fetching real 2024/25 page...")
        response = requests.get(real_2425_url, allow_redirects=True)
        
        print(f"✅ Response received!")
        print(f"   Status: {response.status_code}")
        print(f"   Final URL: {response.url}")
        print(f"   Content Length: {len(response.text)} characters")
        
        # Show what the page contains
        print(f"\n📄 PAGE CONTENT ANALYSIS:")
        content_checks = {
            "Application Unavailable": "Application Unavailable" in response.text,
            "Web Room Booking System 2024/25": "Web Room Booking System 2024/25" in response.text,
            "Web Room Booking System 2025/26": "Web Room Booking System 2025/26" in response.text,
            "Preferred Start": "Preferred Start" in response.text,
            "Login.aspx": "Login.aspx" in response.url,
            "ReturnUrl": "ReturnUrl" in response.url,
            "User Password": "User Password" in response.text,
            "Enterprise Foundation": "Enterprise Foundation" in response.text
        }
        
        for check, found in content_checks.items():
            status = "✅ FOUND" if found else "❌ NOT FOUND"
            print(f"   '{check}': {status}")
        
        # Show page snippet
        print(f"\n📋 PAGE CONTENT SAMPLE:")
        print("-" * 40)
        print(response.text[:800])
        if len(response.text) > 800:
            print("... (truncated)")
        print("-" * 40)
        
        # Now test what the bot would do with this page
        print(f"\n🤖 BOT BEHAVIOR TEST:")
        print("-" * 30)
        
        # Mock requests to return the real 2425 page content
        with patch('check_wrb2526.requests.get') as mock_get:
            mock_get.return_value = response
            
            # Capture what the bot does
            with patch('check_wrb2526.send_email') as mock_send_email:
                with patch('builtins.print') as mock_print:
                    try:
                        check_page()
                        
                        if mock_send_email.called:
                            email_msg = mock_send_email.call_args[0][0]
                            print(f"📧 Bot would send email: '{email_msg}'")
                        elif mock_print.called:
                            print_msg = mock_print.call_args[0][0]
                            print(f"📝 Bot would print: '{print_msg}'")
                        else:
                            print("❓ Bot completed with no action")
                            
                    except Exception as e:
                        print(f"❌ Bot error: {e}")
        
        print(f"\n" + "=" * 50)
        print("✅ Real 2024/25 page test complete!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing real 2425 page: {e}")
        return False

def test_with_real_email():
    """Test the real 2024/25 page with actual email sending."""
    
    real_2425_url = "https://abs.warwick.ac.uk/WRB2425/"
    
    print("\n🚨 REAL EMAIL TEST WITH 2024/25 PAGE")
    print("=" * 50)
    
    confirm = input("This will send a REAL EMAIL if the bot detects changes. Continue? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ Test cancelled")
        return
    
    try:
        # Get the actual 2024/25 page
        response = requests.get(real_2425_url, allow_redirects=True)
        
        print(f"📧 Testing with REAL EMAIL enabled...")
        print(f"🔗 URL: {response.url}")
        
        # Mock requests but allow real email sending
        with patch('check_wrb2526.requests.get') as mock_get:
            mock_get.return_value = response
            
            # Don't mock email - let it send for real
            try:
                check_page()
                print("✅ Bot completed - check your email!")
                
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 REAL 2024/25 PAGE TESTING")
    print("Testing bot behavior against actual working Warwick 2024/25 system")
    print()
    
    # Test what the page contains and how bot reacts
    success = test_real_2425_page()
    
    if success:
        print("\n" + "=" * 60)
        choice = input("Want to test with REAL EMAIL sending? (y/N): ").strip().lower()
        if choice in ['y', 'yes']:
            test_with_real_email()
        else:
            print("�� Test complete!") 