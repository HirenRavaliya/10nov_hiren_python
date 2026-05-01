# Q13 — Authentication & Authorization: Token-Based Auth

## What It Does
Implements DRF `TokenAuthentication` — users must provide a Bearer token to access write endpoints. Read endpoints remain public.

## Endpoints
| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| GET | `/q13/` | None | HTML auth UI + token form |
| POST | `/q13/token/` | None | Get token (POST username+password) |
| GET | `/q13/public/doctors/` | None | Public doctor list |
| GET | `/q13/doctors/` | None | Doctor list |
| POST | `/q13/doctors/` | ✅ Token | Create doctor |
| PUT/PATCH/DELETE | `/q13/doctors/<id>/` | ✅ Token | Modify/delete |

## Usage
```bash
# Get token
curl -X POST http://localhost:8000/q13/token/ \
  -d '{"username":"admin","password":"yourpass"}'

# Use token
curl http://localhost:8000/q13/doctors/ \
  -H "Authorization: Token <your_token>"
```

## Setup
```bash
python manage.py createsuperuser
# Then login at /q13/
```
