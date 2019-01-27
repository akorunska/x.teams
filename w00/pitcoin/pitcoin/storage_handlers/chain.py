from pitcoin.block import Block
from pitcoin.transaction import Deserializer, Transaction
from pitcoin.transaction.tx_validator import check_tx_validity
import pickle
from pathlib import Path
from pitcoin import PROJECT_ROOT


class BlocksStorage:
    def __init__(self, filepath=PROJECT_ROOT+'/storage/.blocks.txt'):
        self.storage_filepath = filepath

    def get_all_blocks(self):
        blocks_list = []
        if not Path(self.storage_filepath).is_file():
            Path(self.storage_filepath).touch()
        else:
            with open(self.storage_filepath, 'rb') as fp:
                try:
                    blocks_list = pickle.load(fp)
                except EOFError:
                    blocks_list = []
        return blocks_list

    def add_block_to_storage(self, b: Block):
        blocks_list = self.get_all_blocks()
        # todo check block`s validity
        if len(blocks_list) != 0:
            if blocks_list[-1].hash_value != b.previous_hash:
                return False
        blocks_list.append(b)
        with open(self.storage_filepath, 'wb+') as fp:
            pickle.dump(blocks_list, fp)
        return True

    def get_last_block(self):
        blocks_list = self.get_all_blocks()
        if len(blocks_list) == 0:
            return None
        return blocks_list[-1]

    def delete_all_blocks_from_mempool(self):
        blocks_list = []
        with open(self.storage_filepath, 'wb+') as fp:
            pickle.dump(blocks_list, fp)
        return True

    def get_blocks_count(self):
        blocks_list = self.get_all_blocks()
        return len(blocks_list)
