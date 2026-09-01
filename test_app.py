import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_redirect(client):
    response = client.get('/')
    assert response.status_code == 302

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_add_student(client):
    with client.session_transaction() as sess:
        sess['user'] = 'admin@example.com'
        
    response = client.post('/add_student', data={
        'student_id': '999',
        'name': 'Test Student',
        'email': 'teststudent@example.com',
        'phone': '+91 9876543210',
        'department': 'Computer Science',
        'course': 'B.E. CS',
        'admission_date': '2024-08-01'
    }, follow_redirects=True)
    
    assert response.status_code == 200