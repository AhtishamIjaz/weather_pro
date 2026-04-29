import os
import sys
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from src.logging import logging
from src.exception import WeatherException
from src.entity.config_entity import ModelTrainerConfig
from src.utils.common import save_bin
from pathlib import Path

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def initiate_model_trainer(self):
        try:
            train_df = pd.read_csv(self.config.train_data_path)
            test_df = pd.read_csv(self.config.test_data_path)

            logging.info("Splitting training and testing input data")
            
            # Assuming last column is target (from transformation)
            X_train, y_train = train_df.iloc[:, :-1], train_df.iloc[:, -1]
            X_test, y_test = test_df.iloc[:, :-1], test_df.iloc[:, -1]

            model = RandomForestRegressor(
                n_estimators=self.config.n_estimators,
                max_depth=self.config.max_depth,
                min_samples_split=self.config.min_samples_split,
                random_state=42
            )

            logging.info(f"Training model with params: {self.config}")
            model.fit(X_train, y_train)

            model_path = os.path.join(self.config.root_dir, self.config.model_name)
            save_bin(data=model, path=Path(model_path))
            
            logging.info(f"Model saved at: {model_path}")

        except Exception as e:
            raise WeatherException(e, sys)
