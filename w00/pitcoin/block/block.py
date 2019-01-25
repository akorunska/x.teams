from pitcoin.block.merkle import get_merkle_root, sha256_bytes_to_bytes
from pitcoin.transaction import Serializer, check_tx_validity

import codecs


class Block:
    def __init__(self, timestamp, previous_hash, transactions):
        self.timestamp = timestamp
        self.nonce = 0
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.merkle_root = get_merkle_root([Serializer.serialize_transaction(tx) for tx in self.transactions])
        self.hash_value = self.get_hash()

    def validate_all_transactions(self):
        tx_are_valid = True
        for tx in self.transactions:
            tx_are_valid = tx_are_valid and check_tx_validity(tx)
        return tx_are_valid

    def get_hash(self):
        data = codecs.encode(self.timestamp, 'ascii') + codecs.encode(str(self.nonce), 'ascii') +\
            codecs.encode(self.previous_hash, 'ascii')
        tx_serialized = [Serializer.serialize_transaction(tx) for tx in self.transactions]
        for tx in tx_serialized:
            data += tx
        data += self.merkle_root
        return sha256_bytes_to_bytes(data)


