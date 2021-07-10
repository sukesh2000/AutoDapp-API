from flask import Flask
import json
import traceback  # error traceback
from flask import Flask
from werkzeug.exceptions import default_exceptions  # exception handling
from werkzeug.exceptions import HTTPException  # exception handling
from server.main.views import main_blueprint # blueprint1

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("server.config.DevelopmentConfig")
    app.register_blueprint(main_blueprint)

    @main_blueprint.errorhandler(Exception)
    def handle_error(e):
        if isinstance(e, HTTPException):
            status_code = 400
        else:
            status_code = 500
        message = str(e)
        print(traceback.format_exc())
        return json.dumps({'message':message, 'error_traceback':traceback.format_exc()}), status_code

    for ex in default_exceptions:
        app.register_error_handler(ex, handle_error)

    return app