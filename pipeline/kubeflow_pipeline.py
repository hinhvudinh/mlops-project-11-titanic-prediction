import kfp
from kfp import dsl
from kfp.components import create_component_from_func
from kfp.compiler import Compiler

from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessing
from src.model_training import ModelTraining
from src.feature_store import RedisFeatureStore
from config.paths_config import RAW_DIR, TRAIN_PATH, TEST_PATH, BASE_IMAGE, KUBEFLOW_URL
from config.database_config import DB_CONFIG

# Component 1: Data Ingestion
def data_ingestion_op():
    """Ingest data from the source DB and store raw data."""
    data_ingestion = DataIngestion(DB_CONFIG, RAW_DIR)
    data_ingestion.run()

# Component 2: Data Processing
def data_processing_op():
    """Process raw data and write features to Redis feature store."""
    feature_store = RedisFeatureStore()
    processor = DataProcessing(TRAIN_PATH, TEST_PATH, feature_store)
    processor.run()

# Component 3: Model Training
def model_training_op():
    """Train a model using features from Redis and log experiment with MLflow."""
    feature_store = RedisFeatureStore()
    trainer = ModelTraining(feature_store)
    trainer.run()

# Wrap Python functions as Kubeflow components
data_ingestion_component = create_component_from_func(data_ingestion_op, base_image=BASE_IMAGE)
data_processing_component = create_component_from_func(data_processing_op, base_image=BASE_IMAGE)
model_training_component = create_component_from_func(model_training_op, base_image=BASE_IMAGE)

@dsl.pipeline(
    name="Titanic Prediction Pipeline",
    description="An ML pipeline for Titanic survival prediction"
)
def titanic_pipeline():
    """Kubeflow pipeline: Ingest -> Process -> Train"""
    step_ingest = data_ingestion_component()
    step_process = data_processing_component().after(step_ingest)
    step_train = model_training_component().after(step_process)

if __name__ == "__main__":
    # Compile the pipeline to a YAML file
    Compiler().compile(
        pipeline_func=titanic_pipeline, 
        package_path="titanic_pipeline.yaml"
    )

    # Connect to the Kubeflow Pipelines UI/API
    client = kfp.Client(host=f"http://{KUBEFLOW_URL}/pipeline")
    # Launch a run of the pipeline
    client.create_run_from_pipeline_func(titanic_pipeline, arguments={})
