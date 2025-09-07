#!/usr/bin/env python3
"""
Test scenarios for different page states.
This simulates various page conditions to test bot behavior.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, Mock
from check_wrb2526 import check_page, URL
from dotenv import load_dotenv

# Load environment for email testing
load_dotenv()

# Test page scenarios
TEST_SCENARIOS = {
    "unavailable": {
        "name": "🔴 System Unavailable (Current State)",
        "description": "Page shows 'Application Unavailable'",
        "url": URL,
        "content": """
<!DOCTYPE html>
<html>
<head><title>Scientia Web Room Booking</title></head>
<body>
    <div class="Banner">
        <span class="BannerTitle">Application Unavailable</span>
        <span class="Text">The web room booking facility is currently unavailable. Please try again later.</span>
    </div>
    <td>Web Room Booking System 2025/26</td>
</body>
</html>
        """,
        "expected_action": "print",
        "expected_message": "Still unavailable."
    },
    
    "login_redirect": {
        "name": "🟡 Login Redirect (System Live)",
        "description": "Page redirects to login - system is live but requires auth",
        "url": "https://abs.warwick.ac.uk/Login.aspx?ReturnUrl=/WRB2526/",
        "content": """
<!DOCTYPE html>
<html>
<head><title>Login - Warwick</title></head>
<body>
    <form>
        <h2>Please log in</h2>
        <input type="text" name="username" placeholder="Username">
        <input type="password" name="password" placeholder="Password">
        <button>Log In</button>
    </form>
</body>
</html>
        """,
        "expected_action": "email",
        "expected_message": "Redirected to login (system live)"
    },
    
    "return_url": {
        "name": "🟡 Return URL (System Live)",
        "description": "Page has ReturnUrl parameter - another login scenario",
        "url": "https://abs.warwick.ac.uk/some/path?ReturnUrl=/WRB2526/",
        "content": """
<!DOCTYPE html>
<html>
<head><title>Access Required</title></head>
<body>
    <h1>Access Required</h1>
    <p>Please authenticate to continue</p>
</body>
</html>
        """,
        "expected_action": "email",
        "expected_message": "Redirected to login (system live)"
    },
    
    "booking_form_wrb": {
        "name": "🟢 Booking Form (WRB Text)",
        "description": "Booking form detected via 'Web Room Booking System 2025/26'",
        "url": URL,
        "content": """
<!DOCTYPE html>
<html>
<head><title>Room Booking System</title></head>
<body>
    <h1>Web Room Booking System 2025/26</h1>
    <form>
        <label>Select Room:</label>
        <select name="room">
            <option>Meeting Room A</option>
            <option>Conference Room B</option>
        </select>
        <label>Date:</label>
        <input type="date" name="date">
        <button>Book Room</button>
    </form>
</body>
</html>
        """,
        "expected_action": "email",
        "expected_message": "Booking form detected"
    },
    
    "booking_form_preferred": {
        "name": "🟢 Booking Form (Preferred Start)",
        "description": "Booking form detected via 'Preferred Start' text",
        "url": URL,
        "content": """
<!DOCTYPE html>
<html>
<head><title>Room Booking</title></head>
<body>
    <h1>Room Booking System</h1>
    <form>
        <label>Preferred Start Time:</label>
        <input type="time" name="start_time">
        <label>Duration:</label>
        <select name="duration">
            <option>1 hour</option>
            <option>2 hours</option>
        </select>
        <button>Submit Booking</button>
    </form>
</body>
</html>
        """,
        "expected_action": "email", 
        "expected_message": "Booking form detected"
    },
    
    "wrb_2425": {
        "name": "🟠 WRB 2024/25 (Wrong Year)",
        "description": "Page shows 2024/25 system instead of 2025/26",
        "url": URL,
        "content": """
<!DOCTYPE html>
<html>
<head><title>Room Booking System</title></head>
<body>
    <h1>Web Room Booking System 2024/25</h1>
    <form>
        <label>Select Room:</label>
        <select name="room">
            <option>Meeting Room A</option>
            <option>Conference Room B</option>
        </select>
        <label>Preferred Start Time:</label>
        <input type="time" name="start_time">
        <button>Book Room</button>
    </form>
</body>
</html>
        """,
        "expected_action": "email",
        "expected_message": "UNEXPECTED CHANGE - Page changed but not recognized as booking system. Manual check required."
    },
    
    "unknown_change": {
        "name": "🔵 Unknown Page Change",
        "description": "Page changed but doesn't match expected patterns",
        "url": URL,
        "content": """
