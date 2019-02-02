from pitcoin_modules.wallet.wallet import *


def construct_transaction_locking_script(address):
    hashed160_pubkey = get_hashed_public_key_from_address(address)
    script = "76a914" + hashed160_pubkey + "88ac"
    return script


