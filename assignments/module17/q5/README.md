# Q5 — Views in Django REST Framework: Class-Based Views CRUD

## What It Does
Implements full CRUD for the Doctor model using **`APIView` class-based views** — the DRF pattern for organizing HTTP methods as class methods.

## Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/q5/` | HTML CRUD dashboard |
| GET | `/q5/edit/<id>/` | HTML edit form |
| GET | `/q5/doctors/` | List all doctors (JSON) |
| POST | `/q5/doctors/` | Create doctor |
| GET | `/q5/doctors/<id>/` | Get single doctor |
| PUT | `/q5/doctors/<id>/` | Full update |
| PATCH | `/q5/doctors/<id>/` | Partial update |
| DELETE | `/q5/doctors/<id>/` | Delete |

## Key Concept
`APIView` lets you define HTTP verbs as methods (`def get`, `def post`, etc.) inside a class, providing cleaner code than function-based views for complex APIs.

## Files
| File | Purpose |
|------|---------|
| `models.py` | Doctor model |
| `serializers.py` | DRF serializer |
| `views.py` | `DoctorListView`, `DoctorDetailView` (APIView) |
| `templates/q5/doctors.html` | CRUD frontend |
| `templates/q5/edit.html` | Edit form |
