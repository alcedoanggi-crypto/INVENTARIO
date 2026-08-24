import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models import User

@pytest.fixture
def app(tmp_path):
    os.environ["UPLOAD_FOLDER"] = str(tmp_path / "uploads")
    
    app = create_app("testing")
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_ENGINE_OPTIONS": {},
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test_secret_key"
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        admin_user = User(
            username="admin_test",
            email="admin@test.com",
            role="admin"
        )
        admin_user.set_password("admin123")
        db.session.add(admin_user)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """Cliente autenticado como el usuario administrador de pruebas."""
    client.post("/login", data={
        "username": "admin_test",
        "password": "admin123"
    }, follow_redirects=True)
    return client