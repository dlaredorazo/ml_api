import logging
import traceback
import sys
from flask import Flask
from flask_cors import CORS
from flask import current_app as app
from web_app.auxiliary import exceptions, auxiliary
from web_app.api import api
from web_app.api.endpoints import predictors

import web_app.ml.load_models as load_ml

def config_app(app_root_path, test_config=None):

    # create and configure the web_app
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.config['app_root'] = app_root_path

    #Configure loggers

    #App logger
    app_logger = logging.getLogger('app_logger')
    app_logger.setLevel(logging.INFO)
    app_fh = logging.FileHandler(str(app_root_path) + '/LogFiles/web_app.log')
    app_formatter = logging.Formatter(fmt='%(levelname)s:%(threadName)s:%(asctime)s:%(filename)s:%(funcName)s:%(message)s',
                                    datefmt='%m/%d/%Y %H:%M:%S')
    app_fh.setFormatter(app_formatter)
    app_logger.addHandler(app_fh)

    #STDOUT/STDERR logger
    """
    root_logger = logging.getLogger('ROOT_LOGGER')
    root_logger.setLevel(logging.INFO)
    handler = logging.FileHandler(str(app_root_path) + '/LogFiles/web_app.log')
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    sys.stderr.write = auxiliary.write_to_log_error
    sys.stdout.write = auxiliary.write_to_log_info
    """

    #Load models
    try:
        models = load_ml.load_ml_models(app.config['app_root'])
        app_logger.info("Loaded the following ML models")
        app_logger.info(models)
    except Exception as e:
        app_logger.error("Could not initialize models")
        app_logger.error(traceback.format_exc())
        raise exceptions.InitializationError("Could not initialize models")

    app.register_blueprint(api.bp)
    app.register_blueprint(predictors.bp)

    return app, models