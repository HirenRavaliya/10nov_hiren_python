# Q4 — Requests and Responses: POST to Add Doctor

## What It Does
Provides an HTML form that submits a POST request to add a new doctor record to the SQLite database. Also exposes a DRF-browsable API endpoint.

## Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/q4/` | HTML form + doctor list |
| GET | `/q4/doctors/` | JSON list of all doctors |
| POST | `/q4/doctors/` | Add a new doctor (JSON body) |

## POST Body Example
```json
{
  "name": "Rahul Mehta",
  "specialty": "Cardiologist",
  "contact_email": "rahul@apollo.com",
  "contact_phone": "+91 9876543210",
  "hospital": "Apollo Hospital",
  "city": "Mumbai",
  "available": true
}
```

## Files
| File | Purpose |
|------|---------|
| `models.py` | Doctor model |
| `serializers.py` | DRF serializer with validation |
| `views.py` | `GET/POST` API view + HTML form view |
| `templates/q4/doctor_form.html` | Frontend add-doctor form |
