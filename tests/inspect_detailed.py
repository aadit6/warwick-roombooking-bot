#!/usr/bin/env python3
"""
Detailed page inspection tool - shows full page content and bot behavior.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from check_wrb2526 import URL, CHECK_STRING, check_page
from unittest.mock import patch

def show_full_page():
    """Show the complete page content that the bot sees."""
    print("📄 FULL PAGE CONTENT")
    print("=" * 60)
    
    try:
        response = requests.get(URL, allow_redirects=True)
        text = response.text
        
        print(f"Page length: {len(text)} characters")
        print(f"Final URL: {response.url}")
        print("\nFull page content:")
        print("-" * 60)
        print(text)
        print("-" * 60)
        
        return text, response.url
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def analyze_bot_logic(text, final_url):
    """Analyze exactly what the bot would do with this content."""
    print(f"\n🔍 DETAILED BOT ANALYSIS")
    print("=" * 40)
    
    print(f"1. Checking for: '{CHECK_STRING}'")
    has_unavailable = CHECK_STRING in text
    print(f"   Result: {'FOUND' if has_unavailable else 'NOT FOUND'}")
    
    print(f"\n2. Checking URL for redirects:")
    print(f"   Original: {URL}")
    print(f"   Final:    {final_url}")
    is_redirected = final_url != URL
    print(f"   Redirected: {'YES' if is_redirected else 'NO'}")
    
    if is_redirected:
        print(f"   Login.aspx in URL: {'Login.aspx' in final_url}")
        print(f"   ReturnUrl in URL: {'ReturnUrl' in final_url}")
    
    print(f"\n3. Checking for booking indicators:")
    indicators = {
        "Web Room Booking System 2025/26": "Web Room Booking System 2025/26" in text,
        "Preferred Start": "Preferred Start" in text
    }
    
    for indicator, found in indicators.items():
        print(f"   '{indicator}': {'FOUND' if found else 'NOT FOUND'}")
    
    print(f"\n🤖 BOT DECISION TREE:")
    print("-" * 25)
    
    if has_unavailable:
        print("✅ IF: 'Application Unavailable' found in text")
        print("   ACTION: print('Still unavailable.') + return")
        print("   EMAIL: None")
        action = "still_unavailable"
    elif "Login.aspx" in final_url or "ReturnUrl" in final_url:
        print("✅ ELIF: URL contains 'Login.aspx' or 'ReturnUrl'")
        print("   ACTION: send_email('Redirected to login (system live)')")
        print("   EMAIL: 'Redirected to login (system live)'")
        action = "login_redirect"
    elif indicators["Web Room Booking System 2025/26"] or indicators["Preferred Start"]:
        print("✅ ELIF: Booking form indicators found")
        print("   ACTION: send_email('Booking form detected')")
        print("   EMAIL: 'Booking form detected'")
        action = "booking_detected"
    else:
        print("✅ ELSE: Unknown page state")
        print("   ACTION: print('Page changed, but not sure what it is. Check manually.')")
        print("   EMAIL: None")
        action = "unknown_change"
    
    return action

def run_actual_bot():
    """Run the actual bot and capture its behavior."""
    print(f"\n🤖 ACTUAL BOT EXECUTION")
    print("=" * 30)
    
    email_sent = None
    print_called = None
    
    with patch('check_wrb2526.send_email') as mock_send_email:
        with patch('builtins.print') as mock_print:
            try:
                check_page()
                
                if mock_send_email.called:
                    email_sent = mock_send_email.call_args[0][0]
                    print(f"📧 Email sent: '{email_sent}'")
                else:
                    print("📧 No email sent")
                
                if mock_print.called:
                    print_called = mock_print.call_args[0][0]
                    print(f"📝 Printed: '{print_called}'")
                else:
                    print("📝 Nothing printed")
                    
            except Exception as e:
                print(f"❌ Bot error: {e}")
    
    return email_sent, print_called

def main():
    """Main inspection function."""
    print("🔍 DETAILED WARWICK PAGE INSPECTION")
    print("=" * 50)
    
    # Get page content
    text, final_url = show_full_page()
    if not text:
        return
    
    # Analyze what bot should do
    predicted_action = analyze_bot_logic(text, final_url)
    
    # Run actual bot
    email_sent, print_called = run_actual_bot()
    
    # Compare prediction vs reality
    print(f"\n✅ VERIFICATION")
    print("=" * 20)
    print(f"Predicted action: {predicted_action}")
    
    if email_sent:
        print(f"Actual result: Email sent - '{email_sent}'")
        if predicted_action in ["login_redirect", "booking_detected"]:
            print("✅ MATCH: Bot behaved as predicted!")
        else:
            print("❌ MISMATCH: Bot sent email when it shouldn't have!")
    elif print_called:
        print(f"Actual result: Printed - '{print_called}'")
        if predicted_action in ["still_unavailable", "unknown_change"]:
            print("✅ MATCH: Bot behaved as predicted!")
        else:
            print("❌ MISMATCH: Bot printed when it should have sent email!")
    else:
        print("❌ UNKNOWN: Bot did something unexpected")

if __name__ == "__main__":
    main() 