# Q12 — CRUD API: Create, Read, Update, Delete for Doctor Profiles

## What It Does
Full CRUD dashboard that lets users create, read, update, and delete doctor profiles via both an HTML UI and a DRF JSON API. Includes a custom `available` action endpoint.

## Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/q12/` | HTML CRUD dashboard |
| GET | `/q12/doctors/` | List all (JSON) |
| POST | `/q12/doctors/` | Create (JSON) |
| GET | `/q12/doctors/<id>/` | Retrieve (JSON) |
| PUT/PATCH | `/q12/doctors/<id>/` | Update (JSON) |
| DELETE | `/q12/doctors/<id>/` | Delete (JSON) |
| GET | `/q12/doctors/available/` | Only available doctors |

## Key Features
- Inline edit form (no page reload)
- Custom `@action` endpoint for filtering available doctors
- Delete confirmation prompt
