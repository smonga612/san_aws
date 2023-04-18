import os
import sys

from flask import Flask,request,render_template,jsonify
from pathlib import Path
#sys.path.append("/opt/python/current/application/san_aws_1/src/pipelines")
#from pipelines import DataTransformation
#from src.pipelines.prediction_pipeline import PredictPipeline
#from src.piplines.training_pipeline

application=Flask(__name__)


@application.route('/')
def home_page():
    return render_template('index.html',path=Path.cwd())

@application.route('/predict',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('form.html')
    else:
        '''
        data=CustomData(
            
            carat=float(request.form.get('carat')),
            depth=float(request.form.get('depth')),
            table=float(request.form.get('table')),
            x=float(request.form.get('x')),
            y=float(request.form.get('y')),
            z=float(request.form.get('z')),
            cut=request.form.get('cut'),
            color=request.form.get('color'),
            clarity=request.form.get('clarity')

            )
            '''
    '''    
    final_df=data.get_data_as_dataframe()
    predict_pipeline=PredictPipeline()
    pred=predict_pipeline.predict(final_df)
    result=round(pred[0],2)
    '''

    return render_template('result.html',final_result=10)

if __name__ =="__main__":
    application.run(host='0.0.0.0')



