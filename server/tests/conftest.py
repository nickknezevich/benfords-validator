import pytest
from ..models import User
from .. import create_app
import os

class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    BCRYPT_LOG_ROUNDS = 13

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    BCRYPT_LOG_ROUNDS = 4
    print(SQLALCHEMY_DATABASE_URI)


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    BCRYPT_LOG_ROUNDS = 4

app = create_app()

@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object(TestingConfig)
    with app.app_context():
        yield app  # testing happens here
        
@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object(TestingConfig)
    with app.app_context():
        yield app  # testing happens here