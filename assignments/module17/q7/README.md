# Q7 — Pagination in Django REST Framework

## What It Does
Returns paginated results for a list of doctors using DRF's `PageNumberPagination`.

## Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/q7/` | HTML paginated UI (with page selector) |
| GET | `/q7/doctors/` | JSON API — 3 doctors per page |
| GET | `/q7/doctors/?page=2` | Navigate to page 2 |
| GET | `/q7/doctors/?page_size=5` | Override page size |

## JSON Response Structure
```json
{
  "count": 15,
  "next": "/q7/doctors/?page=2",
  "previous": null,
  "results": [...]
}
```

## Key Concept
`PageNumberPagination` with `page_size`, `page_size_query_param`, and `max_page_size` configured in a custom pagination class.
