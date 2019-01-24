import unittest
from pitcoin.block import Storage
from pitcoin.transaction import Transaction
from pitcoin.transaction import Serializer


class TestPendingPool(unittest.TestCase):
    # tx = Transaction(
    #         "1GFfoqR4Z4BZEy75Nd9CRMTKAev3oukY2Q",
    #         "16hqCUBS1ifCukfodbhTHMpzdqgzvf6HAM",
    #         10
    #     ).sign_transaction("936abdc0429eb4b38a045fcb8f531ff7cf3888c3a83797df5d033106c4ea6a20")

    def test_adding_to_mempool(self):
        storage = Storage("../storage/mempool_test.txt")
        storage.delete_all_transactions_from_mempool()
        tx = Transaction("sndr", "rspt", 20)
        storage.add_transaction_to_mempool(tx)

        tx_list = storage.get_all_transactions()
        self.assertTrue(tx in tx_list)

    def test_adding_correct_serialized_tx_to_mempool(self):
        storage = Storage("../storage/mempool_test.txt")
        storage.delete_all_transactions_from_mempool()
        tx = Transaction(
            "1GFfoqR4Z4BZEy75Nd9CRMTKAev3oukY2Q",
            "16hqCUBS1ifCukfodbhTHMpzdqgzvf6HAM",
            10
        )
        tx.sign_transaction("936abdc0429eb4b38a045fcb8f531ff7cf3888c3a83797df5d033106c4ea6a20")
        storage.add_serialized_transaction_to_mempool(Serializer.serialize_transaction(tx))

        tx_list = storage.get_all_transactions()
        self.assertTrue(tx in tx_list)

    def test_adding_incorrect_serialized_tx_to_mempool(self):
        storage = Storage("../storage/mempool_test.txt")
        storage.delete_all_transactions_from_mempool()
        tx = Transaction("sndr", "rspt", 20)
        storage.add_serialized_transaction_to_mempool(Serializer.serialize_transaction(tx))

        tx_list = storage.get_all_transactions()
        self.assertFalse(tx in tx_list)

    def test_deleting_last_transaction(self):
        storage = Storage("../storage/mempool_test.txt")
        storage.delete_all_transactions_from_mempool()
        tx1 = Transaction("sndr", "rspt", 20)
        tx2 = Transaction("sndr1", "rspt2", 20)
        tx3 = Transaction("sndr2", "rspt2", 20)
        storage.add_transaction_to_mempool(tx1)
        storage.add_transaction_to_mempool(tx2)
        storage.add_transaction_to_mempool(tx3)

        self.assertEqual(3, storage.get_transactions_count())

        storage.delete_last_transaction_from_mempool()
        self.assertEqual(2, storage.get_transactions_count())

        tx_list = storage.get_all_transactions()
        self.assertFalse(tx3 in tx_list)

    def test_deleting_all_transactions(self):
        storage = Storage("../storage/mempool_test.txt")
        storage.delete_all_transactions_from_mempool()
        tx1 = Transaction("sndr", "rspt", 20)
        tx2 = Transaction("sndr1", "rspt2", 20)
        tx3 = Transaction("sndr2", "rspt2", 20)
        storage.add_transaction_to_mempool(tx1)
        storage.add_transaction_to_mempool(tx2)
        storage.add_transaction_to_mempool(tx3)

        self.assertEqual(3, storage.get_transactions_count())

        storage.delete_all_transactions_from_mempool()
        self.assertEqual(0, storage.get_transactions_count())

        tx_list = storage.get_all_transactions()
        self.assertFalse(tx1 in tx_list)
        self.assertFalse(tx2 in tx_list)
        self.assertFalse(tx3 in tx_list)

