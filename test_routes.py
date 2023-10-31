import unittest
from app import app, db
from models import User

class BloglyTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and test database."""
        self.client = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testdb'  # Use a separate test database.
        app.config['TESTING'] = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up the test database."""
        with app.app_context():
            db.drop_all()

    def test_list_users(self):
        """Test the /users route."""
        # Add test data to the database
        user1 = User(first_name="Test", last_name="User1", image_url="test1.jpg")
        user2 = User(first_name="Test", last_name="User2", image_url="test2.jpg")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User1', response.data)
        self.assertIn(b'Test User2', response.data)

    def test_user_creation(self):
        """Test the /users/new route for user creation."""
        user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'image_url': 'johndoe.jpg'
        }

        response = self.client.post('/users/new', data=user_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    def test_user_detail(self):
        """Test the /users/[user-id] route for user details."""
        user = User(first_name="Test", last_name="User1", image_url="test1.jpg")
        db.session.add(user)
        db.session.commit()

        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User1', response.data)

    def test_user_edit(self):
        """Test the /users/[user-id]/edit route for user editing."""
        user = User(first_name="Test", last_name="User1", image_url="test1.jpg")
        db.session.add(user)
        db.session.commit()

        user_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'image_url': 'updated.jpg'
        }

        response = self.client.post('/users/1/edit', data=user_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated User', response.data)
        self.assertIn(b'updated.jpg', response.data)

if __name__ == '__main__':
    unittest.main()
