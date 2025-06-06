from flask_restx import Namespace, Resource, fields
from api.models.orders import Order
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models.users import User
from api.utils import db


orders_namespace = Namespace('orders', description='Order related operations')

order_model = orders_namespace.model(
    'Order',
    {
        'id': fields.Integer(description='ID of the order'),
        'size': fields.String(required=True, description='Size of the order', enum=['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE']),
        'order_status': fields.String(required=True, description='Status of the order', enum=['PENDING', 'IN_TRANSIT', 'DELIVERED']),
        # 'flavour': fields.String(required=True, description='Flavour of the order'),
        # 'date_created': fields.DateTime(description='Date when the order was created'),
        # 'user_id': fields.Integer(required=True, description='ID of the user who placed the order')
    }
)

@orders_namespace.route('/orders')
class OrderGetCreate(Resource):
    @orders_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self):
        """
            Get all orders.
        """
        orders = Order.query.all()
        return orders ,HTTPStatus.OK

    @orders_namespace.expect(order_model)
    @orders_namespace.marshal_with(order_model)
    @jwt_required()
    def post(self):
        """
            Create a new order.
        """
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        data = orders_namespace.payload
    
        new_order = Order(
            size=data['size'],
            flavour=data['flavour'],
        )
        new_order.user = current_user.id
        new_order.save()
    
        return new_order, HTTPStatus.CREATED

@orders_namespace.route('/order/<int:order_id>')
class GetUpdateDelete(Resource):

    @orders_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self, order_id):
        """
            Get an order by ID.
        """
        order = Order.get_by_id(order_id)
        return order, HTTPStatus.OK

    def put(self, order_id):
        """
            Update an order by ID.
        """	
        pass

    def delete(self, order_id):
        """
            Delete an order by ID.
        """
        pass

@orders_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificUserOrder(Resource):

    def get(self, user_id, order_id):
        """
            Get an order by user ID and order ID.
        """
        pass

@orders_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):

    def get(self, user_id):
        """
            Get all orders for a specific user.
        """
        pass

@orders_namespace.route('/order/status/<int:order_id>')
class UpdateOrderStatus(Resource):
    def patch(self, order_id):
        """
            Update the status of an order by ID.
        """
        pass
    