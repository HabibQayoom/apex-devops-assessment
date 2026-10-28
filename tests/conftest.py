import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture()
def client():
    app = create_app("sqlite://")  # fresh in-memory database for every test
    with TestClient(app) as c:
        yield c
