import json
from pitcoin_modules.wallet import *
from pitcoin_modules.settings import *


class Transaction:
    def __init__(self, inputs: list, outputs: list, locktime: str):
        self.version = 1
        self.inputs = inputs
        self.outputs = outputs
        self.locktime = locktime
        self.txid = self.get_hash()

    def get_hash(self):
        return ""

    # def __str__(self):
    #     return json.dumps(self.__dict__)

    def __eq__(self, other):
        return str(self) == str(other)


# class CoinbaseTransaction(Transaction):
#     def __init__(self, recipient: str):
#         super().__init__("0" * 34, recipient, 50)
#
#     def sign_transaction(self, **kwargs):
#         privkey = export_hex_from_file_with_wif_privkey(PROJECT_ROOT + "/minerkey")
#         return super().sign_transaction(privkey)

