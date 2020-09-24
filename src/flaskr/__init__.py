import os

from flask import Flask
UPLOAD_FOLDER = 'tempfiles'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        UPLOAD_FOLDER= UPLOAD_FOLDER,
        MAX_CONTENT_LENGTH=8 * 1024 * 1024
    )


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    try:
        os.makedirs(app.config["UPLOAD_FOLDER"])
    except OSError:
        pass

    from . import ajax
    app.register_blueprint(ajax.bp)

    from . import api
    app.register_blueprint(api.bp)
    
    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')

    return app
