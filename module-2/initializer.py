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

def genesis_block_setup():
    blockchain = Blockchain()
    genesis_block = blockchain.genesis_block()
    api_url = "http://" + API_HOST + ":" + API_PORT

    chain = requests.get(api_url + '/chain').json()
    if len(chain) > 0:
        requests.delete(api_url + '/chain')
    requests.post(api_url + '/chain/block', str(genesis_block))


make_sure_path_exists('pitcoin_modules/storage')
genesis_block_setup()
