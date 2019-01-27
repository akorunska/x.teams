import unittest
from pitcoin.settings import PROJECT_ROOT
from pitcoin.storage_handlers.pending_pool import MemPoolStorage
from pitcoin.transaction import Transaction
from pitcoin.transaction import Serializer


class TestPendingPool(unittest.TestCase):
    # tx = Transaction(
    #         "1GFfoqR4Z4BZEy75Nd9CRMTKAev3oukY2Q",
    #         "16hqCUBS1ifCukfodbhTHMpzdqgzvf6HAM",
    #         10
    #     ).sign_transaction("936abdc0429eb4b38a045fcb8f531ff7cf3888c3a83797df5d033106c4ea6a20")

    storage_filepath = PROJECT_ROOT + "/storage/mempool_test.txt"

    def test_adding_to_mempool(self):
        storage = MemPoolStorage(self.storage_filepath)
        storage.delete_all_transactions_from_mempool()
        tx = Transaction("sndr", "rspt", 20)
        storage.add_transaction_to_mempool(tx)

        tx_list = storage.get_all_transactions()
        self.assertTrue(tx in tx_list)

    def test_adding_correct_serialized_tx_to_mempool(self):
        storage = MemPoolStorage(self.storage_filepath)
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
        storage = MemPoolStorage(self.storage_filepath)
        storage.delete_all_transactions_from_mempool()
        tx = Transaction("sndr", "rspt", 20)
        storage.add_serialized_transaction_to_mempool(Serializer.serialize_transaction(tx))

        tx_list = storage.get_all_transactions()
        self.assertFalse(tx in tx_list)

    def test_deleting_last_transaction(self):
        storage = MemPoolStorage(self.storage_filepath)
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
        storage = MemPoolStorage(self.storage_filepath)
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

    def test_get_three_last_tx_empty_list(self):
        storage = MemPoolStorage(self.storage_filepath)
        storage.delete_all_transactions_from_mempool()

        storage.get_three_first_transactions()
        self.assertEqual(0, storage.get_transactions_count())

    def test_get_three_last_tx_two_items_list(self):
        storage = MemPoolStorage(self.storage_filepath)
        storage.delete_all_transactions_from_mempool()
        tx1 = Transaction("sndr1", "rspt1", 20)
        tx2 = Transaction("sndr2", "rspt2", 20)
        storage.add_transaction_to_mempool(tx1)
        storage.add_transaction_to_mempool(tx2)

        last_tx_list = storage.get_three_first_transactions()
        self.assertEqual(2, len(last_tx_list))
        self.assertTrue(tx1 in last_tx_list)
        self.assertTrue(tx2 in last_tx_list)

    def test_get_three_last_tx_many_items_list(self):
        storage = MemPoolStorage(self.storage_filepath)
        storage.delete_all_transactions_from_mempool()
        tx1 = Transaction("sndr1", "rspt1", 20)
        tx2 = Transaction("sndr2", "rspt2", 20)
        tx3 = Transaction("sndr3", "rspt3", 20)
        tx4 = Transaction("sndr4", "rspt4", 20)
        storage.add_transaction_to_mempool(tx1)
        storage.add_transaction_to_mempool(tx2)
        storage.add_transaction_to_mempool(tx3)
        storage.add_transaction_to_mempool(tx4)

        last_tx_list = storage.get_three_first_transactions()
        self.assertEqual(3, len(last_tx_list))
        self.assertTrue(tx1 in last_tx_list)
        self.assertTrue(tx2 in last_tx_list)
        self.assertTrue(tx3 in last_tx_list)
        self.assertFalse(tx4 in last_tx_list)

