import json
import traceback
import io
import pickle
import copy
from git import Repo
from . import app_logger
from web_app.auxiliary import exceptions


def load_model(model_spec):
    """Given a model and its version, load it"""

    #models_repo = r"/Users/davidlaredorazo/Documents/Projects/Rappi Challenge/models_and_data"
    models_repo = r"/models_and_data"

    model = None

    #Try to open repository
    try:
        repo = Repo(models_repo)
    except Exception as e:
        app_logger.error('Could not open repository')
        app_logger.error(traceback.format_exc())
        raise exceptions.FileError('Could not open repository')

    #Attempt to load models
    try:
        if not model_spec['model_tag']:
            raise exceptions.UnspecifiedModel('Model not specified')

        if model_spec['model_version']:
            commit = repo.commit(model_spec['model_version'])

            target_file = commit.tree / ('models/deploy/' + model_spec['model_tag'] + '.pkl')

            print(target_file)

            with io.BytesIO(target_file.data_stream.read()) as f:
                model = pickle.load(f)
        else:
            model = pickle.load(open(models_repo + '/models/deploy/' + model_spec['model_tag'] + '.pkl', 'rb'))
    except Exception as e:
        app_logger.error('Could not load model')
        app_logger.error(traceback.format_exc())
        raise exceptions.UnspecifiedModel('Could not load model')

    return model


def load_ml_models(app_root):
    """Load all the models specified in the models_list"""

    models_list = None
    models = {}
    model = None
    print(app_root)

    try:

        app_logger.error("Loading models from")
        app_logger.error(app_root / 'models_list.json')

        with open(app_root / 'models_list.json', 'r') as fp:
            models_list = json.load(fp)

        app_logger.error(models_list)

    except Exception as e:

        app_logger.error("Could not open models list file.")
        app_logger.error(traceback.format_exc())
        print("Could not open models list file. Check app_log file")

    for key in models_list:

        model_spec = models_list[key]
        model = load_model(model_spec)
        models[model_spec['model_tag'] + '/' +
               (model_spec['model_version'] if model_spec['model_version'] else 'latest')] = copy.deepcopy(model)

    return models

