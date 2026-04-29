import pytest
from src.components.api_ingestion import WeatherAPIIngestion

def test_api_ingestion_class():
    obj = WeatherAPIIngestion(city="London")
    assert obj.city == "London"
    assert obj.base_url == "http://api.openweathermap.org/data/2.5/weather"

# You can add more tests for model prediction or data processing here
