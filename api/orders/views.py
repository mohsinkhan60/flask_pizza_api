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

@orders_namespace.route('/orders/<int:order_id>')
class OrderGetUpdateDelete(Resource):

    def get(self, order_id):
        pass

    def put(self, order_id):
        pass

    def delete(self, order_id):
        pass