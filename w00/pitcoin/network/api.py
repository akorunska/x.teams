from flask import Flask, request
from flask_restful import Resource, Api
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
        print("transaction", request.data)
        return mempool.add_serialized_transaction_to_mempool(request.data)


class Transactions(Resource):
    def get(self):
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
