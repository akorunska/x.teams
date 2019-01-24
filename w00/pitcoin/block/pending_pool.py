from pitcoin.transaction import Deserializer
from pitcoin.transaction.tx_validator import check_tx_validity
import pickle
from pathlib import Path


class Storage:
    def __init__(self, filepath='../storage/mempool.txt'):
        self.storage_filepath = filepath

    def get_validated_deserialized_transaction(self, data):
        tx = Deserializer.deserialize_transaction(data)
        if check_tx_validity(tx):
            return tx
        else:
            return None

    def add_serialized_transaction_to_mempool(self, data):
        tx = self.get_validated_deserialized_transaction(data)
        self.add_transaction_to_mempool(tx)

    def get_all_transactions(self):
        tx_list = []
        if not Path(self.storage_filepath).is_file():
            Path(self.storage_filepath).touch()
        else:
            with open(self.storage_filepath, 'rb') as fp:
                tx_list = pickle.load(fp)
        return tx_list

    def add_transaction_to_mempool(self, tx):
        tx_list = self.get_all_transactions()
        tx_list.append(tx)
        with open(self.storage_filepath, 'wb+') as fp:
            pickle.dump(tx_list, fp)

    def delete_last_transaction_from_mempool(self):
        tx_list = self.get_all_transactions()
        tx_list.pop()
        with open(self.storage_filepath, 'wb+') as fp:
            pickle.dump(tx_list, fp)

    def delete_all_transactions_from_mempool(self):
        tx_list = []
        with open(self.storage_filepath, 'wb+') as fp:
            pickle.dump(tx_list, fp)

    def get_three_last_transactions(self):
        tx_list = self.get_all_transactions()

        if len(tx_list) >= 4:
            return tx_list[len(tx_list) - 3: len(tx_list)]
        else:
            return tx_list

    def get_transactions_count(self):
        tx_list = self.get_all_transactions()
        return len(tx_list)
