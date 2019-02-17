import json
import random
import time

import requests

from pitcoin_modules.transaction import *
from pitcoin_modules.block import Block, get_merkle_root
from pitcoin_modules.settings import *
from pitcoin_modules.wallet import *


class Blockchain:
    def __init__(self):
        self.api_url = "http://" + API_HOST + ":" + API_PORT

    def mine(self, block=None):
        if not block:
            block = self.create_block_with_loaded_transactions()

        initial_chain_len = requests.get(self.api_url + '/chain/length').json()['chainlength']
        target = requests.get(self.api_url + '/meta').json()['current_target']
        target = int(target, 16)

        while int(block.hash_value, 16) > target:
            block.nonce = random.randint(0, 2**32)
            block.hash_value = block.get_hash()
            if requests.get(self.api_url + '/chain/length').json()['chainlength'] > initial_chain_len:
                return None
        return block

    def create_block_with_loaded_transactions(self):
        data = requests.get(self.api_url + '/block').json()
        prev = data['block']
        request_data = requests.get(self.api_url + '/transaction/pendings' + '?amount=3').json()
        tx_list = [Serializer.serialize_transaction(Transaction.from_dict(item)) for item in request_data]

        tx_list.append(Serializer.serialize_transaction(self.construct_miners_rewarding_transaction()))
        target = requests.get(self.api_url + '/meta').json()['current_target']
        block = Block(str(int(time.time())), prev['hash_value'], tx_list, target)
        return block

    def construct_miners_rewarding_transaction(self):
        recipient = read_file_contents(PROJECT_ROOT + '/address')
        block_hei = requests.get(self.api_url + '/chain/length').json()['chainlength']
        reward = requests.get(self.api_url + '/meta').json()['current_miner_reward']

        tx = CoinbaseTransaction(construct_transaction_locking_script(recipient), block_hei, reward)
        return tx

    def resolve_conflicts(self):
        # nodes_list = requests.get(self.api_url + '/node').json()
        # current_len = requests.get(self.api_url + '/chain/length').json()['chainlength']
        # longest = {'len': current_len, 'source': ''}
        # for node in nodes_list:
        #     node_chain_len = requests.get(node + '/chain/length').json()['chainlength']
        #     if node_chain_len > longest['len']:
        #         block_list = requests.get(node + '/chain').json()
        #         block_obj_list = [Block.from_json(b) for b in block_list]
        #         if Blockchain.is_valid_chain(block_obj_list):
        #             longest['len'] = node_chain_len
        #             longest['source'] = node
        # if longest['source'] == '':
        #     return ""
        # requests.delete(self.api_url + '/chain')
        # requests.delete(self.api_url + '/utxo')
        # for block in block_list:
        #     requests.post(self.api_url + '/chain', json.dumps(block))
        # return longest
        pass

    @staticmethod
    def is_valid_chain(list):
        if len(list) == 0:
            return True
        prev = list[0]
        for i in range(1, len(list)):
            cur = list[i]
            if cur.hash_value != cur.get_hash():
                return False
            if cur.previous_hash != prev.hash_value:
                return False
            if not cur.validate_all_transactions():
                return False
            prev = cur
        return True

    def add_node(self, node_url):
        requests.post(self.api_url + '/node', node_url)

    def genesis_block(self):
        target = requests.get(self.api_url + '/meta').json()['current_target']
        genesis = Block(
            str(int(time.time())), 64 * '0',
            [Serializer.serialize_transaction(self.construct_miners_rewarding_transaction())],
            target
        )
        return self.mine(block=genesis)

    def submit_tx(self, raw_tx):
        data = json.dumps({'transaction': raw_tx})
        return requests.post(self.api_url + '/transaction', data).json()

    def mine_and_submit_block(self):
        block = self.mine()
        if not block:
            return None
        data = json.dumps({'block': str(block)})
        requests.post(self.api_url + '/block', data)
        return block.hash_value


if __name__ == '__main__':
    blockchain = Blockchain()
    print(blockchain.mine_and_submit_block())
