import os
import logging
import time

from flask import (Flask, render_template)
from app.config import config

if not os.path.exists('./log/'):
    os.makedirs('./log/')

logging.basicConfig(filename='./log/app.log',
                    filemode="a+",
                    format="%(asctime)s %(levelname)s : %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.DEBUG)


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(config['development'])
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import page
    app.register_blueprint(page.bp)

    from . import res
    app.register_blueprint(res.bp)

    from . import exe
    app.register_blueprint(exe.bp)

    from . import hw
    app.register_blueprint(hw.bp)

    from . import statistics
    app.register_blueprint(statistics.bp)

    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('/page/404.html'), 404

    return app