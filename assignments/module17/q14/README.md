# Q14 — OpenWeatherMap API Integration

## What It Does
Fetches current weather data for any city using the OpenWeatherMap API and displays temperature, humidity, wind speed, pressure, and weather icon.

## Endpoint
```
GET /q14/?city=Mumbai
```

## Setup
1. Register at https://openweathermap.org/api
2. Copy your API key
3. Add to `.env`:
```
OPENWEATHERMAP_API_KEY=your_key_here
```

## API Called
```
GET https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric
```

## Data Displayed
- Temperature (°C), Feels Like
- Humidity, Pressure
- Wind Speed
- Weather description + icon
