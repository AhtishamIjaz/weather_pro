import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from src.pipeline.predict_pipeline import CustomData, PredictionPipeline
from src.pipeline.train_pipeline import TrainingPipeline
from src.components.api_ingestion import WeatherAPIIngestion
from src.logging import logging

app = FastAPI()

# Setup templates
templates = Jinja2Templates(directory="templates")

class WeatherInput(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    pressure: float

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/weather_data")
async def get_weather_data(city: str = "London"):
    try:
        api_ingestion = WeatherAPIIngestion()
        
        # 1. Fetch current weather
        current_weather = api_ingestion.fetch_live_weather(city)
        if not current_weather:
            return {"error": "Could not fetch current weather"}

        # 2. Fetch 5-day forecast
        forecast = api_ingestion.fetch_5day_forecast(city)

        # 3. Get AI Prediction based on current weather
        data = CustomData(
            temperature=current_weather["temperature"],
            humidity=current_weather["humidity"],
            wind_speed=current_weather["wind_speed"],
            pressure=current_weather["pressure"]
        )
        final_df = data.get_data_as_dataframe()
        predict_pipeline = PredictionPipeline()
        prediction = predict_pipeline.predict(final_df)

        return {
            "current": current_weather,
            "forecast": forecast,
            "prediction": float(prediction[0])
        }

    except Exception as e:
        logging.error(f"Error in get_weather_data: {e}")
        return {"error": str(e)}

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.main()
        return {"message": "Training successful !!"}
    except Exception as e:
        return {"error": f"Error Occurred! {e}"}

@app.post("/predict")
async def predict_route(input_data: WeatherInput):
    try:
        data = CustomData(
            temperature=input_data.temperature,
            humidity=input_data.humidity,
            wind_speed=input_data.wind_speed,
            pressure=input_data.pressure
        )
        final_df = data.get_data_as_dataframe()
        predict_pipeline = PredictionPipeline()
        prediction = predict_pipeline.predict(final_df)

        return {"prediction": float(prediction[0])}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
