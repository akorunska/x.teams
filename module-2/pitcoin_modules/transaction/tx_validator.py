from pitcoin_modules.wallet import *
from .transaction import Transaction


def check_tx_validity(tx: Transaction):
    return True
    # if check_coinbase_transaction(tx):
    #     return True
    #
    # return (check_address_available(tx.sender) and
    #         check_address_available(tx.recipient) and
    #         check_corresponding_addressed(tx.sender, tx.sign_pubkey) and
    #         check_signature_validity(tx.sign_pubkey, tx.signature, tx.get_hash()))

def check_coinbase_transaction(tx: Transaction):
    return (tx.amount == 50 and
            tx.sender == "0" * 34 and
            check_address_available(tx.recipient) and
            check_corresponding_addressed(tx.recipient, tx.sign_pubkey) and
            check_signature_validity(tx.sign_pubkey, tx.signature, tx.get_hash()))

def check_address_available(address):
    try:
        hex_address = codecs.decode(binascii.hexlify(base58.b58decode_check(address)), "ascii")
    except Exception as e:
        return False
    if not len(hex_address) == 42:
        return False
    if not hex_address[0:2] == "00":
        return False
    return True


def check_corresponding_addressed(address, pubkey):
    if not len(pubkey) == 128:
        return False
    received_address_compressed = get_address_from_public_key(b"04" + codecs.encode(pubkey, 'ascii'))
    received_address_uncompressed = get_address_from_public_key(
        get_compressed_form_of_public_key(codecs.encode(pubkey, 'ascii'))
    )
    if not (received_address_compressed == address or received_address_uncompressed == address):
        return False
    return True


def check_signature_validity(pubkey, signature, hash):
    return check_message_signature(pubkey, signature, hash)
