import os
import sys
import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset
from src.logging import logging
from src.exception import WeatherException

class ModelMonitoring:
    def __init__(self, train_data_path: str, live_data_path: str):
        self.train_data_path = train_data_path
        self.live_data_path = live_data_path

    def generate_drift_report(self):
        """Generates a data drift report comparing training data vs new incoming data."""
        try:
            train_df = pd.read_csv(self.train_data_path)
            live_df = pd.read_csv(self.live_data_path)

            logging.info("Generating Data Drift Report using Evidently AI...")
            
            report = Report(metrics=[
                DataDriftPreset(),
            ])

            snapshot = report.run(reference_data=train_df, current_data=live_df)
            
            report_path = "reports/data_drift_report.html"
            os.makedirs("reports", exist_ok=True)
            snapshot.save_html(report_path)
            
            logging.info(f"Drift report saved at: {report_path}")
            return report_path

        except Exception as e:
            raise WeatherException(e, sys)

if __name__ == "__main__":
    # Example usage
    monitor = ModelMonitoring("artifacts/data_transformation/train.csv", "artifacts/data_transformation/test.csv")
    monitor.generate_drift_report()
