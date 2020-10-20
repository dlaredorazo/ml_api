import sys
sys.path.append('.')

print('creando app')

import pathlib
from flask import Flask
from web_app.core import app_create

root_path = pathlib.Path(__file__).parent.absolute()
app, models = app_create.config_app(root_path)
app.config['ml_models'] = models

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=8080)
