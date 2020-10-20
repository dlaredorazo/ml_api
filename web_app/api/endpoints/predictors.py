from flask import jsonify, request, Blueprint
from flask import current_app as app
import pandas as pd
import random
import json
import traceback
from web_app.auxiliary import exceptions
from . import app_logger

bp = Blueprint('predictors', __name__, url_prefix='/api')

ports = set(['C', 'Q', 'S'])
sexs = set(['female', 'male'])
p_classs = set(['Class_1', 'Class_2', 'Class_3'])

types = {'Age':float, 'SibSp':int, 'Parch':int, 'Fare':float, 'C':int, 'Q':int, 'S':int, 'female':int, 'male':int, 'Class_1':int, 'Class_2':int, 'Class_3':int}


@bp.route("/predict/", methods=['POST'])
def predict():

    data = None
    models = app.config['ml_models']
    models_names = list(models.keys())

    if request.method == 'POST':

        #Load data
        try:
            data = request.get_json()
            transformed_data = data_transform(data)
        except Exception as e:
            app_logger.error("Unable to transform data")
            app_logger.error(traceback.format_exc())
            raise exceptions.DataError("Unable to transform data")

    #Make inference
    try:
        #This can be used for A/B testing once the kpi's have been defined
        selected_model = random.randint(0,len(models)-1)
        model = models[models_names[selected_model]]

        predictions = model.predict(transformed_data)
        results = predictions.tolist()
        app_logger.info("Inference with " + str(models_names[selected_model]))
    except Exception as e:
        app_logger.error("Unable to make inference")
        app_logger.error(traceback.format_exc())
        raise exceptions.InferenceError("Unable to make inference")

    return jsonify({'data':results})


@bp.route("/queryModels/")
def queryModels():

    models = [key for key in app.config['ml_models']]

    return jsonify({'Loaded models':models})


def data_transform(data):
    """Transform the incoming data in a format suitable for the ml model"""

    predict_df = pd.DataFrame(data)

    predict_df = predict_df.drop(['Name','Ticket','Cabin'], axis=1)

    #Need to find a way to apply the same transformation as with the training set (save the transformations to pickle)

    #Transform categorical into integer
    embark_dummies_titanic = pd.get_dummies(predict_df['Embarked'])
    sex_dummies_titanic = pd.get_dummies(predict_df['Sex'])
    pclass_dummies_titanic = pd.get_dummies(predict_df['Pclass'], prefix="Class")

    for col in ports - set(embark_dummies_titanic.columns):
        embark_dummies_titanic.loc[:, col] = 0

    for col in sexs - set(sex_dummies_titanic.columns):
        sex_dummies_titanic.loc[:, col] = 0

    for col in p_classs - set(pclass_dummies_titanic.columns):
        pclass_dummies_titanic.loc[:, col] = 0


    #Put data together
    training = predict_df.drop(['Embarked', 'Sex', 'Pclass'], axis=1)
    titanic = training.join([embark_dummies_titanic, sex_dummies_titanic, pclass_dummies_titanic])
    titanic = titanic.loc[:,['Age', 'SibSp', 'Parch', 'Fare', 'C', 'Q', 'S', 'female', 'male', 'Class_1', 'Class_2', 'Class_3']] #Rearrange columns to match training

    #Change datatypes
    for key in types:
        titanic[key] = titanic[key].astype(types[key])

    return titanic