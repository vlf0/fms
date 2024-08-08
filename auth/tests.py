import os
os.environ['TESTING'] = 'TESTING'
import pytest
from fastapi.testclient import TestClient
from fms.main import app
from .auth_handler import AuthHandler
from fms.db_utils import session_manager
from .models import Base
from sqlalchemy import create_engine, Connection, Table
from sqlalchemy.orm import sessionmaker, Session


def test_user_register():
    db = session_manager.engine
    print(os.getenv('TESTING'))
    print(db.engine)
    client = TestClient(app)
    Base.metadata.create_all(bind=db)
    db.commit()

    response = client.post('/api/v1/register', json={
        'name': 'testuser',
        'password': 'testpassword',
        'email': 'test@mail.ru',
        'is_active': True,
        'is_stuff': False
    })
    Base.metadata.drop_all(bind=db)
    db.commit()
    assert response.status_code == 202
