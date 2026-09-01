import pytest
from app import app, students, users

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_login_success(client):
    response = client.post('/login', data={'username': 'admin', 'password': 'password123'}, follow_redirects=True)
    assert response.status_code == 200

def test_add_student(client):
    with client.session_transaction() as sess:
        sess['user'] = 'admin'
    response = client.post('/add', data={
        'name': 'Test Student',
        'roll': '999',
        'marks': '90',
        'attendance': 'Present'
    }, follow_redirects=True)
    assert response.status_code == 200