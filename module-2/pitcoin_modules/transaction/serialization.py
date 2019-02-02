import codecs
import struct
from .tx_validator import *
from .transaction import Transaction


def reverse_bytes(s: str):
    res = list(s)
    for i in range(len(s) // 2):
        res[2*i] = s[len(s) - 2 - i*2]
        res[2*i + 1] = s[len(s) - 1 - i*2]
    return ''.join(res)


class Serializer:
    @staticmethod
    def serialize_transaction(tx: Transaction):
        # amount = codecs.encode("%04x" % tx.amount)
        # sender = codecs.encode(tx.sender, 'utf-8')

        # serialized_tx = struct.pack("4s34s34s128s128s", amount, sender, recipient, sign_pubkey, signature)
        result = ""

        #packing tx version
        result += reverse_bytes("%08x" % tx.version)

        #packing tx inputs
        result += "%02x" % len(tx.inputs)
        #packing each input
        for input in tx.inputs:
            #pack txid
            result += reverse_bytes(input.txid)
            #pack vout
            result += reverse_bytes("%08x" % input.vout)
            #pack scriptsig
            result += "%02x" % (len(input.scriptsig) // 2)
            result += input.scriptsig
            #add sequence
            result += "f" * 8

        #packing tx outputs
        result += "%02x" % len(tx.outputs)
        # packing each output
        for output in tx.outputs:
            #pack value
            result += reverse_bytes("%016x" % output.value)
            # pack scriptsig
            result += "%02x" % (len(output.scriptpubkey) // 2)
            result += output.scriptpubkey

        #packing locktime
        result += reverse_bytes("%08x" % tx.locktime)
        return result


class Deserializer:
    @staticmethod
    def deserialize_transaction(stx: bytes):
        # (amount, sender, recipient, sign_pubkey, signature) = struct.unpack("4s34s34s128s128s", stx)
        # return Transaction(
        #                     codecs.decode(sender, "utf-8"),
        #                     codecs.decode(recipient, "utf-8"),
        #                     int(amount, 16),
        #                     codecs.decode(sign_pubkey, "utf-8"),
        #                     codecs.decode(signature, "utf-8")
        # )
        pass

