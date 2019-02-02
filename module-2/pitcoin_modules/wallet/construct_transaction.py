from pitcoin_modules.transaction import Input, Output, Transaction
from pitcoin_modules.wallet.wallet import *


def construct_transaction_locking_script(recipient):
    hashed160_pubkey = get_hashed_public_key_from_address(recipient)
    script = "76a914" + hashed160_pubkey + "88ac"
    return script


def construct_transaction_unlocking_script(privkey, txid):
    resp = sign_message_with_private_key(privkey, codecs.encode(txid))
    resp['public_key'] = b"04" + resp['public_key']
    script = "%02x" % (len(resp['signature']) // 2) + codecs.decode(resp['signature']) + "%02x" % (len(resp['public_key']) // 2) + codecs.decode(resp['public_key'])
    return script

def construct_transaction(sender_privkey, sender, recipient, amount, utxo_list):
    # collect all outputs necessary to pay that amount of money
    outputs_to_spend = []
    value_to_spend = 0
    for outp in utxo_list:
        outputs_to_spend.append(outp)
        value_to_spend += outp.value
        if value_to_spend >= amount:
            break
    # convert all outputs we are going to use in the ouputs
    inputs = [
        Input(
            outp.txid,
            outp.vout,
            construct_transaction_unlocking_script(sender_privkey, outp.txid)
        ) for outp in outputs_to_spend
    ]

    # create outputs: to the recipient and change for the sender(if needed)
    outputs = [Output(amount, construct_transaction_locking_script(recipient))]
    if value_to_spend > amount:
        outputs.append(Output(value_to_spend - amount, construct_transaction_locking_script(sender)))

    return Transaction(inputs, outputs, locktime=0)
