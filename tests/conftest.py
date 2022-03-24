"""Setup tests."""

import os
import tempfile

import pytest
from myapp import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "DATABASE_URI": "sqlite:///" + db_path,
        }
    )

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Test client for the app."""
    return app.test_client()
