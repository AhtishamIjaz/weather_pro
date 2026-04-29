import os
import sys
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.metrics import mean_squared_error, r2_score
from src.logging import logging
from src.exception import WeatherException
from src.entity.config_entity import ModelEvaluationConfig
from src.utils.common import save_json, load_bin
from pathlib import Path
from urllib.parse import urlparse

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        r2 = r2_score(actual, pred)
        return rmse, r2

    def log_into_mlflow(self):
        try:
            test_df = pd.read_csv(self.config.test_data_path)
            model = load_bin(self.config.model_path)

            X_test, y_test = test_df.iloc[:, :-1], test_df.iloc[:, -1]

            mlflow.set_registry_uri(self.config.mlflow_uri)
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            with mlflow.start_run():
                predicted_qualities = model.predict(X_test)
                (rmse, r2) = self.eval_metrics(y_test, predicted_qualities)

                # Saving metrics as local json
                scores = {"rmse": rmse, "r2": r2}
                save_json(path=Path(self.config.metric_file_name), data=scores)

                mlflow.log_params(self.config.all_params.RandomForestRegressor)
                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)

                # Model registry does not work with local folder
                if tracking_url_type_store != "file":
                    mlflow.sklearn.log_model(model, "model", registered_model_name="WeatherModel")
                else:
                    mlflow.sklearn.log_model(model, "model")

        except Exception as e:
            raise WeatherException(e, sys)
