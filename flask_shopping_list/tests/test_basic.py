import pytest
import tempfile

from app import app, db, Item
from flask import json
import os

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE']
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    app.testing = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_get(client):
    i1 = Item(name='eggs', quantity=12)
    db.session.add(i1)
    db.session.commit()
    rv = client.get('/items/')
    items = json.loads(rv.data)['items']
    assert len(items) == 1
    it = items[0]
    assert it['name'] == 'eggs'
    assert it['quantity'] == '12'
