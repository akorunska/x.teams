import ecdsa
import binascii


def check_message_signature(public_key: bytes, signature: bytes, msg: bytes):
    vk = ecdsa.VerifyingKey.from_string(binascii.unhexlify(public_key), curve=ecdsa.SECP256k1)
    return vk.verify(binascii.unhexlify(signature), msg)


message = b"Grudger"
pubkey = b"11855c28aae95a947ccf3361425c3d33ed669ef9ae07b50559343e31316a56249d99764b637b39e939b4a46f4cc021c2d3144da3be5ee0ce6ca47293d0db51b9"
signature = b"7effdfc0c3051fcc0803ec19358e4fef8c904ba53135cb06e0eb2ee985458ece15fea8fa3819258d11230559da2b94911ae06576acad52ae59fa944febab82c1"

print(check_message_signature(pubkey, signature, message))
