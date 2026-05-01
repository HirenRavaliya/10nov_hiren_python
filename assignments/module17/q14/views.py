import requests
from django.shortcuts import render
from django.conf import settings

def weather(request):
    weather_data = None
    error = None
    city = request.GET.get('city', '')
    if city:
        api_key = settings.OPENWEATHERMAP_API_KEY
        if not api_key or api_key == 'your_openweathermap_api_key_here':
            error = 'OpenWeatherMap API key not configured. Add OPENWEATHERMAP_API_KEY to .env'
        else:
            try:
                url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    weather_data = {
                        'city': data['name'],
                        'country': data['sys']['country'],
                        'temp': data['main']['temp'],
                        'feels_like': data['main']['feels_like'],
                        'humidity': data['main']['humidity'],
                        'pressure': data['main']['pressure'],
                        'description': data['weather'][0]['description'].capitalize(),
                        'icon': data['weather'][0]['icon'],
                        'wind_speed': data['wind']['speed'],
                        'visibility': data.get('visibility', 0) // 1000,
                    }
                elif resp.status_code == 404:
                    error = f'City "{city}" not found. Try another city name.'
                else:
                    error = f'API error: {resp.status_code} — {resp.json().get("message","Unknown error")}'
            except Exception as e:
                error = f'Request failed: {e}'
    return render(request, 'q14/weather.html', {
        'weather': weather_data, 'error': error, 'city': city
    })
