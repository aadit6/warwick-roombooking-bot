# Warwick WRB 25/26 Availability Checker

Automated bot that monitors the Warwick University Web Room Booking System and sends email notifications when it becomes available for 25/26.

Why - the University/SU doesn't notify societies when the WRB system becomes available and popular rooms (such as the Oculus) get booked weeks in advance so this gives an advantage

## Features

- ✅ **24/7 Monitoring** - Runs every 15 minutes via GitHub Actions
- ✅ **Smart Detection** - Recognizes different page states (unavailable, login redirect, booking form)
- ✅ **Email Alerts** - Instant notifications when the system goes live
- ✅ **Year Validation** - Distinguishes between 2024/25 and 2025/26 systems
- ✅ **Comprehensive Testing** - Full test suite with 15 unit tests and 7 scenarios

## Quick Start

### 1. Setup Environment
```bash
# Copy example environment file
cp env.example .env

# Edit with your Gmail credentials
nano .env
```

### 2. Configure Gmail App Password
1. Enable 2-factor authentication on Gmail
2. Generate App Password: Google Account → Security → App passwords
3. Use format: `ABCDEFGHIJKLMNOP` (remove spaces from `ABCD EFGH IJKL MNOP`)

### 3. Test Locally
```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Test the bot
uv run python check_wrb2526.py

# Run test suite
uv run python -m unittest tests.test_check_wrb2526 -v
```

### 4. Deploy to GitHub Actions
1. Fork this repository
2. Add these GitHub Secrets:
   - `EMAIL_USER`: Your Gmail address
   - `EMAIL_PASS`: Your Gmail App Password
   - `TO_EMAIL`: Notification recipient email
3. The bot will automatically start monitoring every 15 minutes

## How It Works

The bot monitors `https://abs.warwick.ac.uk/WRB2526/` and detects:

- 🔴 **"Application Unavailable"** → Continues monitoring
- 🟡 **Login redirect** → 📧 Sends "System is live!" email  
- 🟢 **Booking form** → 📧 Sends "Booking form detected!" email
- 🟠 **Wrong year (2024/25)** → 📧 Sends alert email
- 🔵 **Unknown change** → 📧 Sends alert email

## Testing & Development

For detailed testing instructions, development setup, and troubleshooting, see **[SETUP.md](SETUP.md)**.

## Status

- ✅ **Working**: Bot successfully monitors and detects page changes
- ✅ **Tested**: Comprehensive test suite validates all scenarios
- ✅ **Production Ready**: Automated monitoring via GitHub Actions
