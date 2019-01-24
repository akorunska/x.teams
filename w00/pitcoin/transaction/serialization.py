import codecs
import struct
from .tx_validator import *
from .transaction import Transaction


class Serializer:
    @staticmethod
    def serialize_transaction(tx: Transaction):
        amount = codecs.encode("%04x" % tx.amount)
        sender = codecs.encode(tx.sender, 'utf-8')
        recipient = codecs.encode(tx.recipient, 'utf-8')

        serialized_tx = struct.pack("4s34s34s128s128s", amount, sender, recipient, tx.sign_pubkey, tx.signature)
        return serialized_tx


class Deserializer:
    @staticmethod
    def deserialize_transaction(stx: bytes):
        (amount, sender, recipient, sign_pubkey, signature) = struct.unpack("4s34s34s128s128s", stx)
        return Transaction(
                            codecs.decode(sender, "utf-8"),
                            codecs.decode(recipient, "utf-8"),
                            int(amount, 16),
                            sign_pubkey,
                            signature
        )

