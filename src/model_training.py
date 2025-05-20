from src.logger import get_logger
from src.custom_exception import CustomException
import pandas as pd
from src.feature_store import RedisFeatureStore
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
import os
import pickle
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, feature_store:RedisFeatureStore, model_save_path="artifacts/model/"):
        self.feature_store = feature_store
        self.model_save_path = model_save_path
        self.model = None
        
        os.makedirs(self.model_save_path, exist_ok=True)
        logger.info("Model training initialized.....")

    def load_data_from_redis(self, entity_ids):
        try:
            logger.info("Extracting data from Redis")

            data = []

            for entity_id in entity_ids:
                features = self.feature_store.get_features(entity_id)
                if features:
                    data.append(features)
                else:
                    logger.warning("Feature not found")
            
            return data
        
        except Exception as e:
            logger.error(f"Error while loading data from redis {e}")
            raise CustomException(str(e))
    
    def prepare_data(self):
        try:
            entity_ids = self.feature_store.get_all_entity_ids()

            train_entity_ids, test_entity_ids = train_test_split(entity_ids, test_size=0.2, random_state=42)

            train_data = self.load_data_from_redis(train_entity_ids)
            test_data = self.load_data_from_redis(test_entity_ids)

            train_df = pd.DataFrame(train_data)
            test_df = pd.DataFrame(test_data)

            X_train = train_df.drop("Survived", axis=1)
            logger.info(X_train.columns)
            X_test = test_df.drop("Survived", axis=1)
            y_train = train_df["Survived"]
            y_test = test_df["Survived"]

            logger.info("Preparation for model training completed")

            return X_train, X_test, y_train, y_test
        
        except Exception as e:
            logger.error(f"Error while preparing data {e}")
            raise CustomException(str(e))
    
    def hyperparameter_tunning(self, X_train, y_train):
        try:
            param_distributions = {
                    'n_estimators': [100, 200, 300],
                    'max_depth': [10, 20, 30],
                    'min_samples_split': [2, 5],
                    'min_samples_leaf': [1, 2]
                }
            
            rf = RandomForestClassifier(random_state=42)
            random_search = RandomizedSearchCV(rf, param_distributions, n_iter=10, cv=3, scoring='accuracy', random_state=42)
            random_search.fit(X_train, y_train)

            logger.info(f"Best paramters : {random_search.best_params_}")

            return random_search.best_estimator_
        
        except Exception as e:
            logger.error(f"Error while preparing data {e}")
            raise CustomException(str(e))
    
    def train_and_evaluate(self, X_train, y_train, X_test, y_test):
        try:
            with mlflow.start_run(run_name="RandomForestTraining"):
                mlflow.log_param("model_type", "RandomForestClassifier")

                # Hyperparameters tunning
                best_rf = self.hyperparameter_tunning(X_train, y_train)

                # Log best params
                for param, value in best_rf.get_params().items():
                    mlflow.log_param(param, value)

                # Evaluate
                y_pred = best_rf.predict(X_test)

                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred)
                recall = recall_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred)

                mlflow.log_metric("accuracy", accuracy)
                mlflow.log_metric("precision", precision)
                mlflow.log_metric("recall", recall)
                mlflow.log_metric("f1", f1)

                logger.info(f"Accuracy is {accuracy}")

                # can save into model registry using mlflow, comet ML
                # self.save_model(best_rf)
                mlflow.sklearn.log_model(best_rf, "model")

                return accuracy
        
        except Exception as e:
            logger.error(f"Error while model training {e}")
            raise CustomException(str(e))
    
    def save_model(self , model):
        try:
            model_filename = f"{self.model_save_path}random_forest_model.pkl"

            with open(model_filename,'wb') as model_file:
                pickle.dump(model , model_file)

            logger.info(f"Model saved at {model_filename}")
        except Exception as e:
            logger.error(f"Error while model saving {e}")
            raise CustomException(str(e))

    def run(self):
        try:
            logger.info("Starting Model Training Pipleine....")
            
            # can use s3
            mlflow.set_tracking_uri("file:./mlruns")
            mlflow.set_experiment("TitanicPredictionExperiment")
            
            X_train , X_test , y_train, y_test = self.prepare_data()
            accuracy = self.train_and_evaluate(X_train , y_train, X_test , y_test)

            logger.info("End of Model Training pipeline...")

        except Exception as e:
            logger.error(f"Error while model training pipeline {e}")
            raise CustomException(str(e))

if __name__ == "__main__":
    feature_store = RedisFeatureStore()
    model_trainer = ModelTraining(feature_store)
    model_trainer.run()