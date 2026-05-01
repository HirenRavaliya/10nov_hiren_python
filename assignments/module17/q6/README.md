# Q6 — URL Routing in Django REST Framework

## What It Does
Uses DRF's **DefaultRouter** to auto-register a `ModelViewSet`, automatically creating all 6 CRUD URL patterns from a single line of code.

## Endpoints (auto-generated)
| Method | URL | Action |
|--------|-----|--------|
| GET | `/q6/doctors/` | list |
| POST | `/q6/doctors/` | create |
| GET | `/q6/doctors/<id>/` | retrieve |
| PUT | `/q6/doctors/<id>/` | update |
| PATCH | `/q6/doctors/<id>/` | partial update |
| DELETE | `/q6/doctors/<id>/` | destroy |

## Key Concept
`DefaultRouter` + `ModelViewSet` is the most concise way to create a full CRUD API. One `router.register()` generates all routes automatically.
