import json
from pitcoin.wallet import *
from pitcoin.settings import *


class Transaction:
    # todo add id for the transaction
    def __init__(self, sender: str, recipient: str, amount: int, sign_pubkey="", signature=""):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.sign_pubkey = sign_pubkey
        self.signature = signature

    def get_hash(self):
        data = self.sender + self.recipient + str(self.amount)
        return binascii.unhexlify(hashlib.sha256(data.encode("utf-8")).hexdigest())

    def sign_transaction(self, sender_privkey):
        resp = sign_message_with_private_key(sender_privkey, self.get_hash())
        self.sign_pubkey = codecs.decode(resp['public_key'], 'ascii')
        self.signature = codecs.decode(resp['signature'], 'ascii')
        return resp

    def __str__(self):
        return json.dumps(self.__dict__)

    def __eq__(self, other):
        return str(self) == str(other)


class CoinbaseTransaction(Transaction):
    def __init__(self, recipient: str):
        super().__init__("0" * 34, recipient, 50)

    def sign_transaction(self, **kwargs):
        privkey = export_hex_from_file_with_wif_privkey(PROJECT_ROOT + "/minerkey")
        return super().sign_transaction(privkey)

