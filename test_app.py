import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_student(client):
    response = client.post('/add', data={'name': 'Test Student', 'roll': '999'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Student' in response.data

def test_update_marks_and_grade(client):
    response = client.post('/update_marks/1', data={'marks': '90'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'A+' in response.data