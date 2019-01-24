import unittest
from pitcoin.transaction import *


class TestSerialization(unittest.TestCase):
    def test_serialization_basic(self):
        tx = Transaction("1GFfoqR4Z4BZEy75Nd9CRMTKAev3oukY2Q", "1FrNfonA4Z24ugVww9JjoeqzjxCE9LN3cf", 20)
        tx.sign_transaction("936abdc0429eb4b38a045fcb8f531ff7cf3888c3a83797df5d033106c4ea6a20")

        serialized = Serializer.serialize_transaction(tx)
        deserialized = Deserializer.deserialize_transaction(serialized)
        self.assertEqual(str(tx), str(deserialized))


class TestTransactionAdressesValidation(unittest.TestCase):
    def test_check_valid_address(self):
        addr = "1F2h8wVXzUaatkgJjNLCRzsrts3MuaBnjM"
        self.assertEqual(True, check_address_available(addr))

    def test_check_short_address(self):
        addr = "1F2h8wVXzUaatkgJjNLCRzsrts3MuaBnj"
        self.assertEqual(False, check_address_available(addr))

    def test_check_long_address(self):
        addr = "1F2h8wVXzUaatkgJjNLCRzsrts3MuaBnjMe"
        self.assertEqual(False, check_address_available(addr))

    def test_check_bad_checksum(self):
        pubkey = "033fb2d971568a6952b1f436c7cf471efca5d4cd2ec37a51003d463584106ba1e4"
        pubkey_sha_encrypted = hashlib.sha256(binascii.unhexlify(pubkey)).hexdigest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(binascii.unhexlify(pubkey_sha_encrypted))
        pubkey_ripemd_encrypted = ripemd160.hexdigest()
        mainnet_network_bytes = "00"
        key_with_network_bytes = mainnet_network_bytes + pubkey_ripemd_encrypted
        address = key_with_network_bytes + "cb4ae80c"
        addr = base58.b58encode(binascii.unhexlify(address)).decode('ascii')

        self.assertEqual(False, check_address_available(addr))

    def test_check_bad_network_bytes(self):
        pubkey = "033fb2d971568a6952b1f436c7cf471efca5d4cd2ec37a51003d463584106ba1e4"
        pubkey_sha_encrypted = hashlib.sha256(binascii.unhexlify(pubkey)).hexdigest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(binascii.unhexlify(pubkey_sha_encrypted))
        pubkey_ripemd_encrypted = ripemd160.hexdigest()
        network_bytes = "02"
        key_with_network_bytes = network_bytes + pubkey_ripemd_encrypted
        key_hashed1 = hashlib.sha256(binascii.unhexlify(key_with_network_bytes)).hexdigest()
        key_hashed2 = hashlib.sha256(binascii.unhexlify(key_hashed1)).hexdigest()
        address = key_with_network_bytes + key_hashed2[:8]
        addr = base58.b58encode(binascii.unhexlify(address)).decode('ascii')

        self.assertEqual(False, check_address_available(addr))

class TestTransactionCorrespondingAddressesValidation(unittest.TestCase):
    def test_check_address_from_uncompressed_pubkey(self):
        pubkey = b'50e829ca678c60031a11b990fea865e03ba35d0579aa62750b918b98c4b935d803ecc57a4bb2fc2ab1193a87fca5386d71516aca89df267fc907bcb3b84d396a'
        addres_from_uncompressed_privkey = '1GFfoqR4Z4BZEy75Nd9CRMTKAev3oukY2Q'
        self.assertEqual(True, check_corresponding_addressed(addres_from_uncompressed_privkey, pubkey))

    def test_check_address_from_compressed_pubkey(self):
        pubkey = b'50e829ca678c60031a11b990fea865e03ba35d0579aa62750b918b98c4b935d803ecc57a4bb2fc2ab1193a87fca5386d71516aca89df267fc907bcb3b84d396a'
        addres_from_compressed_privkey = '1NERjvtBxL5ErAKhCC3mfgWbp3QMd8y6ba'
        self.assertEqual(True, check_corresponding_addressed(addres_from_compressed_privkey, pubkey))

