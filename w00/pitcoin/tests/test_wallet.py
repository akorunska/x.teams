import unittest
import numpy as np
from pitcoin.wallet import *


class TestGeneratePrivateKey(unittest.TestCase):
    def test_generated_key_length(self):
        for x in range(100):
            privkey = generate_private_key()
            self.assertEqual(64, len(privkey.encode("utf-8")))

    def test_generated_keys_are_unique(self):
        keys = []
        for x in range(100):
            keys.append(generate_private_key())
        self.assertEqual(len(keys), np.unique(keys).size)

    def test_generated_keys_value_does_not_exseed_order_of_elliptic_curve(self):
        order_of_elliptic_curve = 1.158 * 10 ** 77
        for x in range(100):
            privkey = generate_private_key()
            self.assertTrue(float(int(privkey, 16)) < order_of_elliptic_curve)


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

