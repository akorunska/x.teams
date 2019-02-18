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
        self.witness = []
        self.txid = self.get_hash()

        self.senders = []
        for input in self.inputs:
            if input.txid != '0' * 64:
                self.senders.append(self.address_from_unlocking_script(input.scriptsig))
        self.recipients = []
        for output in self.outputs:
            self.recipients.append(self.address_from_locking_script(output.scriptpubkey))

    @staticmethod
    def address_from_locking_script(script: str):
        pubkey_hashed = script[6:len(script) - 4]
        return get_address_from_hashed_public_key(pubkey_hashed)

    @staticmethod
    def address_from_unlocking_script(script: str):
        pubkey = script[len(script) - 128:]
        return get_address_from_public_key("04" + pubkey)

    def get_hash(self):
        tx_data = Serializer.serialize_transaction(self)
        return sha256_str_to_str(sha256_str_to_str(tx_data))

    def __str__(self):
        return self.to_json()

    def to_dict(self):
        data = {
            "version": self.version,
            "inputs": [input.__dict__ for input in self.inputs],
            "outputs": [output.__dict__ for output in self.outputs],
            "locktime": self.locktime,
            "txid": self.txid,
            "senders": self.senders,
            "recipients": self.recipients
        }
        for i, output in zip(range(1, len(data['outputs']) + 1), data['outputs']):
            output['txid'] = self.txid
            output['vout'] = i
        return data

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(dict):
        version = dict['version']
        inputs = [Input(input['txid'], input['vout'], input['scriptsig']) for input in dict['inputs']]
        outputs = [Output(output['value'], output['scriptpubkey']) for output in dict['outputs']]
        return Transaction(inputs, outputs, dict['locktime'])

    def __eq__(self, other):
        return self.txid == other.txid


class CoinbaseTransaction(Transaction):
    def __init__(self, scriptpubkey, block_height: int, reward):
        inputs = []
        inputs.append(Input("0" * 64, int("f" * 8, 16), "%016x" % block_height))
        outputs = [
            Output(int(reward * 10**8), scriptpubkey)
        ]
        super().__init__(inputs, outputs, 0)


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

    @staticmethod
    def construct_tx_data_as_signature_message(inputs, outputs, locktime, utxo_list):
        for input in inputs:
            prev_txid = input.txid
            prev_vout = input.vout
            output_to_spend = None
            for utxo in utxo_list:
                if utxo.txid == prev_txid and utxo.vout == prev_vout:
                    output_to_spend = utxo
                    break
            input.scriptsig = output_to_spend.scriptpubkey
        return Serializer.serialize_transaction(Transaction(inputs, outputs, locktime))


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
