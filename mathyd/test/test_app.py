import pytest

from mathyd import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_assignments_none(client):
    resp = client.get('/assignments')
    assert resp.status_code == 200
    assert resp.json is not None
    assert 'data' in resp.json
    assert 'assignments' in resp.json['data']
    assert resp.json['data']['assignments'] == []


def test_assignment_post(client):
    resp = client.post('/assignment', json={
        'title': 'assignment title'
    })
    assert resp.status_code == 200
    assert resp.json is not None
    assert 'data' in resp.json
    assert 'assignment_id' in resp.json['data']
    assert resp.json['data']['assignment_id'] == 1
    
    resp = client.get('/assignment/1')
    assert resp.status_code == 200
    assert resp.json is not None
    assert 'data' in resp.json
    assert 'assignment' in resp.json['data']
    assert resp.json['data']['assignment']['title'] == 'assignment title'


def test_assignment_post_no_data(client):
    resp = client.post('/assignment')
    assert resp.status_code == 400
    assert resp.json is not None
    assert 'msg' in resp.json
    assert resp.json['msg'] == 'invalid or missing assignment data'


def test_assignment_post_invalid_json(client):
    resp = client.post('/assignment', data={ "title": "assignment" })
    assert resp.status_code == 400
    assert resp.json is not None
    assert 'msg' in resp.json
    assert resp.json['msg'] == 'invalid or missing assignment data'