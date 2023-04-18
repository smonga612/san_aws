import os
import sys
import pandas as pd
import numpy as np
from src.utils import save_object

from src.logger import logging
from src.exception import CustomException

from sklearn.impute import SimpleImputer ##handling missing values
from sklearn.preprocessing import StandardScaler ## Handling Feature Scaling
from sklearn.preprocessing import OrdinalEncoder ## Ordinal Encoding
## import piplines
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    
    def get_data_transformation_object(self):
        try:
            logging.info("Data Transformation Initiated")

            #define the custom ranking for each ordinal variables
            cut_cat=['Fair','Good','Very Good','Premium','Ideal']
            clarity_cat=['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']
            color_cat=['D','E','F','G','H','I','J']

            #define which columns should be ordinal encoded and which should be scaled
            categorical_cols=['cut','color','clarity']
            numerical_cols=['carat','depth','table','x','y','z']

            logging.info('Pipeline Initiated')

            #numerical Pipeline
            num_pipeline=Pipeline(
            steps=[
            ('imputer',SimpleImputer(strategy='median')),
            ('scaler',StandardScaler())
                

                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('ordinal_encoder',OrdinalEncoder(categories=[cut_cat,color_cat,clarity_cat])),
                ('scaler',StandardScaler())
                ]
             )

            preprocessor=ColumnTransformer([
                ('num_pipeline',num_pipeline,numerical_cols),
                ('cat_pipeline',cat_pipeline,categorical_cols)

                ])
            logging.info('Pipeline Completed')
            return preprocessor
     

        except Exception as e:
            logging.info("Error in DataTransformation")
            raise CustomException(e,sys)
        
    def initaite_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info('Read train and test data completed')
            logging.info(f'Train Dataframe Head : \n {train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head : \n {test_df.head().to_string()}')

            logging.info('Obtaining preprocessing object')
            preprocessing_obj=self.get_data_transformation_object()
            
            target_column_name='price'
            drop_columns=[target_column_name,'id']

            input_feature_train_df=train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info("Applying preprocessing object on training and testing datasets")

            ## Transformating using preprocessor obj
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.fit_transform(input_feature_test_df)

            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]
            logging.info("Before save_object")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )      
            logging.info('preprocessor pickle file saved') 
              
             

        except Exception as e:
            logging.info("Exception occured in the initiate  datatransformation")
        
        return(train_arr,test_arr,self.data_transformation_config.preprocessor_obj_file_path)
        
