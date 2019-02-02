import codecs
import struct

from pitcoin_modules.transaction.input import Input
from pitcoin_modules.transaction.output import Output
from .tx_validator import *
from .transaction import Transaction, CoinbaseTransaction


def reverse_bytes(s: str):
    res = list(s)
    for i in range(len(s) // 2):
        res[2*i] = s[len(s) - 2 - i*2]
        res[2*i + 1] = s[len(s) - 1 - i*2]
    return ''.join(res)


class Serializer:
    @staticmethod
    def serialize_transaction(tx: Transaction):
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
    def deserialize_transaction(stx: str):
        cur = 0
        version = int(reverse_bytes(stx[cur:cur + 8]), 16)
        cur += 8

        inputs_count = int(stx[cur:cur + 2], 16)
        cur += 2
        inputs = []
        for i in range(inputs_count):
            txid = reverse_bytes(stx[cur:cur + 64])
            cur += 64
            vout = int(reverse_bytes(stx[cur:cur+8]), 16)
            cur += 8
            len = int(stx[cur:cur+2], 16)
            cur += 2
            scriptsig = stx[cur:cur + len*2]
            cur += len*2
            cur += 8    #skipping sequence

            inputs.append(Input(txid, vout, scriptsig))

        outputs_count = int(stx[cur:cur + 2], 16)
        cur += 2
        outputs = []
        for i in range(outputs_count):
            value = int(reverse_bytes(stx[cur:cur+16]), 16)
            cur += 16
            len = int(stx[cur:cur + 2], 16)
            cur += 2
            scriptpubkey = stx[cur:cur + len*2]
            cur += len*2

            outputs.append(Output(value, scriptpubkey))

        locktime = int(reverse_bytes(stx[cur:cur + 8]), 16)
        return Transaction(inputs, outputs, locktime)

