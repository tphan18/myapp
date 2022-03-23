import os

import werkzeug
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:////db/app.db",
    )

    from eastridge.db import db_session, init_db

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.errorhandler(werkzeug.exceptions.BadRequest)
    def handle_bad_request(e):
        return {"error": [e.description]}, e.code

    init_db()

    from . import invoices

    app.register_blueprint(invoices.bp)

    return app
