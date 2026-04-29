import requests
import os
import sys
import pandas as pd
from src.logging import logging
from src.exception import WeatherException
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class WeatherAPIIngestion:
    def __init__(self, city: str = "London"):
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.city = city
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def fetch_live_weather(self, city: str = None):
        """Fetches current weather data from OpenWeatherMap."""
        try:
            if not self.api_key:
                logging.warning("WEATHER_API_KEY missing in .env. Cannot fetch real weather.")
                return None

            search_city = city if city else self.city
            params = {
                "q": search_city,
                "appid": self.api_key,
                "units": "metric"
            }

            response = requests.get(self.base_url, params=params)
            data = response.json()

            if response.status_code == 200:
                weather_data = {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"],
                    "pressure": data["main"]["pressure"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"]
                }
                logging.info(f"Successfully fetched live weather for {search_city}")
                return weather_data
            else:
                logging.error(f"API Error: {data.get('message')}")
                return None

        except Exception as e:
            raise WeatherException(e, sys)

    def fetch_5day_forecast(self, city: str = None):
        """Fetches 5-day weather forecast from OpenWeatherMap."""
        try:
            if not self.api_key:
                return None

            search_city = city if city else self.city
            forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
            params = {
                "q": search_city,
                "appid": self.api_key,
                "units": "metric"
            }

            response = requests.get(forecast_url, params=params)
            data = response.json()

            if response.status_code == 200:
                forecast_list = []
                # API returns data every 3 hours. We pick one per day (at 12:00 PM if available)
                for item in data['list']:
                    if "12:00:00" in item['dt_txt']:
                        forecast_list.append({
                            "date": item['dt_txt'].split(" ")[0],
                            "temp": item['main']['temp'],
                            "description": item['weather'][0]['description'],
                            "icon": item['weather'][0]['icon']
                        })
                
                # Fallback: if no 12:00:00 found, just take every 8th item (24 hours apart)
                if not forecast_list:
                    forecast_list = [{
                        "date": item['dt_txt'].split(" ")[0],
                        "temp": item['main']['temp'],
                        "description": item['weather'][0]['description'],
                        "icon": item['weather'][0]['icon']
                    } for item in data['list'][::8]]

                return forecast_list[:5]
            else:
                return None

        except Exception as e:
            raise WeatherException(e, sys)

if __name__ == "__main__":
    obj = WeatherAPIIngestion()
    print("Live Weather:", obj.fetch_live_weather("London"))
    print("5-Day Forecast:", obj.fetch_5day_forecast("London"))
