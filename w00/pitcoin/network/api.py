from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from json import dumps
import json
from flask import jsonify
from pitcoin.network.pending_pool import Storage
from pitcoin.settings import *


mempool = Storage()
app = Flask(__name__)
api = Api(app)


class Transaction(Resource):
    def post(self):
        response = app.response_class(
            response=json.dumps({"result": mempool.add_serialized_transaction_to_mempool(request.data)}),
            status=200,
            mimetype='application/json'
        )
        return response


class Transactions(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('amount', type=int)
        args = parser.parse_args()

        if args['amount'] == 3:
            list = mempool.get_three_first_transactions()
        else:
            list = mempool.get_all_transactions()
        response = app.response_class(
            response=json.dumps([tx.__dict__ for tx in list]),
            status=200,
            mimetype='application/json'
        )
        return response

    def delete(self):
        return mempool.delete_all_transactions_from_mempool()


api.add_resource(Transaction, '/transaction/new')
api.add_resource(Transactions, '/transaction/pendings')


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT)
