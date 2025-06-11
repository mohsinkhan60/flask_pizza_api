import unittest
from .. import create_app
from api.config.config import config_dict
from api.models.orders import Order
from api.utils import db
from flask_jwt_extended import create_access_token
from api.models.users import User
from werkzeug.security import generate_password_hash

class OrderTestCase(unittest.TestCase):
    def setUp(self):
       self.app = create_app(config=config_dict['test'])
       self.app_context = self.app.app_context()
       self.app_context.push()
       self.client = self.app.test_client()
       db.create_all()

       # Create a test user for authentication
       user = User(
           username='testuser',
           email='testuser@example.com',
           password_hash=generate_password_hash('testpassword')
       )
       db.session.add(user)
       db.session.commit()

    def tearDown(self):
       db.drop_all()
       self.app_context.pop()
       self.app = None
       self.client = None


    def test_get_all_orders(self):

        token=create_access_token(identity='testuser')

        headers={
            "Authorization":f"Bearer {token}"
        }

        response=self.client.get('/orders/orders',headers=headers)

        assert response.status_code == 200

        assert response.json == []


    def test_create_order(self):
        data={
            "size":"LARGE",
            "quantity":3,
            "flavour":"Test Flavour"
        }

        token=create_access_token(identity='testuser')

        headers={
            "Authorization":f"Bearer {token}"
        }


        response=self.client.post('/orders/orders',json=data,headers=headers)


        assert response.status_code == 201

        orders= Order.query.all()

        assert len(orders) == 1