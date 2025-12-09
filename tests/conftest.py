import pytest
from fastapi.testclient import TestClient
from app.app import app
from app.db.db import SessionLocal
from app.api import models


@pytest.fixture(scope="session", autouse=True)
def clear_db():
    # NOTE: this clears DB before running tests
    # alternatively, I could have created a separate test DB
    db = SessionLocal()
    try:
        db.query(models.Vehicle).delete()
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


@pytest.fixture(scope="module")
def client():
    return TestClient(app)
