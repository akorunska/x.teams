import json

from pitcoin_modules.block.merkle import get_merkle_root, sha256_bytes_to_bytes
from pitcoin_modules.transaction import Serializer, Deserializer, check_tx_validity

import codecs


class Block:
    def __init__(self, timestamp, previous_hash, transactions, nonce=0):
        self.timestamp = timestamp
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.transactions = [codecs.decode(tx, 'ascii') for tx in transactions]
        self.merkle_root = codecs.decode(get_merkle_root(self.transactions), 'ascii')
        self.hash_value = self.get_hash()

    def validate_all_transactions(self):
        tx_are_valid = True
        for tx in self.transactions:
            tx_are_valid = tx_are_valid and check_tx_validity(Deserializer.deserialize_transaction(codecs.encode(tx, 'ascii')))
        return tx_are_valid

    def get_hash(self):
        data = codecs.encode(self.timestamp, 'ascii') + codecs.encode(str(self.nonce), 'ascii') +\
            codecs.encode(self.previous_hash, 'ascii')
        for tx in self.transactions:
            data += codecs.encode(tx)
        data += codecs.encode(self.merkle_root, 'ascii')
        return codecs.decode(sha256_bytes_to_bytes(data), 'ascii')

    @staticmethod
    def from_json(json_str):
        block = Block(
            json_str['timestamp'],
            json_str['previous_hash'],
            [codecs.encode(tx, 'ascii') for tx in json_str['transactions']],
            json_str['nonce']
        )
        return block

    def __str__(self):
        return json.dumps(self.__dict__)
