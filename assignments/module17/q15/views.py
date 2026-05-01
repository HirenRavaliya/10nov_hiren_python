import requests
from django.shortcuts import render
from django.conf import settings

def geocode(request):
    result = None
    error = None
    address = request.GET.get('address', '')
    if address:
        api_key = settings.GOOGLE_MAPS_API_KEY
        if not api_key or api_key == 'your_google_maps_api_key_here':
            error = 'Google Maps API key not configured. Add GOOGLE_MAPS_API_KEY to .env'
        else:
            try:
                url = f'https://maps.googleapis.com/maps/api/geocode/json?address={requests.utils.quote(address)}&key={api_key}'
                resp = requests.get(url, timeout=10)
                data = resp.json()
                if data['status'] == 'OK':
                    loc = data['results'][0]
                    result = {
                        'formatted_address': loc['formatted_address'],
                        'lat': loc['geometry']['location']['lat'],
                        'lng': loc['geometry']['location']['lng'],
                        'place_id': loc['place_id'],
                        'types': ', '.join(loc.get('types', [])),
                    }
                else:
                    error = f'Geocoding failed: {data["status"]} — {data.get("error_message","")}'
            except Exception as e:
                error = f'Request failed: {e}'
    return render(request, 'q15/geocode.html', {
        'result': result, 'error': error, 'address': address,
        'api_key': settings.GOOGLE_MAPS_API_KEY,
    })
