import unittest
from pitcoin.block import Storage
from pitcoin.transaction import Transaction


class TestPendingPool(unittest.TestCase):
    def test_adding_to_mempool(self):
        storage = Storage("../storage/mempool_test.txt")
        storage.delete_all_transactions_from_mempool()
        tx = Transaction("sndr", "rspt", 20)
        storage.add_transaction_to_mempool(tx)

        tx_list = storage.get_all_transactions()
        self.assertTrue(tx in tx_list)



