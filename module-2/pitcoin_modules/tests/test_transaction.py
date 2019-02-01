import unittest
from pitcoin_modules.transaction import *
from pitcoin_modules.transaction.input import Input
from pitcoin_modules.transaction.output import Output


class TestTransaction(unittest.TestCase):
    def test_raw_transaction_basic(self):
        inputs = [Input(
            "7967a5185e907a25225574544c31f7b059c1a191d65b53dcc1554d339c4f9efc",
            "47304402206a2eb16b7b92051d0fa38c133e67684ed064effada1d7f925c842da401d4f22702201f196b10e6e4b4a9fff948e5c5d71ec5da53e90529c8dbd122bff2b1d21dc8a90121039b7bcd0824b9a9164f7ba098408e63e5b7e3cf90835cceb19868f54f8961a825"
        )]
        outputs = [Output(
            2207563,
            "76a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac"
        )]
        tx = Transaction(inputs, outputs, locktime=0)
        print(tx)

        raw_tx = "01000000017967a5185e907a25225574544c31f7b059c1a191d65b53dcc1554d339c4f9efc010000006a47304402206a2eb16b7b92051d0fa38c133e67684ed064effada1d7f925c842da401d4f22702201f196b10e6e4b4a9fff948e5c5d71ec5da53e90529c8dbd122bff2b1d21dc8a90121039b7bcd0824b9a9164f7ba098408e63e5b7e3cf90835cceb19868f54f8961a825ffffffff014baf2100000000001976a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac00000000"
        # self.assertEqual(raw_tx, Serializer.serialize_transaction(tx))