from flask import request, Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route("/")
def hello():
    # This could also be returning an index.html
    return """Hello World from Flask in a uWSGI Nginx Docker container with \
     Python 3.7 (from the example template), 
     try also: <a href="/users/">/users/</a>"""
