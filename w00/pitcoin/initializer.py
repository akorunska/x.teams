import requests

from pitcoin.blockchain import Blockchain
from pitcoin.settings import *

def genesis_block_setup():
    blockchain = Blockchain()
    genesis_block = blockchain.genesis_block()
    api_url = "http://" + API_HOST + ":" + API_PORT

    chain = requests.get(api_url + '/chain').json()
    if len(chain) > 0:
        requests.delete(api_url + '/chain')
    requests.post(api_url + '/chain/block', str(genesis_block))


genesis_block_setup()
