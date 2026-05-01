# Q15 — Google Maps Geocoding API

## What It Does
Converts a text address into geographic coordinates (latitude/longitude) using the Google Maps Geocoding API, with optional map preview.

## Endpoint
```
GET /q15/?address=Taj+Mahal+Agra
```

## Setup
1. Enable Geocoding API at https://console.cloud.google.com
2. Copy API key
3. Add to `.env`:
```
GOOGLE_MAPS_API_KEY=your_key_here
```

## API Called
```
GET https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={key}
```

## Response Data
- Formatted address
- Latitude & Longitude
- Place ID
- Location types