<!DOCTYPE html>
<html>
<head><title>System Maintenance</title></head>
<body>
    <h1>System Maintenance</h1>
    <p>The room booking system is undergoing maintenance.</p>
    <p>Expected completion: 2 hours</p>
</body>
</html>
        """,
        "expected_action": "email",
        "expected_message": "UNEXPECTED CHANGE - Page changed but not recognized as booking system. Manual check required."
    }
}

def run_scenario(scenario_name):
    """Run a specific test scenario."""
    scenario = TEST_SCENARIOS[scenario_name]
    
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {scenario['name']}")
    print(f"📝 Description: {scenario['description']}")
    print(f"🔗 URL: {scenario['url']}")
    print(f"📄 Expected Action: {scenario['expected_action']}")
    print(f"💬 Expected Message: '{scenario['expected_message']}'")
    print(f"{'='*60}")
    
    # Mock the HTTP response
    mock_response = Mock()
    mock_response.text = scenario['content']
    mock_response.url = scenario['url']
    
    # Capture bot behavior
    email_sent = None
    print_called = None
    
    with patch('check_wrb2526.requests.get', return_value=mock_response):
        with patch('check_wrb2526.send_email') as mock_send_email:
            with patch('builtins.print') as mock_print:
                try:
                    check_page()
                    
                    if mock_send_email.called:
                        email_sent = mock_send_email.call_args[0][0]
                        print(f"📧 Bot Action: Email sent - '{email_sent}'")
                    elif mock_print.called:
                        print_called = mock_print.call_args[0][0]
                        print(f"📝 Bot Action: Printed - '{print_called}'")
                    else:
                        print("❓ Bot Action: No action detected")
                        
                except Exception as e:
                    print(f"❌ Bot crashed: {e}")
    
    # Verify results
    print(f"\n✅ VERIFICATION:")
    expected_action = scenario['expected_action']
    expected_message = scenario['expected_message']
    
    if expected_action == "email" and email_sent:
        if email_sent == expected_message:
            print(f"✅ PASS: Email sent correctly - '{email_sent}'")
        else:
            print(f"❌ FAIL: Wrong email message")
            print(f"   Expected: '{expected_message}'")
            print(f"   Actual:   '{email_sent}'")
    elif expected_action == "print" and print_called:
        if print_called == expected_message:
            print(f"✅ PASS: Printed correctly - '{print_called}'")
        else:
            print(f"❌ FAIL: Wrong print message")
            print(f"   Expected: '{expected_message}'")
            print(f"   Actual:   '{print_called}'")
    elif expected_action == "email" and not email_sent:
        print(f"❌ FAIL: Expected email but got print: '{print_called}'")
    elif expected_action == "print" and not print_called:
        print(f"❌ FAIL: Expected print but got email: '{email_sent}'")
    else:
        print(f"❓ UNKNOWN: Unexpected behavior")

def run_all_scenarios():
    """Run all test scenarios."""
    print("🧪 WARWICK BOOKING BOT - SCENARIO TESTING")
    print("🎯 Testing bot behavior across different page states")
    
    results = {}
    
    for scenario_name in TEST_SCENARIOS:
        run_scenario(scenario_name)
        results[scenario_name] = "completed"
    
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY: Tested {len(TEST_SCENARIOS)} scenarios")
    print(f"✅ All scenarios completed!")
    print(f"{'='*60}")

def interactive_testing():
    """Interactive scenario testing."""
    while True:
        print(f"\n🧪 SCENARIO TESTING MENU")
        print(f"{'='*40}")
        
        for i, (key, scenario) in enumerate(TEST_SCENARIOS.items(), 1):
            print(f"{i}. {scenario['name']}")
        
        print(f"{len(TEST_SCENARIOS) + 1}. Run all scenarios")
        print(f"{len(TEST_SCENARIOS) + 2}. Exit")
        
        try:
            choice = int(input(f"\nSelect scenario (1-{len(TEST_SCENARIOS) + 2}): "))
            
            if choice == len(TEST_SCENARIOS) + 2:
                print("👋 Goodbye!")
                break
            elif choice == len(TEST_SCENARIOS) + 1:
                run_all_scenarios()
            elif 1 <= choice <= len(TEST_SCENARIOS):
                scenario_name = list(TEST_SCENARIOS.keys())[choice - 1]
                run_scenario(scenario_name)
            else:
                print("❌ Invalid choice!")
                
        except (ValueError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    interactive_testing() 