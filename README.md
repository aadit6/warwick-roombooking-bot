# Warwick WRB 25/26 Availability Checker

This bot checks if the Warwick Web Room Booking (WRB) 25/26 page is live and sends an email when it becomes available.

## Local Setup

1. Install [uv](https://docs.astral.sh/uv/).
2. Clone this repo.
3. Copy `.env.example` → `.env` and fill in your details:
```
EMAIL_USER=you@gmail.com
EMAIL_PASS=your_app_password
TO_EMAIL=you@gmail.com
```
4. Run the checker:
```bash
uv run python check_wrb2526.py
```
