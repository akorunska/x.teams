import unittest
from pitcoin_modules.script import *


class TestScript(unittest.TestCase):
    def test_script_correct(self):
        s = "4022e11f044267c37f76b738ab9a046e436cee8a339e7f7a9dd8ed6de0f95051ed4046b60ead4d9db9a1a532dace2cf5b03f7569678c3bba74a7284efd4ba485ea410450e829ca678c60031a11b990fea865e03ba35d0579aa62750b918b98c4b935d803ecc57a4bb2fc2ab1193a87fca5386d71516aca89df267fc907bcb3b84d396a76a914e8e4b375038b0a1a1dc70543eab7ea6ce279df4388ac"
        self.assertTrue(run_script(s, "f0973390e55e765a468b5e2af16f5b586e38f33207ba4f6e657615ba5e46b3a2"))

