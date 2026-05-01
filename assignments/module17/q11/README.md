# Q11 — RESTful API Design

## What It Does
Implements a proper RESTful API with standard HTTP verbs, resource URLs, and appropriate status codes using DRF's generic class-based views.

## Endpoints
| Method | URL | Status | Description |
|--------|-----|--------|-------------|
| GET | `/q11/doctors/` | 200 | List all doctors |
| POST | `/q11/doctors/` | 201 | Create doctor |
| GET | `/q11/doctors/<id>/` | 200/404 | Get doctor |
| PUT | `/q11/doctors/<id>/` | 200/400 | Full update |
| PATCH | `/q11/doctors/<id>/` | 200/400 | Partial update |
| DELETE | `/q11/doctors/<id>/` | 204 | Delete |

## REST Principles Demonstrated
- Resource-based URLs (nouns, not verbs)
- HTTP methods as actions
- Correct status codes
- JSON responses
- Stateless design
