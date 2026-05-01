# Q8 — Settings Configuration: SQLite Database

## What It Does
Demonstrates Django's database settings configuration using SQLite, displaying the database path, size, and all stored doctor records.

## Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/q8/` | HTML page showing DB info + records |
| GET | `/q8/doctors/` | JSON list of doctors |
| GET | `/q8/doctors/<id>/` | JSON single doctor |

## Database Config (settings.py)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## Key Concept
Django uses `db.sqlite3` by default — no extra setup needed. The ORM handles schema creation via migrations.
