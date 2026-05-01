# Q22 — Google Maps API Integration: Doctor Locations

## What It Does
Displays doctor locations in a city on an interactive Google Map with custom markers and info windows. Supports filtering by city and adding new doctor locations.

## Endpoints
| URL | Description |
|-----|-------------|
| `/q22/` | Interactive map + doctor list + add form |
| `/q22/?city=Mumbai` | Filter doctors by city |
| `/q22/api/` | JSON API for doctor locations |
| `/q22/api/?city=Mumbai` | Filtered JSON API |

## Setup
1. Enable Maps JavaScript API + Geocoding API at https://console.cloud.google.com
2. Create API key
3. Add to `.env`:
```
GOOGLE_MAPS_API_KEY=your_key_here
```

## Without API Key
- Doctors are still stored and listed
- Map shows a placeholder message
- Use Q15 (Geocoder) to find lat/lng for addresses

## Adding Doctors
Use the form at the bottom of `/q22/` to add doctors with known coordinates.
**Tip:** Use Q15 to geocode addresses and get lat/lng.
