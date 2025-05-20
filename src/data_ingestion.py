import psycopg
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import os
from sklearn.model_selection import train_test_split
import sys
from config.database_config import DB_CONFIG
from config.paths_config import *

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, db_params, output_dir):
        self.db_params = db_params
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)
    
    def connect_to_db(self):
        try:
            conn = psycopg.connect(
                host = self.db_params["host"],
                port = self.db_params["port"],
                dbname = self.db_params["dbname"],
                user = self.db_params["user"],
                password = self.db_params["password"],

            )

            logger.info("Database connection established ....")
            return conn

        except Exception as e:
            logger.error(f"error while establishing connection")
            raise CustomException(str(e), sys)
        
    def extract_data(self):
        try:
            conn = self.connect_to_db()
            query = "SELECT * FROM public.titanic" # schema.table
            df = pd.read_sql_query(query, conn)
            conn.close()
            logger.info("Data extracted from DB")
            return df
        
        except Exception as e:
            logger.error(f"error while extracting data {e}")
            raise CustomException(str(e), sys)
    
    def save_data(self, df):
        try:
            train_df, test_df = train_test_split(df, test_size=0.2)
            train_df.to_csv(TRAIN_PATH, index=False)
            test_df.to_csv(TEST_PATH, index=False)

            logger.info("Data splitting and saving done")

        except Exception as e:
            logger.error(f"error while saving data {e}")
            raise CustomException(str(e), sys)
    
    def run(self):
        try:
            logger.info("Data Ingestion Pipeline started .........")
            df = self.extract_data()
            self.save_data(df)
            logger.info("End of data ingestion pipeline...")
        
        except Exception as e:
            logger.error(f"error while data ingestion pipeline {e}")
            raise CustomException(str(e), sys)

if __name__ == "__main__":
    data_ingestion = DataIngestion(DB_CONFIG, RAW_DIR)
    data_ingestion.run()
