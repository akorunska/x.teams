from pitcoin.transaction import Deserializer, Transaction
from pitcoin.transaction.tx_validator import check_tx_validity
import pickle
from pathlib import Path
from pitcoin import PROJECT_ROOT


class Storage:
    def __init__(self, filepath=PROJECT_ROOT+'/storage/mempool.txt'):
        self.storage_filepath = filepath

    def get_validated_deserialized_transaction(self, data):
        tx = Deserializer.deserialize_transaction(data)
        if check_tx_validity(tx):
            return tx
        else:
            return None

    def add_serialized_transaction_to_mempool(self, data):
        tx = self.get_validated_deserialized_transaction(data)
        if tx is None:
            return False
        self.add_transaction_to_mempool(tx)
        return True

    def get_all_transactions(self):
        tx_list = []
        if not Path(self.storage_filepath).is_file():
            Path(self.storage_filepath).touch()
        else:
            with open(self.storage_filepath, 'rb') as fp:
                try:
                    tx_list = tx_list = pickle.load(fp)
                except EOFError:
                    tx_list = []
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
        return True

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


if __name__ == '__main__':
    st = Storage()
    tx_list = st.get_all_transactions()
    tx = Transaction(
        "1GFfoqR4Z4BZEy75Nd9CRMTKAev3oukY2Q",
        "16hqCUBS1ifCukfodbhTHMpzdqgzvf6HAM",
        10
    )
    tx.sign_transaction("936abdc0429eb4b38a045fcb8f531ff7cf3888c3a83797df5d033106c4ea6a20")

    # st.add_transaction_to_mempool(tx)
    tx_list = st.get_all_transactions()
    for tx in tx_list:
        print(tx)
