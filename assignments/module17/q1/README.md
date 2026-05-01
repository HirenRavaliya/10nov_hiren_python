# Q1 — Introduction to APIs: Random Joke Fetcher

## What It Does
Fetches a random joke from the **Official Joke API** (a free, public REST API) and displays it on a web page with a "reveal punchline" interaction.

## Endpoint
```
GET /q1/
```

## How It Works
1. A Django view (`views.fetch_joke`) sends a `GET` request to `https://official-joke-api.appspot.com/random_joke`
2. The JSON response contains `setup` and `punchline` fields
3. The template renders the setup, and the punchline is hidden until the user clicks "Reveal Punchline"

## API Used
- **Name**: Official Joke API  
- **URL**: https://official-joke-api.appspot.com  
- **Auth**: None (public API)  
- **No `.env` key required**

## Files
| File | Purpose |
|------|---------|
| `views.py` | Fetches joke from API, handles errors |
| `urls.py` | Routes `/q1/` to view |
| `templates/q1/joke.html` | Frontend page with punchline reveal |

## Run
```bash
python manage.py runserver
# Visit: http://127.0.0.1:8000/q1/
```
