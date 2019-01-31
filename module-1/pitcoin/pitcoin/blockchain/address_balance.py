import codecs
from pitcoin.block.block import Block
from pitcoin.transaction import *


def get_balance(block_list: list, address: str):
    balance = 0
    for block in block_list:
        tx_list = [Deserializer.deserialize_transaction(codecs.encode(tx, 'ascii')) for tx in block.transactions]
        for tx in tx_list:
            if tx.sender == address:
                balance -= tx.amount
            elif tx.recipient == address:
                balance += tx.amount
    return balance
