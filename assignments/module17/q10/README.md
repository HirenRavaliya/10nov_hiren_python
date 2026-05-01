# Q10 — Social Authentication, Email & OTP (Placeholder)

## Status
**Implementation left blank** — requires live Google OAuth2 credentials and a Twilio account.

## What It Would Do
1. Allow users to log in with Google via `django-allauth`
2. After Google login, generate a 6-digit OTP
3. Send OTP to the user's phone via Twilio SMS
4. Verify OTP before granting access

## Required .env Keys
```
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+1234567890
```

## Packages
```bash
pip install django-allauth twilio
```

## Add Credentials
1. Create app at https://console.cloud.google.com
2. Set redirect URI: `http://localhost:8000/accounts/google/login/callback/`
3. Add Social Application in Django Admin
