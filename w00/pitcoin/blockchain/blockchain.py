import time

import requests

from pitcoin.transaction import *
from pitcoin.block import Block
from pitcoin.settings import *
from pitcoin.wallet import *


class Blockchain:
    def __init__(self):
        self.difficulty = 2
        self.chain = []
        self.api_url = "http://" + API_HOST + ":" + API_PORT

    def mine(self, block=None):
        if not block:
            block = self.create_block_with_loaded_transactions()
        while block.hash_value[0:self.difficulty] != '0' * self.difficulty:
            block.nonce += 1
            block.hash_value = block.get_hash()
        return block

    def create_block_with_loaded_transactions(self):
        prev = requests.get(self.api_url + '/chain?trunc=last').json()
        request_data = requests.get(self.api_url + '/transaction/pendings' + '?amount=3').json()
        tx_list = [Serializer.serialize_transaction(Transaction(
            item['sender'],
            item['recipient'],
            item['amount'],
            item['sign_pubkey'],
            item['signature']
        )) for item in request_data]
        # todo add coinbase transaction in the block
        block = Block(str(int(time.time())), prev['hash_value'], tx_list)
        return block

    def construct_miners_rewarding_transaction(self):
        resipient = read_file_contents(PROJECT_ROOT + '/address')
        tx = CoinbaseTransaction(resipient)
        tx.sign_transaction()
        return tx

    def resolve_conflicts(self):
        pass

    def is_valid_chain(self):
        pass

    def add_node(self):
        pass

    def genesis_block(self):
        genesis = Block(str(int(time.time())), 64 * '0', [Serializer.serialize_transaction(self.construct_miners_rewarding_transaction())])
        return self.mine(block=genesis)

    def submit_tx(self, tx):
        serialized = Serializer.serialize_transaction(tx)
        requests.post(self.api_url + '/transaction/new', serialized)

    def mine_and_submit_block(self):
        block = self.mine()
        requests.post(self.api_url + '/chain', str(block))


if __name__ == '__main__':
    blockchain = Blockchain()
    print(blockchain.mine_and_submit_block())
