# Developer Setup & Testing Guide

## Overview
Comprehensive guide for developing, testing, and debugging the Warwick Room Booking Bot. For basic usage, see [README.md](README.md).

## Quick Start

### 1. Environment Setup
```bash
# Copy the example environment file
cp env.example .env

# Edit .env with your email credentials
nano .env
```

### 2. Gmail Configuration
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. Use this App Password (not your regular password) in `.env`

### 3. Install Dependencies
```bash
# Using uv (recommended)
uv run python check_wrb2526.py

# Or install manually
pip install requests python-dotenv
```

### 4. Test the Bot
```bash
# Run comprehensive tests
uv run python -m unittest test_check_wrb2526 -v

# Run live test (safe - no emails sent)
uv run python test_live.py

# Run the actual bot
uv run python check_wrb2526.py
```

## Environment Variables

Create a `.env` file with these variables:

```bash
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-gmail-app-password
TO_EMAIL=recipient@example.com
```

## Bot Behavior

The bot checks the Warwick Room Booking URL and:

1. **"Application Unavailable"** → Prints "Still unavailable." (no email)
2. **Redirects to login** → Sends "Redirected to login (system live)" email
3. **Booking form detected** → Sends "Booking form detected" email
4. **Unknown change** → Prints warning to check manually

## GitHub Actions

The bot runs automatically every 15 minutes via GitHub Actions. Set these secrets in your repository:

- `EMAIL_USER`: Your Gmail address
- `EMAIL_PASS`: Your Gmail App Password  
- `TO_EMAIL`: Email address to receive notifications

## Testing

### Unit Tests (Mocked Email)
```bash
uv run python -m unittest tests.test_check_wrb2526 -v
```

### Integration Tests (Real Email Config)
```bash
uv run python -m unittest tests.test_real_email -v
```

### Real Email Test (Sends Actual Email)
```bash
ENABLE_REAL_EMAIL_TESTS=true uv run python -m unittest tests.test_real_email.TestRealEmailIntegration.test_real_email_sending -v
```

### Live Test (Safe - No Emails)
```bash
uv run python tests/test_live.py
```

### Manual Run
```bash
uv run python check_wrb2526.py
```

### Page Reading Verification
```bash
# Quick page summary
uv run python tests/page_summary.py

# Detailed page inspection
uv run python tests/inspect_page.py

# Full page content (verbose)
uv run python tests/inspect_detailed.py
```

### Scenario Testing Environment
```bash
# Test different page states (safe - no real emails)
uv run python tests/test_scenarios.py

# Test with real email capability
uv run python tests/test_with_real_email.py
```

The scenario testing includes:
- 🔴 **System Unavailable** (current state)
- 🟡 **Login Redirect** (system live, requires auth)
- 🟡 **Return URL** (alternative login scenario)
- 🟢 **Booking Form** (detected via text patterns)
- 🟠 **WRB 2024/25** (wrong year detection)
- 🔵 **Unknown Change** (sends alert email)

## Troubleshooting

### Common Issues

1. **"Still unavailable" every time**: This is normal! The bot is working correctly.
2. **SMTP Authentication Error**: Use Gmail App Password, not regular password
3. **Connection timeout**: Check internet connection and firewall settings

## Email Testing

### Quick Email Test
```bash
# Simple one-shot test
uv run python tests/test_email_simple.py
```

### Interactive Email Testing
```bash
# Full testing suite with menu options
uv run python tests/test_email.py
```

The interactive test provides options to:
1. **Single test email** - Send one test email
2. **Batch test** - Send 3 different test scenarios  
3. **Realistic simulation** - Send exactly what the bot would send
4. **Exit** - Quit the testing suite

### Manual Bot Trigger Test
To test email functionality by forcing the bot to send an email, temporarily modify the bot:

```python
# In check_wrb2526.py, temporarily change:
if CHECK_STRING in text:
    send_email("Test email - forced trigger")  # Add this line for testing
    print("Still unavailable.")
    return
```

**⚠️ Remember to revert this change after testing!**

## Support

- Check logs in GitHub Actions for automated runs
- Run `python test_live.py` to diagnose issues
- Verify email credentials with Gmail App Passwords 