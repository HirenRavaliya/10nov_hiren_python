# Q3 — Serialization in Django REST Framework

## What It Does
Defines a `Doctor` model and serializes it using **DRF ModelSerializer**, exposing fields like `name`, `specialty`, `contact_email`, `contact_phone`, `hospital`, `city`, and `available`.

## Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/q3/` | HTML doctor listing page |
| GET | `/q3/doctors/` | JSON list of all doctors (DRF API) |
| GET | `/q3/doctors/<id>/` | JSON single doctor detail |

## Model Fields
```python
name, specialty, contact_email, contact_phone, hospital, city, available, created_at
```

## Key Concept
`ModelSerializer` auto-generates serializer fields from the model, including validation, making it the fastest way to expose models as API.

## Files
| File | Purpose |
|------|---------|
| `models.py` | Doctor model definition |
| `serializers.py` | DRF ModelSerializer |
| `views.py` | API views using serializer |
| `templates/q3/doctors.html` | Frontend card listing |

## Run
```bash
python manage.py makemigrations q3
python manage.py migrate
# Visit: http://127.0.0.1:8000/q3/doctors/
```
