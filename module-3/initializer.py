import errno
import os
import requests
from pitcoin_modules.blockchain import Blockchain
from pitcoin_modules.settings import *


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def clear_storage(path):
    try:
        os.remove(path + ".blocks.txt")
    except OSError:
        pass
    try:
        os.remove(path + ".mempool.txt")
    except OSError:
        pass
    try:
        os.remove(path + ".utxopool.txt")
    except OSError:
        pass


def genesis_block_setup():
    blockchain = Blockchain()
    genesis_block = blockchain.genesis_block()
    api_url = "http://" + API_HOST + ":" + API_PORT

    requests.post(api_url + '/chain/block', str(genesis_block))


def get_known_nodes():
    pass



make_sure_path_exists('pitcoin_modules/storage/')
clear_storage('pitcoin_modules/storage/')

# get all known nodes from the config file
# if there are no nodes, create own genesis block
genesis_block_setup()
