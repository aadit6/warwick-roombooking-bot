#!/usr/bin/env python3
"""
Clean page summary tool - shows key page information and bot behavior.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from check_wrb2526 import URL, CHECK_STRING, check_page
from unittest.mock import patch

def main():
    """Show page summary and bot behavior."""
    print("📊 WARWICK BOOKING PAGE SUMMARY")
    print("=" * 45)
    
    try:
        # Get page
        response = requests.get(URL, allow_redirects=True)
        text = response.text
        
        # Basic info
        print(f"🌐 URL: {URL}")
        print(f"📄 Status: {response.status_code}")
        print(f"📏 Size: {len(text)} characters")
        print(f"🔗 Final URL: {response.url}")
        
        # Check for key strings
        print(f"\n🔍 KEY CONTENT ANALYSIS:")
        checks = {
            f"'{CHECK_STRING}'": CHECK_STRING in text,
            "'Web Room Booking System 2025/26'": "Web Room Booking System 2025/26" in text,
            "'Preferred Start'": "Preferred Start" in text,
            "URL redirected": response.url != URL,
            "'Login.aspx' in URL": "Login.aspx" in response.url,
            "'ReturnUrl' in URL": "ReturnUrl" in response.url
        }
        
        for check, result in checks.items():
            status = "✅ FOUND" if result else "❌ NOT FOUND"
            print(f"   {check}: {status}")
        
        # Bot decision
        print(f"\n🤖 BOT BEHAVIOR:")
        if CHECK_STRING in text:
            print("   📝 Action: Print 'Still unavailable.'")
            print("   📧 Email: None")
            print("   ✅ Status: Working correctly - page not live yet")
        elif "Login.aspx" in response.url or "ReturnUrl" in response.url:
            print("   📧 Action: Send 'Redirected to login (system live)'")
            print("   🚨 Status: BOOKING SYSTEM IS LIVE!")
        elif "Web Room Booking System 2025/26" in text or "Preferred Start" in text:
            print("   📧 Action: Send 'Booking form detected'")
            print("   🚨 Status: BOOKING SYSTEM IS LIVE!")
        else:
            print("   ⚠️  Action: Print 'Page changed, check manually'")
            print("   🔍 Status: Unknown page state")
        
        # Page title
        if "<title>" in text:
            title_start = text.find("<title>") + 7
            title_end = text.find("</title>", title_start)
            if title_end > title_start:
                title = text[title_start:title_end].strip()
                print(f"\n📰 Page Title: '{title}'")
        
        # Test actual bot
        print(f"\n🧪 ACTUAL BOT TEST:")
        with patch('check_wrb2526.send_email') as mock_send_email:
            with patch('builtins.print') as mock_print:
                check_page()
                
                if mock_send_email.called:
                    email_msg = mock_send_email.call_args[0][0]
                    print(f"   📧 Result: Email sent - '{email_msg}'")
                    print("   🚨 ALERT: BOOKING SYSTEM DETECTED AS LIVE!")
                elif mock_print.called:
                    print_msg = mock_print.call_args[0][0]
                    print(f"   📝 Result: Printed - '{print_msg}'")
                    print("   ✅ Status: Normal operation (system not live)")
                else:
                    print("   ❓ Result: Unknown behavior")
        
        print(f"\n" + "=" * 45)
        print("✅ Page analysis complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 