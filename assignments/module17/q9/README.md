# Q9 — Project Setup: doctor_finder App

## What It Does
Sets up the `doctor_finder` Django app with models, serializers, and views — with search functionality by specialty and city.

## Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/q9/` | HTML Doctor Finder with filters |
| GET | `/q9/api/doctors/` | JSON API (supports `?search=`) |
| GET/POST | `/q9/api/doctors/` | List + Create |
| GET/PUT/DELETE | `/q9/api/doctors/<id>/` | Detail CRUD |

## Extra Features
- `SearchFilter` on `name`, `specialty`, `city`
- `latitude`/`longitude` fields for map integration (used in Q22)

## Files
| File | Purpose |
|------|---------|
| `models.py` | Doctor model with geo fields |
| `serializers.py` | DRF serializer |
| `views.py` | ViewSet + HTML search view |
| `templates/q9/finder.html` | Filterable doctor finder UI |
