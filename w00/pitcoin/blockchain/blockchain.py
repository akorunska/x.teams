import time

import requests

from pitcoin.transaction import *
from pitcoin.block import Block
from pitcoin.settings import *


class Blockchain:
    def __init__(self):
        self.difficulty = 2
        self.chain = []
        self.api_url = "http://" + API_HOST + ":" + API_PORT

    def mine(self):
        request_data = requests.get(self.api_url + '/transaction/pendings' + '?amount=3').json()
        tx_list = [Transaction(
            item['sender'],
            item['recipient'],
            item['amount'],
            item['sign_pubkey'],
            item['signature']
        ) for item in request_data]
        # todo add coinbase transaction in the block
        block = Block(str(int(time.time())), '0', tx_list)
        while block.hash_value[0:self.difficulty] != b'0' * self.difficulty:
            block.nonce += 1
            block.hash_value = block.get_hash()

    def resolve_conflicts(self):
        pass

    def is_valid_chain(self):
        pass

    def add_node(self):
        pass

    def genesis_block(self):
        pass

    def submit_tx(self, tx):
        serialized = Serializer.serialize_transaction(tx)
        requests.post(self.api_url + '/transaction/new', serialized)

    def submit_block(self, block: Block):
        pass

if __name__ == '__main__':
    blockchain = Blockchain()
    blockchain.mine()
