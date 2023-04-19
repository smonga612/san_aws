import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation

# Intialize the Data Ingestion Configuration
@dataclass
class DataIngestionconfig:
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifacts','test.csv')
    raw_data_path:str=os.path.join('artifacts','raw.csv')
    master_data_path:str=os.path.join('data','gemstone.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionconfig()

    def initiate_data_ingestion(self):
        logging.info('Data Ingestion methods starts')
        try:
            df=pd.read_csv(self.ingestion_config.master_data_path)
            logging.info('Dataset read as pandas DataFrame')
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False)
            logging.info('Train test split')
            train_data,test_data=train_test_split(df,test_size=0.30,random_state=42)

            train_data.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_data.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('Ingestion of Data is Completed')

        
        except Exception as e:
            logging.info('Exception occured at Data Ingestion Stage')
            raise CustomException(e,sys)
        return(
            self.ingestion_config.train_data_path,
            self.ingestion_config.test_data_path
            
    
        )

## run Data Ingestion
if __name__=='__main__':
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initaite_data_transformation(train_data,test_data)
