import unittest
from pitcoin_modules.transaction import Transaction, Serializer, Output, Input


class TestRawWitnessTransaction(unittest.TestCase):
    def test_raw_transaction_creation(self):
        inputs = [Input(
            "fc9e4f9c334d55c1dc535bd691a1c159b0f7314c54745522257a905e18a56779",
            1,
            ""
        )]
        outputs = [Output(
            2207563,
            "0014db4d1141d0048b1ed15839d0b7a4c488cd368b0e"
        )]
        witness = ["47304402206a2eb16b7b92051d0fa38c133e67684ed064effada1d7f925c842da401d4f22702201f196b10e6e4b4a9fff948e5c5d71ec5da53e90529c8dbd122bff2b1d21dc8a90121039b7bcd0824b9a9164f7ba098408e63e5b7e3cf90835cceb19868f54f8961a825"]
        tx = Transaction(inputs, outputs, locktime=0, witness=witness, version=2)

        # raw_tx = "01000000017967a5185e907a25225574544c31f7b059c1a191d65b53dcc1554d339c4f9efc010000006a47304402206a2eb16b7b92051d0fa38c133e67684ed064effada1d7f925c842da401d4f22702201f196b10e6e4b4a9fff948e5c5d71ec5da53e90529c8dbd122bff2b1d21dc8a90121039b7bcd0824b9a9164f7ba098408e63e5b7e3cf90835cceb19868f54f8961a825ffffffff014baf2100000000001976a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac00000000"
        # self.assertEqual(raw_tx, Serializer.serialize_transaction(tx))
        print(Serializer.serialize_sw_transaction(tx))
