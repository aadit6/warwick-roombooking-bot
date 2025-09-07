#!/usr/bin/env python3
"""
Page inspection tool for the Warwick Room Booking Bot.
This script shows exactly what the bot sees when it checks the page.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from check_wrb2526 import URL, CHECK_STRING

def inspect_page():
    """Inspect the current state of the Warwick booking page."""
    print("🔍 Warwick Room Booking Page Inspector")
    print("=" * 50)
    print(f"📡 Target URL: {URL}")
    print(f"🎯 Looking for: '{CHECK_STRING}'")
    print()
    
    try:
        print("📥 Making HTTP request...")
        response = requests.get(URL, allow_redirects=True)
        
        print(f"✅ Request successful!")
        print(f"   Status Code: {response.status_code}")
        print(f"   Final URL: {response.url}")
        print(f"   Content Length: {len(response.text)} characters")
        print()
        
        # Check if URL changed (redirected)
        if response.url != URL:
            print("🔄 REDIRECT DETECTED!")
            print(f"   Original: {URL}")
            print(f"   Final:    {response.url}")
            
            # Check for login redirect patterns
            if "Login.aspx" in response.url:
                print("   🚨 This looks like a LOGIN REDIRECT!")
                print("   ➜ Bot would send: 'Redirected to login (system live)'")
            elif "ReturnUrl" in response.url:
                print("   🚨 This looks like a RETURN URL REDIRECT!")
                print("   ➜ Bot would send: 'Redirected to login (system live)'")
            print()
        
        # Check page content
        text = response.text
        print("📄 Page Content Analysis:")
        print("-" * 30)
        
        # Check for unavailable message
        if CHECK_STRING in text:
            print(f"❌ Found: '{CHECK_STRING}'")
            print("   ➜ Bot action: Print 'Still unavailable.' (no email)")
        else:
            print(f"✅ NOT found: '{CHECK_STRING}'")
            print("   ➜ Page has changed from unavailable state!")
        
        # Check for booking system indicators
        booking_indicators = [
            "Web Room Booking System 2025/26",
            "Preferred Start",
            "booking",
            "room",
            "Reserve"
        ]
        
        print(f"\n🎯 Booking System Indicators:")
        found_indicators = []
        for indicator in booking_indicators:
            if indicator in text:
                found_indicators.append(indicator)
                print(f"   ✅ Found: '{indicator}'")
            else:
                print(f"   ❌ Not found: '{indicator}'")
        
        # Determine bot action
        print(f"\n🤖 Bot Decision Logic:")
        if CHECK_STRING in text:
            print("   📝 Action: Print 'Still unavailable.' (no email)")
        elif "Login.aspx" in response.url or "ReturnUrl" in response.url:
            print("   📧 Action: Send email 'Redirected to login (system live)'")
        elif "Web Room Booking System 2025/26" in text or "Preferred Start" in text:
            print("   📧 Action: Send email 'Booking form detected'")
        else:
            print("   ⚠️  Action: Print 'Page changed, but not sure what it is. Check manually.'")
        
        # Show page snippet
        print(f"\n📋 Page Content Sample (first 500 chars):")
        print("-" * 40)
        print(repr(text[:500]))
        if len(text) > 500:
            print("... (truncated)")
        
        # Show page title
        if "<title>" in text:
            title_start = text.find("<title>") + 7
            title_end = text.find("</title>", title_start)
            if title_end > title_start:
                title = text[title_start:title_end].strip()
                print(f"\n📰 Page Title: '{title}'")
        
        return True
        
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        print("   ➜ Bot would crash with this error")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def compare_with_bot():
    """Run the actual bot logic and compare."""
    print(f"\n🤖 Running Actual Bot Logic:")
    print("-" * 30)
    
    from check_wrb2526 import check_page
    from unittest.mock import patch
    
    # Capture the bot's output
    with patch('check_wrb2526.send_email') as mock_send_email:
        with patch('builtins.print') as mock_print:
            try:
                check_page()
                
                if mock_send_email.called:
                    args = mock_send_email.call_args[0]
                    print(f"📧 Bot would send email: '{args[0]}'")
                elif mock_print.called:
                    args = mock_print.call_args[0]
                    print(f"📝 Bot printed: '{args[0]}'")
                else:
                    print("🤔 Bot completed but no action detected")
                    
            except Exception as e:
                print(f"❌ Bot crashed: {e}")

if __name__ == "__main__":
    success = inspect_page()
    if success:
        compare_with_bot()
    
    print(f"\n" + "=" * 50)
    print("✅ Page inspection complete!")
    print("   Use this tool regularly to monitor page changes") 