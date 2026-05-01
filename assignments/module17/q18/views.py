import requests
from django.shortcuts import render

def countries(request):
    country_data = None
    error = None
    country_name = request.GET.get('country', '')
    if country_name:
        try:
            resp = requests.get(
                f'https://restcountries.com/v3.1/name/{country_name}',
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()[0]
                currencies = data.get('currencies', {})
                curr_list = [f"{v.get('name','?')} ({v.get('symbol','?')})" for v in currencies.values()]
                languages = list(data.get('languages', {}).values())
                country_data = {
                    'name': data['name']['common'],
                    'official_name': data['name']['official'],
                    'capital': ', '.join(data.get('capital', ['—'])),
                    'population': f"{data.get('population', 0):,}",
                    'area': f"{data.get('area', 0):,.0f} km²",
                    'region': data.get('region', '—'),
                    'subregion': data.get('subregion', '—'),
                    'languages': ', '.join(languages) if languages else '—',
                    'currencies': ', '.join(curr_list) if curr_list else '—',
                    'flag': data.get('flags', {}).get('png', ''),
                    'flag_emoji': data.get('flag', ''),
                    'calling_code': '+' + str(data.get('idd', {}).get('root', '')).replace('+','') + ''.join(data.get('idd', {}).get('suffixes', [])),
                    'timezone': ', '.join(data.get('timezones', ['—'])[:2]),
                }
            elif resp.status_code == 404:
                error = f'Country "{country_name}" not found. Check the spelling.'
            else:
                error = f'API error: {resp.status_code}'
        except Exception as e:
            error = f'Request failed: {e}'
    return render(request, 'q18/countries.html', {
        'country': country_data, 'error': error, 'country_name': country_name
    })
