import pytest
from app import app, db, Student


@pytest.fixture
def client():
    """Provides test client and performs auto-cleanup before and after tests."""
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            # Clean up before test runs
            Student.query.filter_by(id='999').delete()
            db.session.commit()

        yield client

        with app.app_context():
            # Clean up after test finishes
            Student.query.filter_by(id='999').delete()
            db.session.commit()


# ==========================================
# 3 TEST CASES
# ==========================================

# Test 1: Home page redirect check (follows the redirect to get 200 OK)
def test_home_page(client):
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200


# Test 2: Database Insert Test
def test_add_student(client):
    response = client.post(
        '/add_student',
        data={'id': '999', 'name': 'Test Student', 'email': 'test@example.com'},
        follow_redirects=True,
    )
    assert response.status_code == 200


# Test 3: View/Index Page Test (Matches your actual main route)
def test_view_students(client):
    # If your view route is named something else (e.g. '/' or '/index' or '/view'), 
    # use that route path here:
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200