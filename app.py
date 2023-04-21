import os
import sys
import glob

from flask import Flask,request,render_template
from pathlib import Path
#sys.path.append("/var/app/current/src/pipelines")

from src.pipelines.prediction_pipeline import PredictPipeline, CustomData
#from src.piplines.training_pipeline

app=Flask(__name__)

#results = [os.path.basename(f) for f in glob.glob(os.path.join("/var/app/current/src/pipelines", '*.*'))]
@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('form.html')
    else:
        carat=float(request.form.get('carat'))        
        depth=float(request.form.get('depth'))
        table=float(request.form.get('table'))
        x=float(request.form.get('x'))
        y=float(request.form.get('y'))
        z=float(request.form.get('z'))
        cut=request.form.get('cut')
        color=request.form.get('color')
        clarity=request.form.get('clarity')

        data=CustomData(carat,depth,table,cut,color,clarity)

    
    
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
    final_df=data.get_data_as_dataframe()
    predict_pipeline=PredictPipeline()
    pred=predict_pipeline.predict(final_df)
    result=round(pred[0],2)
    
    
    return render_template('result.html',final_result=result)

if __name__ =="__main__":
    app.run(host='0.0.0.0')



