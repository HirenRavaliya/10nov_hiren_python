# Q2 — Requirements for Web Development Projects

## What It Does
Displays an interactive setup guide showing all the packages needed for this Django project and step-by-step commands to initialize a Django project from scratch.

## Endpoint
```
GET /q2/
```

## Packages Covered
- `django` — Core web framework
- `djangorestframework` — DRF for building REST APIs
- `requests` — HTTP client for external API calls
- `python-dotenv` — Load secrets from `.env`
- `sendgrid`, `twilio` — Email and SMS APIs
- `stripe` — Payment integration
- `django-allauth` — Social authentication

## Files
| File | Purpose |
|------|---------|
| `views.py` | Renders setup steps and package list |
| `urls.py` | Routes `/q2/` |
| `templates/q2/setup.html` | Interactive setup guide page |

## Run
```bash
python manage.py runserver
# Visit: http://127.0.0.1:8000/q2/
```
