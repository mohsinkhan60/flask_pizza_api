from flask_restx import Namespace, Resource, fields

orders_namespace = Namespace('orders', description='Order related operations')


@orders_namespace.route('/orders')
class OrderGetCreate(Resource):

    def get(self):
        """
            Get all orders.
        """
        pass

    def post(self):
        """
            Create a new order.
        """
        pass

@orders_namespace.route('/order/<int:order_id>')
class GetUpdateDelete(Resource):

    def get(self, order_id):
        """
            Get an order by ID.
        """
        pass

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
    