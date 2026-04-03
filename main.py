from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging import logger
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys

from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from dotenv import load_dotenv
load_dotenv()

if __name__=="__main__":
    try:
        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config)
        logger.info("Entered the DataIngestionStage")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logger.info("Data Ingestion Completed now turn for Data Validation")
        print(dataingestionartifact)

        #Data Validation
        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logger.info("Data Validation initialized")
        data_validation_artifact=data_validation.initiate_data_validation()
        logger.info("Data Validation Completed")
        print(data_validation_artifact)

        #Data Transformation
        data_transformation_config=DataTransformationConfig(training_pipeline_config)
        data_transformation=DataTransformation(
            data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config
        )
        logger.info("Data Transformation Initiated")
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        logger.info("Data Transformation Completed")
        print(data_transformation_artifact)


        #Model Trainer
        logger.info("Model Training Started")
        model_trainer_config=ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        logger.info("Model Training completed")
    except Exception as e:
        raise NetworkSecurityException(e,sys)   