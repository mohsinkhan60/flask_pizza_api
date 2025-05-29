from flask_restx import Namespace, Resource, fields

orders_namespace = Namespace('orders', description='Order related operations')


@orders_namespace.route('/')
class HomeOrders(Resource):
    def get(self):
        return {'message': 'Hello from Orders!'}, 200