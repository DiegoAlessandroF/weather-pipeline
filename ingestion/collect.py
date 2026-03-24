import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from ingestion.load import load_weather_metrics

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

CITIES = [
    "Rio de Janeiro,BR",
    "São Paulo,BR",
    "Belo Horizonte,BR",
    "Salvador,BR",
    "Curitiba,BR",
]

def collect_weather(city: str) -> dict:
    response = requests.get(BASE_URL, params={
        "q":      city,
        "appid":  API_KEY,
        "units":  "metric",
        "lang":   "pt_br",
    })
    response.raise_for_status()
    data = response.json()

    return {
        "city":         data["name"],
        "country":      data["sys"]["country"],
        "collected_at": datetime.utcnow().isoformat(),
        "temp":         data["main"]["temp"],
        "temp_min":     data["main"]["temp_min"],
        "temp_max":     data["main"]["temp_max"],
        "humidity":     data["main"]["humidity"],
        "pressure":     data["main"]["pressure"],
        "weather":      data["weather"][0]["description"],
        "wind_speed":   data["wind"]["speed"],
        "cloudiness":   data["clouds"]["all"],
    }

def save_locally(records: list):
    os.makedirs("data/raw", exist_ok=True)
    date_str = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    path = f"data/raw/weather_{date_str}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"Salvo em: {path}")

def run():
    print(f"Coletando dados - {datetime.utcnow().isoformat()}")
    records = []

    for city in CITIES:
        try:
            data = collect_weather(city)
            records.append(data)
            print(f"  ✓ {data['city']}: {data['temp']}°C - {data['weather']}")
        except Exception as e:
            print(f"  ✗ Erro em {city}: {e}")

    save_locally(records)
    load_weather_metrics(records)
    print(f"\nTotal coletado: {len(records)}/{len(CITIES)} cidades")

if __name__ == "__main__":
    run()