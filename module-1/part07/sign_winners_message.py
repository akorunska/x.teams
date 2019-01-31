import hashlib
import codecs
import ecdsa
import binascii


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
    return vk.verify(binascii.unhexlify(signature), msg)


data = b"https://ncase.me/trust/"
winner = b"Grudger"
private_key = hashlib.sha256(data).hexdigest()

result = sign_message_with_private_key(private_key, winner)

print(" public key: %s \n signarute: %s\n" % (result["public_key"], result["signature"]))
print(" signature verification result:", check_message_signature(result["public_key"], result['signature'], winner))

