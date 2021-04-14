import os
import csv
from flask import Flask
from flask import Blueprint
bp = Blueprint('main', __name__, template_folder='templates')


def create_app(test_config=None):
    # create and configure the app
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_mapping(
        SECRET_KEY=''
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        application.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        application.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass

    import charter
    application.register_blueprint(charter.bp)
    application.add_url_rule('/', endpoint='home')

    return application

application = create_app()