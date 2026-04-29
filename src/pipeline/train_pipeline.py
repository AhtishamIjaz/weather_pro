from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.logging import logging
import sys
from src.exception import WeatherException

STAGE_NAME = "Training Pipeline"

class TrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            logging.info(">>>>>> STAGE: Data Ingestion STARTED <<<<<<")
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.initiate_data_ingestion()
            logging.info(">>>>>> STAGE: Data Ingestion COMPLETED <<<<<<\n\nx==========x")

            logging.info(">>>>>> STAGE: Data Transformation STARTED <<<<<<")
            data_transformation_config = config.get_data_transformation_config()
            data_transformation = DataTransformation(config=data_transformation_config)
            data_transformation.initiate_data_transformation()
            logging.info(">>>>>> STAGE: Data Transformation COMPLETED <<<<<<\n\nx==========x")

            logging.info(">>>>>> STAGE: Model Training STARTED <<<<<<")
            model_trainer_config = config.get_model_trainer_config()
            model_trainer = ModelTrainer(config=model_trainer_config)
            model_trainer.initiate_model_trainer()
            logging.info(">>>>>> STAGE: Model Training COMPLETED <<<<<<\n\nx==========x")

            logging.info(">>>>>> STAGE: Model Evaluation STARTED <<<<<<")
            model_evaluation_config = config.get_model_evaluation_config()
            model_evaluation = ModelEvaluation(config=model_evaluation_config)
            model_evaluation.log_into_mlflow()
            logging.info(">>>>>> STAGE: Model Evaluation COMPLETED <<<<<<\n\nx==========x")

        except Exception as e:
            raise WeatherException(e, sys)

if __name__ == '__main__':
    try:
        logging.info(f">>>>>> {STAGE_NAME} STARTED <<<<<<")
        obj = TrainingPipeline()
        obj.main()
        logging.info(f">>>>>> {STAGE_NAME} COMPLETED <<<<<<\n\nx==========x")
    except Exception as e:
        logging.exception(e)
        raise e
