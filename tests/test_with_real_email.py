#!/usr/bin/env python3
"""
Test scenarios with REAL email sending.
Use this to test bot behavior with actual email notifications.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, Mock
from check_wrb2526 import check_page, URL
from test_scenarios import TEST_SCENARIOS
from dotenv import load_dotenv

load_dotenv()

def test_scenario_with_real_email(scenario_name, send_real_email=False):
    """Test a scenario with optional real email sending."""
    scenario = TEST_SCENARIOS[scenario_name]
    
    print(f"\n{'='*70}")
    print(f"🧪 REAL EMAIL TEST: {scenario['name']}")
    print(f"📝 Description: {scenario['description']}")
    print(f"📧 Real Email: {'YES' if send_real_email else 'NO (mocked)'}")
    print(f"{'='*70}")
    
    # Mock the HTTP response
    mock_response = Mock()
    mock_response.text = scenario['content']
    mock_response.url = scenario['url']
    
    # Run with or without real email
    if send_real_email:
        print("🚨 WARNING: This will send a REAL EMAIL if triggered!")
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Test cancelled")
            return
    
    email_sent = None
    print_called = None
    real_email_sent = False
    
    with patch('check_wrb2526.requests.get', return_value=mock_response):
        if send_real_email:
            # Don't mock email - let it send for real
            with patch('builtins.print') as mock_print:
                try:
                    print("🤖 Running bot with REAL EMAIL enabled...")
                    check_page()
                    
                    if mock_print.called:
                        print_called = mock_print.call_args[0][0]
                        print(f"📝 Bot printed: '{print_called}'")
                    else:
                        real_email_sent = True
                        print("📧 Bot completed - check your email!")
                        
                except Exception as e:
                    print(f"❌ Error: {e}")
        else:
            # Mock email for safe testing
            with patch('check_wrb2526.send_email') as mock_send_email:
                with patch('builtins.print') as mock_print:
                    try:
                        check_page()
                        
                        if mock_send_email.called:
                            email_sent = mock_send_email.call_args[0][0]
                            print(f"📧 Bot would send email: '{email_sent}'")
                        elif mock_print.called:
                            print_called = mock_print.call_args[0][0]
                            print(f"📝 Bot printed: '{print_called}'")
                            
                    except Exception as e:
                        print(f"❌ Error: {e}")
    
    # Show expected vs actual
    print(f"\n📊 RESULTS:")
    print(f"   Expected: {scenario['expected_action']} - '{scenario['expected_message']}'")
    
    if real_email_sent:
        print(f"   Actual: Real email sent!")
        print(f"   📬 Check inbox: {os.getenv('TO_EMAIL')}")
    elif email_sent:
        print(f"   Actual: Would send email - '{email_sent}'")
    elif print_called:
        print(f"   Actual: Printed - '{print_called}'")
    else:
        print(f"   Actual: No action detected")

def quick_test_all():
    """Quick test all scenarios (no real emails)."""
    print("🧪 QUICK TEST ALL SCENARIOS")
    print("=" * 50)
    
    for scenario_name, scenario in TEST_SCENARIOS.items():
        print(f"\n🔸 {scenario['name']}")
        test_scenario_with_real_email(scenario_name, send_real_email=False)

def interactive_real_email_testing():
    """Interactive testing with real email options."""
    print("📧 REAL EMAIL SCENARIO TESTING")
    print("⚠️  Warning: Some options will send actual emails!")
    
    while True:
        print(f"\n🧪 REAL EMAIL TEST MENU")
        print(f"{'='*45}")
        
        for i, (key, scenario) in enumerate(TEST_SCENARIOS.items(), 1):
            email_icon = "📧" if scenario['expected_action'] == "email" else "📝"
            print(f"{i}. {email_icon} {scenario['name']}")
        
        print(f"\n{len(TEST_SCENARIOS) + 1}. 🧪 Quick test all (no real emails)")
        print(f"{len(TEST_SCENARIOS) + 2}. 🚨 Test booking detection with REAL EMAIL")
        print(f"{len(TEST_SCENARIOS) + 3}. 🚨 Test login redirect with REAL EMAIL")
        print(f"{len(TEST_SCENARIOS) + 4}. 👋 Exit")
        
        try:
            choice = int(input(f"\nSelect option (1-{len(TEST_SCENARIOS) + 4}): "))
            
            if choice == len(TEST_SCENARIOS) + 4:
                print("👋 Goodbye!")
                break
            elif choice == len(TEST_SCENARIOS) + 1:
                quick_test_all()
            elif choice == len(TEST_SCENARIOS) + 2:
                # Test booking detection with real email
                print("\n🎯 Testing booking form detection with REAL EMAIL")
                test_scenario_with_real_email("booking_form_wrb", send_real_email=True)
            elif choice == len(TEST_SCENARIOS) + 3:
                # Test login redirect with real email
                print("\n🎯 Testing login redirect with REAL EMAIL")
                test_scenario_with_real_email("login_redirect", send_real_email=True)
            elif 1 <= choice <= len(TEST_SCENARIOS):
                scenario_name = list(TEST_SCENARIOS.keys())[choice - 1]
                scenario = TEST_SCENARIOS[scenario_name]
                
                if scenario['expected_action'] == "email":
                    print(f"\n📧 This scenario would send email: '{scenario['expected_message']}'")
                    real_email = input("Send REAL email? (y/N): ").strip().lower() == 'y'
                else:
                    real_email = False
                
                test_scenario_with_real_email(scenario_name, send_real_email=real_email)
            else:
                print("❌ Invalid choice!")
                
        except (ValueError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            break

def main():
    """Main testing interface."""
    print("🧪 WARWICK BOOKING BOT - SCENARIO TESTING ENVIRONMENT")
    print("🎯 Test different page states and bot responses")
    print("📧 Option to send real emails for complete testing")
    
    # Check email config
    email_user = os.getenv("EMAIL_USER")
    to_email = os.getenv("TO_EMAIL")
    
    if email_user and to_email:
        print(f"✅ Email configured: {email_user} → {to_email}")
    else:
        print("⚠️  Email not configured - real email tests will fail")
    
    interactive_real_email_testing()

if __name__ == "__main__":
    main() 