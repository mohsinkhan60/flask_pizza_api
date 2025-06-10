import unittest
from .. import create_app
from api.config.config import config_dict
from api.utils import db
from werkzeug.security import generate_password_hash

class UserTestCase(unittest.TestCase):


   def setUp(self):
      self.app = create_app(config=config_dict['test'])
      self.app_context = self.app.app_context()
      self.app_context.push()
      self.client = self.app.test_client()
      db.create_all()

   def tearDown(self):
      db.drop_all()
      self.app_context.pop()
      self.app = None
      self.client = None

   def test_user_registration(self):
      data = {
         'username': 'testuser',
         'email': 'testuser@gmail.com',
         'password': 'testpassword'
      }
      response = self.client.post('/auth/signup', json=data)
      assert response.status_code == 201
