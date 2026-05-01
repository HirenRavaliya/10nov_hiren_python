# Q18 — REST Countries API Integration

## What It Does
Displays details of any country (population, language, currency, capital, area, flag, timezone) using the free REST Countries API — **no API key required**.

## Endpoint
```
GET /q18/?country=India
```

## API Used
```
GET https://restcountries.com/v3.1/name/{country}
```
- Free, no authentication needed
- Returns JSON with extensive country metadata

## Data Displayed
- Flag image + emoji
- Official name, capital
- Population, area, region
- Language(s), currency, timezone
