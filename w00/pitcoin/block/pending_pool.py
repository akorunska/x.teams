from pitcoin.transaction import Deserializer
from pitcoin.transaction.tx_validator import check_tx_validity
import pickle
from pathlib import Path

# storage_filepath = '../storage/mempool.txt'


class Storage:
    def __init__(self, filepath='../storage/mempool.txt'):
        self.storage_filepath = filepath

    def get_validated_deserialized_transaction(data):
        tx = Deserializer.deserialize_transaction(data)
        if check_tx_validity(tx):
            return tx
        else:
            return None

    def add_transaction_to_mempool(self, tx):
        tx_list = []
        if not Path(self.storage_filepath).is_file():
            Path(self.storage_filepath).touch()
            tx_list = []
        else:
            with open(self.storage_filepath, 'rb') as fp:
                tx_list = pickle.load(fp)

        tx_list.append(tx)
        with open(self.storage_filepath, 'wb+') as fp:
            pickle.dump(tx_list, fp)

    def delete_last_transaction_from_mempool(self):
        tx_list = []
        if not Path(self.storage_filepath).is_file():
            return
        else:
            with open(self.storage_filepath, 'rb') as fp:
                tx_list = pickle.load(fp)

        tx_list.pop()
        with open(self.storage_filepath, 'wb+') as fp:
            pickle.dump(tx_list, fp)

    def delete_all_transactions_from_mempool(self):
        tx_list = []

        with open(self.storage_filepath, 'wb+') as fp:
            pickle.dump(tx_list, fp)

    def get_all_transactions(self):
        tx_list = []
        if not Path(self.storage_filepath).is_file():
            return
        else:
            with open(self.storage_filepath, 'rb') as fp:
                tx_list = pickle.load(fp)

        return tx_list

    def get_three_last_transactions(self):
        tx_list = []
        if not Path(self.storage_filepath).is_file():
            return
        else:
            with open(self.storage_filepath, 'rb') as fp:
                tx_list = pickle.load(fp)

        if len(tx_list) >= 4:
            return tx_list[len(tx_list) - 3: len(tx_list)]
        else:
            return tx_list


# 00221CAEuYPgEYnyepAF51AiKdCvPfTgjoMieU1GMRXMjXGVxC43GtonDHJ5YY8jQp2RKHEA50e829ca678c60031a11b990fea865e03ba35d0579aa62750b918b98c4b935d803ecc57a4bb2fc2ab1193a87fca5386d71516aca89df267fc907bcb3b84d396a0580fae8ca3bbf6b7a016d5f247feb89efbd0412e84524d0746520bd45ea45112e4ce76474636eb36f67b5407249742ee54b97322184135fe0251511f5149328

if __name__ == '__main__':
    tx = Storage.get_validated_deserialized_transaction(b'00091GFfoqR4Z4BZEy75Nd9CRMTKAev3oukY2Q1GMRXMjXGVxC43GtonDHJ5YY8jQp2RKHEA50e829ca678c60031a11b990fea865e03ba35d0579aa62750b918b98c4b935d803ecc57a4bb2fc2ab1193a87fca5386d71516aca89df267fc907bcb3b84d396a7388be31865e41be006c14ef7033be6301105563f1bf16cc257fc7af43630bc735b075e1be42c9a37799ed69a1e49de6a14d3390550718e78db3dbd454a08021')
    # Storage.add_transaction_to_mempool(tx)
    # Storage.delete_last_transaction_from_mempool()

    Storage.delete_all_transactions_from_mempool()

    txs = Storage.get_three_last_transactions()
    for t in txs:
        print(t)