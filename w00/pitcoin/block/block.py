

class Block:
    def __init__(self, timestamp, previous_hash, transactions):
        self.timestamp = timestamp
        self.nonce = previous_hash
        self.previous_hash = transactions
        self.transactions = []
        self.hash = 0
        self.merkle_root = 0

    def validate_all_transactions(self):
        pass

    def get_hash(self):
        pass

