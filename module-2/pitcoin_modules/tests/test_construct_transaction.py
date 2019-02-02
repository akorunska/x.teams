import unittest
from pitcoin_modules.wallet import *


class TestConstructTransactionLockingScript(unittest.TestCase):
    def test_basic_construction(self):
        address = "1GFfoqR4Z4BZEy75Nd9CRMTKAev3oukY2Q"
        script = construct_transaction_locking_script(address)
        self.assertEqual("76a914a7501ae704b299ca3eb5bec10f8e3d8c3bb5cae088ac", script)
