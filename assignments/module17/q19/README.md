# Q19 — Email Sending API (SendGrid): Registration Confirmation

## What It Does
Registers a user and sends an HTML confirmation email via the **SendGrid API**.

## Endpoint
```
GET /q19/          — Registration form + user list
POST /q19/         — Register user + send email
```

## Setup
1. Register at https://sendgrid.com (free tier: 100 emails/day)
2. Create API key with "Mail Send" permission
3. Verify your sender email
4. Add to `.env`:
```
SENDGRID_API_KEY=SG.xxxx
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
```

## Without API Key
Registration still works and records are saved. Email sending is skipped with a warning.

## Files
| File | Purpose |
|------|---------|
| `models.py` | Registration model with `email_sent` field |
| `views.py` | Register view + `send_confirmation_email()` |
| `templates/q19/register.html` | Registration form + history |
