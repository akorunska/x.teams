import codecs
from pitcoin_modules.block.block import Block
from pitcoin_modules.transaction import *


def address_from_p2pkh_script(script: str):
    pubkey_hashed = script[6:len(script) - 4]
    return get_address_from_hashed_public_key(pubkey_hashed)


def get_balance(outp_list: list, address: str):
    balance = 0
    for outp in outp_list:
        # print(address_from_p2pkh_script(outp.scriptpubkey))
        if address_from_p2pkh_script(outp.scriptpubkey) == address:
            balance += outp.value
    return balance
