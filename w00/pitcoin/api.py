import codecs

import requests
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
from pitcoin.storage_handlers.pending_pool import MemPoolStorage
from pitcoin.storage_handlers.chain import BlocksStorage
from pitcoin.block import Block
from pitcoin.settings import *
from pitcoin.transaction.serialization import *


mempool = MemPoolStorage()
blocks = BlocksStorage()
nodes = []

app = Flask(__name__)
api = Api(app)


class Transaction(Resource):
    def post(self):
        response = app.response_class(
            response=json.dumps({"result": mempool.add_serialized_transaction_to_mempool(request.data)}),
            status=200,
            mimetype='application/json'
        )

        #broadcasting transaction to all known nodes
        for node in nodes:
            requests.post(node + '/transaction/new', request.data)

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


class Chain(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('trunc', type=str)
        args = parser.parse_args()

        list = blocks.get_all_blocks()
        if args['trunc'] == "last":
            last = list[-1]
            json_repr = json.dumps(last.__dict__)
        else:
            json_repr = json.dumps([b.__dict__ for b in list])
        response = app.response_class(
            response=json_repr,
            status=200,
            mimetype='application/json'
        )
        return response

    def delete(self):
        response = app.response_class(
            response=json.dumps({"result": blocks.delete_all_blocks_from_mempool()}),
            status=200,
            mimetype='application/json'
        )
        return response


class ChainBlock(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('height', type=int)
        args = parser.parse_args()

        list = blocks.get_all_blocks()

        if args['height'] and args['height'] < len(list):
            block = list[args['height']]
        else:
            block = blocks.get_last_block()
        print(block)
        json_repr = json.dumps(block.__dict__)

        response = app.response_class(
            response=json_repr,
            status=200,
            mimetype='application/json'
        )
        return response

    def post(self):
        json_repr = json.loads(codecs.decode(request.data, 'ascii'))
        block = Block(
            json_repr['timestamp'],
            json_repr['previous_hash'],
            [codecs.encode(tx, 'ascii') for tx in json_repr['transactions']],
            json_repr['nonce']
        )

        last_block = blocks.get_last_block()
        if last_block:
            if block.hash_value == last_block.hash_value:
                return ""

        response = app.response_class(
            response=json.dumps({"result": blocks.add_block_to_storage(block)}),
            status=200,
            mimetype='application/json'
        )
        # deleting all transactions that new block contains from the mempool
        for tx in block.transactions:
            deserialized = Deserializer.deserialize_transaction(codecs.encode(tx, 'ascii'))
            mempool.delete_transaction_if_exists(deserialized)

        # broadcasting new block for all known nodes
        for node in nodes:
            requests.post(node + '/chain/block', json.dumps(json_repr))

        return response


class ChainLength(Resource):
    def get(self):
        response = app.response_class(
            response=json.dumps({"chain_length": len(blocks.get_all_blocks())}),
            status=200,
            mimetype='application/json'
        )
        return response


class Node(Resource):
    def get(self):
        return app.response_class(
            response=json.dumps(nodes),
            status=200,
            mimetype='application/json'
        )

    def post(self):
        nodes.append(codecs.decode(request.data, 'ascii'))
        return True


api.add_resource(Transaction, '/transaction/new', methods=['POST'])
api.add_resource(Transactions, '/transaction/pendings', methods=['GET', 'DELETE'])
api.add_resource(Chain, '/chain',  methods=['GET', 'DELETE'])
api.add_resource(ChainBlock, '/chain/block', methods=['GET', 'POST'])
api.add_resource(ChainLength, '/chain/length', methods=['GET'])
api.add_resource(Node, '/node', methods=['GET', 'POST'])


def serve():
    app.run(host=API_HOST, port=API_PORT)


if __name__ == '__main__':
    serve()
