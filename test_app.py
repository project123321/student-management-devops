import unittest
from app import app

class TestStudentManagementSystem(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_user_registration_and_login(self):
        # Register
        reg_response = self.client.post('/register', data={'username': 'teststudent', 'password': 'password123'}, follow_redirects=True)
        self.assertIn(b"Registration successful", reg_response.data)

        # Login
        login_response = self.client.post('/login', data={'username': 'teststudent', 'password': 'password123'}, follow_redirects=True)
        self.assertIn(b"Mark Attendance", login_response.data)

    def test_mark_attendance(self):
        # Login first
        self.client.post('/login', data={'username': 'admin', 'password': 'admin123'})
        
        # Mark attendance
        att_response = self.client.post('/mark-attendance', data={
            'student_name': 'Anish Kumar',
            'roll_no': '103',
            'date': '2026-08-30',
            'status': 'Present'
        }, follow_redirects=True)
        
        self.assertIn(b"Anish Kumar", att_response.data)

if __name__ == "__main__":
    unittest.main()