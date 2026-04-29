from src.pipeline.train_pipeline import TrainingPipeline
from src.logging import logging

if __name__ == "__main__":
    try:
        logging.info("Starting the training process...")
        train = TrainingPipeline()
        train.main()
        logging.info("Training process completed successfully.")
    except Exception as e:
        logging.error(f"Training failed: {e}")
