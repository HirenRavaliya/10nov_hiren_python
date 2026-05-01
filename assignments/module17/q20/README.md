# Q20 — SMS Sending API (Twilio): OTP on Registration

## What It Does
Sends a 6-digit OTP to the user's mobile number via Twilio SMS during registration, then verifies it before completing registration.

## Endpoint
```
GET/POST /q20/
```

## Flow
1. User enters phone number → POST sends OTP via Twilio
2. User enters received OTP → POST verifies against stored OTP
3. On success → registration complete

## Setup
1. Register at https://twilio.com (free trial available)
2. Get Account SID, Auth Token, and phone number
3. Add to `.env`:
```
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

## Without Twilio Config
Runs in **demo mode** — OTP is displayed on screen for testing without actual SMS sending.

## Files
| File | Purpose |
|------|---------|
| `models.py` | OTPRecord model |
| `views.py` | Send OTP + verify OTP logic |
| `templates/q20/otp.html` | Multi-step OTP UI |
