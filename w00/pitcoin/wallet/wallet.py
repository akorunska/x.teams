import binascii
import codecs
import secrets
import hashlib
import base58
import ecdsa


def generate_private_key():
    order_of_elliptic_curve = 1.158 * 10**77
    privkey = hex(int(order_of_elliptic_curve))

    while float(int(privkey, 16)) >= order_of_elliptic_curve:
        randbits = secrets.randbits(1024)
        privkey = hashlib.sha256(str(randbits).encode('utf-8')).hexdigest()
    return privkey


def read_file_contents(filename):
    f = open(filename)
    return f.read().strip().upper()


def convert_hex_private_key_to_wif(hex_privkey: str):
    hex_privkey = str(hex_privkey)
    hex_privkey_extended = "80" + hex_privkey
    hashed1 = hashlib.sha256(binascii.unhexlify(hex_privkey_extended)).hexdigest()
    hashed2 = hashlib.sha256(binascii.unhexlify(hashed1)).hexdigest()
    final_key = hex_privkey_extended + hashed2[:8]
    return base58.b58encode(binascii.unhexlify(final_key))


def convert_wif_to_hex_private_key(wif_privkey: str):
    hex_decoded = binascii.hexlify(base58.b58decode(wif_privkey))[2:-8]
    return hex_decoded


def export_wif_from_file_with_hex_privkey(filename):
    hex_privkey = read_file_contents(filename)
    return convert_hex_private_key_to_wif(hex_privkey)


def export_hex_from_file_with_wif_privkey(filename):
    wif_privkey = read_file_contents(filename)
    return convert_wif_to_hex_private_key(wif_privkey)


def get_public_key_from_private_key(privkey, use_compressed=True):
    privkey_bytes = codecs.decode(privkey, 'hex')
    # Get ECDSA public key
    key = ecdsa.SigningKey.from_string(privkey_bytes, curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    key_hex = codecs.encode(key_bytes, 'hex')
    if not use_compressed:
        pubkey = b"04" + key_hex
    else:
        x = key_hex[0:(int(len(key_hex)/2))]
        y = key_hex[(int(len(key_hex)/2)):]
        if int(y, 16) % 2 == 0:
            pubkey = b'02' + x
        else:
            pubkey = b'03' + x
    return pubkey


def get_address_from_private_key(privkey, use_compressed=True):
    # using compressed key as default to generate and address as it becoming default option for many bitcoin clients
    # uncompressed key can be used as well by use_compressed=False
    pubkey = get_public_key_from_private_key(privkey, use_compressed)

    pubkey_sha_encrypted = hashlib.sha256(binascii.unhexlify(pubkey)).hexdigest()

    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(binascii.unhexlify(pubkey_sha_encrypted))
    pubkey_ripemd_encrypted = ripemd160.hexdigest()

    mainnet_network_bytes = "00"
    key_with_network_bytes = mainnet_network_bytes + pubkey_ripemd_encrypted

    key_hashed1 = hashlib.sha256(binascii.unhexlify(key_with_network_bytes)).hexdigest()
    key_hashed2 = hashlib.sha256(binascii.unhexlify(key_hashed1)).hexdigest()
    address = key_with_network_bytes + key_hashed2[:8]
    return base58.b58encode(binascii.unhexlify(address)).decode('ascii')


def sign_message_with_private_key(privkey, message: bytes):
    responce = {}
    privkey_bytes = codecs.decode(privkey, 'hex')
    key = ecdsa.SigningKey.from_string(privkey_bytes, curve=ecdsa.SECP256k1)
    verifying_key = key.get_verifying_key()
    responce['public_key'] = binascii.hexlify(verifying_key.to_string())
    responce['signature'] = binascii.hexlify(key.sign(message))
    # print(vk.verify(binascii.unhexlify(responce['signature']), message))
    return responce


def check_message_signature(public_key: bytes, signature: bytes, msg: bytes):
    vk = ecdsa.VerifyingKey.from_string(binascii.unhexlify(public_key), curve=ecdsa.SECP256k1)
    return vk.verify(binascii.unhexlify(signature), msg)  # True
