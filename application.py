from flask import Flask,request,render_template,jsonify
#from src.pipelines.prediction_pipeline  import CustomData,PredictPipeline
#from src.piplines.training_pipeline

application=Flask(__name__)


@application.route('/')
def home_page():
    return render_template('index.html')




@application.route('/predict',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('form.html')
    else:
        pass

    return render_template('result.html')

if __name__ =="__main__":
    application.run(host='0.0.0.0')