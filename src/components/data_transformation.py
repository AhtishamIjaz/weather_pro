import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from pathlib import Path
from src.logging import logging
from src.exception import WeatherException
from src.entity.config_entity import DataTransformationConfig
from src.utils.common import save_bin

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def get_data_transformer_object(self):
        """Creates the preprocessing pipeline."""
        try:
            numerical_columns = ["temperature", "humidity", "wind_speed", "pressure"]
            
            num_pipeline = Pipeline(
                steps=[
                    ("scaler", StandardScaler())
                ]
            )

            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise WeatherException(e, sys)

    def initiate_data_transformation(self):
        """Perform data transformation and split."""
        try:
            df = pd.read_csv(self.config.data_path)
            logging.info("Read data for transformation.")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "target"
            numerical_columns = ["temperature", "humidity", "wind_speed", "pressure"]

            input_feature_df = df.drop(columns=[target_column_name, 'timestamp'], axis=1)
            target_feature_df = df[target_column_name]

            logging.info("Applying preprocessing object on training and testing dataframes.")

            # Splitting data
            X_train, X_test, y_train, y_test = train_test_split(
                input_feature_df, target_feature_df, test_size=0.2, random_state=42
            )

            # Fit and transform
            X_train_transformed = preprocessing_obj.fit_transform(X_train)
            X_test_transformed = preprocessing_obj.transform(X_test)

            # Combine transformed features with target
            train_arr = np.c_[X_train_transformed, np.array(y_train)]
            test_arr = np.c_[X_test_transformed, np.array(y_test)]

            # Save transformed data as CSV for Model Trainer
            train_df = pd.DataFrame(train_arr)
            test_df = pd.DataFrame(test_arr)

            train_path = os.path.join(self.config.root_dir, "train.csv")
            test_path = os.path.join(self.config.root_dir, "test.csv")

            train_df.to_csv(train_path, index=False)
            test_df.to_csv(test_path, index=False)

            # Save preprocessing object
            save_bin(data=preprocessing_obj, path=Path(self.config.preprocess_obj_file))

            logging.info("Saved preprocessing object and transformed data.")

            return train_path, test_path, self.config.preprocess_obj_file

        except Exception as e:
            raise WeatherException(e, sys)
