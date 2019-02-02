import json

from pitcoin_modules.transaction.input import Input
from pitcoin_modules.transaction.output import Output
from pitcoin_modules.wallet import *
from pitcoin_modules.settings import *


class Transaction:
    def __init__(self, inputs: list, outputs: list, locktime: int):
        self.version = 1
        self.inputs = inputs
        self.outputs = outputs
        self.locktime = locktime
        self.txid = self.get_hash()

    def get_hash(self):
        return ""

    def __str__(self):
        return self.to_json()

    def to_json(self):
        data = {
            "version": self.version,
            "inputs": [input.__dict__ for input in self.inputs],
            "ouputs": [output.__dict__ for output in self.outputs],
            "locktime": self.locktime,
            "txid": self.txid
        }
        return json.dumps(data)

    def from_json(self):
        pass

    def __eq__(self, other):
        return str(self) == str(other)


class CoinbaseTransaction(Transaction):
    def __init__(self, scriptpubkey):
        inputs = []
        inputs.append(Input("0" * 64, int("f" * 8, 16), ""))
        outputs = [Output(5000000000, scriptpubkey)]
        super().__init__(inputs, outputs, 0)

