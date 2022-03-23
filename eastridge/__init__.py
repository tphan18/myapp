"""App module."""

import os

import werkzeug
from flask import Flask


def create_app(test_config=None):
    """Create and configure the app."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config.from_mapping(
            DATABASE_URI="sqlite:///" + os.path.join(basedir, "../db", "app.db"),
        )
    else:
        app.config.from_mapping(test_config)

    with app.app_context():
        from eastridge.db import db_session, init_db

        init_db()

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            db_session.remove()

    @app.errorhandler(werkzeug.exceptions.BadRequest)
    def handle_bad_request(e):
        return {"error": e.description}, e.code

    @app.errorhandler(404)
    def handle_not_found(e):
        return {"error": "Not found"}, 404

    from . import invoices

    app.register_blueprint(invoices.bp)

    return app
