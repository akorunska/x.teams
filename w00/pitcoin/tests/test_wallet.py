import unittest
from ..wallet import *


class TestConvertHexPrivateKeyToWif(unittest.TestCase):
    def test_correct_hex(self):
        hex = "c1421c809f270aa475f16adeaf3dab4fb9d28eaccbf2e1e35ff38cf99609c308"
        result = convert_hex_private_key_to_wif(hex)
        self.assertEqual(b"5KHQ6zJtnXr3P99stSh2e2VpwgQwbU5qsMDcJvqwXjQNSQGS6P2", result)

    def test_correct_hex_as_bytes(self):
        hex = "c1421c809f270aa475f16adeaf3dab4fb9d28eaccbf2e1e35ff38cf99609c308"
        result = convert_hex_private_key_to_wif(hex)
        self.assertEqual(b"5KHQ6zJtnXr3P99stSh2e2VpwgQwbU5qsMDcJvqwXjQNSQGS6P2", result)


class TestConvertWifPrivateKeyToHex(unittest.TestCase):
    def test_correct_wif(self):
        wif = "5KHQ6zJtnXr3P99stSh2e2VpwgQwbU5qsMDcJvqwXjQNSQGS6P2"
        result = convert_wif_to_hex_private_key(wif)
        self.assertEqual(b"c1421c809f270aa475f16adeaf3dab4fb9d28eaccbf2e1e35ff38cf99609c308", result)

    def test_correct_wif_as_bytes(self):
        wif = b"5KHQ6zJtnXr3P99stSh2e2VpwgQwbU5qsMDcJvqwXjQNSQGS6P2"
        result = convert_wif_to_hex_private_key(wif)
        self.assertEqual(b"c1421c809f270aa475f16adeaf3dab4fb9d28eaccbf2e1e35ff38cf99609c308", result)

