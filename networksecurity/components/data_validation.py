from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging import logger
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
import os,sys

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
            self._schema_columns = [list(col.keys())[0] for col in self._schema_config["columns"]]
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        #Static method as it is going to be called only once no need to repeatedively call it
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def validate_no_of_column(self,df:pd.DataFrame)-> bool:
        try:
            number_of_columns=len(self._schema_columns)
            logger.info(f"Require number of columns={number_of_columns}")
            logger.info(f"DataFrames columns number {len(df.columns)}")
            if len(df.columns)==number_of_columns:
                return True
            else:
                return False 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_numerical_column(self,df:pd.DataFrame)->bool:
        try:
            for col in df.columns:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    logger.info(f"Non‑numeric column found: {col} (dtype={df[col].dtype})")
                    return False
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_data_drift(self,base_df:pd.DataFrame,cur_df:pd.DataFrame,threshold=0.05) -> bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=cur_df[column]
                is_sample_dist=ks_2samp(d1,d2)
                if threshold<=is_sample_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                
                report.update({
                    column:{
                        "p_value":float(is_sample_dist.pvalue),
                        "drift_status":is_found
                    }
                })
            drift_report_file_path=self.data_validation_config.drift_report_file_path
            #create the directory
            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)

            write_yaml_file(drift_report_file_path,report)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_data_validation(self,)->DataValidationConfig:
        try:
            train_file_path,test_file_path=self.data_ingestion_artifact.train_file_path,self.data_ingestion_artifact.test_file_path

            #read the data from both file
            train_df=DataValidation.read_data(train_file_path)
            test_df=DataValidation.read_data(test_file_path)

            #Validate number of columns
            status=self.validate_no_of_column(train_df)
            if not status:
                error_message=f"Train dataframe does not contain all columns \n"
            status=self.validate_no_of_column(test_df)
            if not status:
                error_message=f"Test dataframe does not contain all columns \n"
            
            status=self.validate_numerical_column(train_df)
            if not status:
                error_message=f"Train dataframe does not contain all Integer column  \n"
            status=self.validate_numerical_column(test_df)
            if not status:
                error_message=f"Test dataframe does not contain all Integer column \n"
            
            #lets check data drift
            status=self.detect_data_drift(base_df=train_df,cur_df=test_df)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True) 

            train_df.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True
            )           
            
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path,index=False,header=True
            )     

            data_validation_artifact=DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )      
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)