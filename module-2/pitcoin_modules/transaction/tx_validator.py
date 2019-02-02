from .transaction import Transaction
from pitcoin_modules.script import run_script


def get_tx_by_txid(tx_list, txid):
    for tx in tx_list:
        if tx.txid == txid:
            return tx
    return None


def check_tx_validity(tx: Transaction, tx_list: list):
    for input in tx.inputs:
        tx_with_output_to_unlock = get_tx_by_txid(tx_list, input.txid)
        if not tx_with_output_to_unlock:
            return False
        if len(tx_with_output_to_unlock.outputs) < input.vout:
            return False
        output = tx_with_output_to_unlock.outputs[input.vout - 1]
        script = input.scriptsig + output.scriptpubkey
        if not run_script(script, input.txid):
            return False
    return True

