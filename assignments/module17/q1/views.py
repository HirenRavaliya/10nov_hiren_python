import requests
from django.shortcuts import render


def fetch_joke(request):
    joke = None
    error = None
    try:
        response = requests.get(
            'https://official-joke-api.appspot.com/random_joke',
            timeout=5
        )
        data = response.json()
        joke = {'setup': data['setup'], 'punchline': data['punchline']}
    except Exception as e:
        error = f"Could not fetch joke: {e}"
    return render(request, 'q1/joke.html', {'joke': joke, 'error': error})
