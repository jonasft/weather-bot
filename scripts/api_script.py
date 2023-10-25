import requests
import sqlite3
from datetime import datetime


def fetch_data():
    url = (
        "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=60.10&lon=9.58"
    )
    headers = {"User-Agent": "Kiteable/0.1 (jonas.foyn@gmail.com)"}
    response = requests.get(url, headers=headers)
    data = response.json()

    wind_data = []
    for timeseries in data["properties"]["timeseries"]:
        timestamp = timeseries["time"]
        time = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        if 10 <= time.hour <= 20:
            wind_data.append(
                (
                    timestamp,
                    timeseries["data"]["instant"]["details"]["wind_speed"],
                    timeseries["data"]["instant"]["details"]["wind_from_direction"],
                )
            )


if __name__ == "__main__":
    data = fetch_data()
