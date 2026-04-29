import os
import sys
import pandas as pd
from src.exception import WeatherException
from src.utils.common import load_bin
from pathlib import Path

class PredictionPipeline:
    def __init__(self):
        self.model_path = Path("artifacts/model_trainer/model.pkl")
        self.preprocessor_path = Path("artifacts/data_transformation/preprocessor.pkl")

    def predict(self, features):
        try:
            model = load_bin(self.model_path)
            preprocessor = load_bin(self.preprocessor_path)

            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)

            return preds

        except Exception as e:
            raise WeatherException(e, sys)

class CustomData:
    def __init__(self, temperature: float, humidity: float, wind_speed: float, pressure: float):
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.pressure = pressure

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "temperature": [self.temperature],
                "humidity": [self.humidity],
                "wind_speed": [self.wind_speed],
                "pressure": [self.pressure],
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise WeatherException(e, sys)
