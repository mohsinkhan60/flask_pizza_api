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

order_status_model = orders_namespace.model(
    'OrderStatus',
    {
        'order_status': fields.String(required=True, description='Status of the order', enum=['PENDING', 'IN_TRANSIT', 'DELIVERED'])
    }
)

@orders_namespace.route('/orders')
class OrderGetCreate(Resource):
    @orders_namespace.marshal_with(order_model)
    @orders_namespace.doc(
        description='Get all orders From Here', 
    )
    @jwt_required()
    def get(self):
        """
            Get all orders.
        """
        orders = Order.query.all()
        return orders ,HTTPStatus.OK

    @orders_namespace.expect(order_model)
    @orders_namespace.marshal_with(order_model)
    @orders_namespace.doc(
        description='Create a new order',
    )
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
    @orders_namespace.doc(
        description='Retrieve an order by ID',
        params={'order_id': 'An ID for the given order'}
    )
    def get(self, order_id):
        """
            Get an order by ID.
        """
        order = Order.get_by_id(order_id)
        return order, HTTPStatus.OK

    @orders_namespace.expect(order_model)
    @orders_namespace.marshal_with(order_model)
    @orders_namespace.doc(
        description='Update an order given an order ID',
        params={'order_id': 'An ID for the given order'}
    )
    @jwt_required()
    def put(self, order_id):
        """
            Update an order by ID.
        """	
        order_to_update = Order.get_by_id(order_id)

        data = orders_namespace.payload

        order_to_update.quantity = data['quantity']
        order_to_update.size = data['size']
        order_to_update.flavour = data['flavour']

        db.session.commit()
        return order_to_update, HTTPStatus.OK

    @orders_namespace.marshal_with(order_model)
    @orders_namespace.doc(
        description='Delete an order by Order ID',
        params={'order_id': 'An ID for the given order'}
    )
    @jwt_required()
    def delete(self, order_id):
        """
            Delete an order by ID.
        """
        order_to_delete = Order.get_by_id(order_id)
        order_to_delete.delete()
        return order_to_delete, HTTPStatus.NO_CONTENT

@orders_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificUserOrder(Resource):
    @orders_namespace.marshal_with(order_model)
    @orders_namespace.doc(
        description='Get an order by user ID and order ID',
        params={
            'user_id': 'An ID for the user',
            'order_id': 'An ID for the order'
        }
    )
    @jwt_required()
    def get(self, user_id, order_id):
        """
            Get an order by user ID and order ID.
        """
        user = User.get_by_id(user_id)
        order=Order.query.filter_by(id=order_id).filter_by(user=user_id).first()
        return order, HTTPStatus.OK

@orders_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):

    @orders_namespace.marshal_with(order_model)
    @orders_namespace.doc(
        description='Get orders of a user given their user ID',
        params={'user_id': 'An ID for the user'}
    )
    @jwt_required()
    def get(self, user_id):
        """
            Get all orders for a specific user.
        """
        user = User.get_by_id(user_id)
        orders = user.orders
        return orders, HTTPStatus.OK


@orders_namespace.route('/order/status/<int:order_id>')
class UpdateOrderStatus(Resource):
    @orders_namespace.expect(order_status_model)
    @orders_namespace.marshal_with(order_model)
    @orders_namespace.doc(
        description='Update the status given an order ID',
        params={'order_id': 'An ID for the order'}
    )
    @jwt_required()
    def patch(self, order_id):
        """
            Update the status of an order by ID.
        """
        data = orders_namespace.payload
        order_to_update = Order.get_by_id(order_id)

        order_to_update.order_status = data['order_status']
    
        db.session.commit()
        return order_to_update, HTTPStatus.OK