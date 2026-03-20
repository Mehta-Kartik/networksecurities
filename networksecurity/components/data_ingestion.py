from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging import logger

#Configue file for data ingestion config

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import pymongo
import pandas as pd
import numpy as np
from typing import List
from sklearn.model_selection import train_test_split


from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,dataingestionconfig:DataIngestionConfig):
        try:
            self.dataingestionconfig=dataingestionconfig
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self):
        try:
            databasename=self.dataingestionconfig.database_name
            collection_name=self.dataingestionconfig.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[databasename][collection_name]

            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"],inplace=True,axis="columns")
            
            df.replace({"na":np.nan},inplace=True)

            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
        

    def export_data_to_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.dataingestionconfig.feature_store_file_path
            #creating the folder
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.dataingestionconfig.train_test_split_ratio)

            logger.info("Performed train test split on the dataframe")
            logger.info("Exited split_data_as_train_test method of Data_Ingestion class")

            dir_path=os.path.dirname(self.dataingestionconfig.train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            dir_path=os.path.dirname(self.dataingestionconfig.test_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logger.info(f"Exporting train and test file path")

            train_set.to_csv(
                self.dataingestionconfig.train_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.dataingestionconfig.test_file_path, index=False, header=True
            )

            logger.info(f"Exporting train and test file path")
        except Exception as e:
            NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_to_feature_store(dataframe)

            self.split_data_as_train_test(dataframe=dataframe)

            dataingestionartifact=DataIngestionArtifact(self.dataingestionconfig.train_file_path,self.dataingestionconfig.test_file_path)

            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)