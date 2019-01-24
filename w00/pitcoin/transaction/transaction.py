import json
from pitcoin.wallet import *


class Transaction:
    def __init__(self, sender: str, recipient: str, amount: int, sign_pubkey=b"", signature=b"", ):
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
        self.sign_pubkey = resp['public_key']
        self.signature = resp['signature']
        return resp

    def __str__(self):
        data = {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "sign_pubkey": codecs.decode(self.sign_pubkey, "utf-8"),
            "signature": codecs.decode(self.signature, "utf-8")
        }
        return json.dumps(data)

    def __eq__(self, other):
        return str(self) == str(other)


class CoinbaseTransaction(Transaction):
    def __init__(self, recipient: str):
        super().__init__("0" * 64, recipient, 50)

    def sign_transaction(self, **kwargs):
        privkey = export_hex_from_file_with_wif_privkey("minerkey")
        return super().sign_transaction(privkey)

