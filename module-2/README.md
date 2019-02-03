# Satoshi Way: module 2

The aim of week one is to improve some modules of the system to be more bitcoin-like.
* Transactions, constructed in the way Bitcoin network can accept them
* UTXO system
* Updated wallet_cli
* Bitcoin Script implementation

## Setup instructions
* Clone the repository
* Create virtualenv with python3.6+ and activate it (python version currently being used in development is Python 3.6.7 )
* Install all project dependencies, using 
``` 
pip install -r requirements.txt 
```
* Root module-2 directory contains some scripts that should be launched before you begin exploring pitcoin.
* In the separate terminal tab launch api.py with the command 
(this process should run all the time as you work with your pitcoin node)
``` 
python api.py 
```
* Now run initializer.py. This script will create and publish genesis block.
```
python initializer.py
```
That`s it! You can now use wallet-cli or miner-cli.

If you get errors about port being occupied already that is okay. 
The reason for it must be other pitcoin node already running on the computer.

In this case you may want to edit settings.py file inside inner pitcoin folder. 
This file specifies port and host api will use to run.

## API 'GET' routes

During various interactions with cli it can be really useful to know what's happening inside the node. 
Some of the routes below are actually being used by the node itself, but feel free to check out what's out there.

```
/transaction                                            # get list of all transaction included in known blocks
/transaction?txid=txid_of_transaction_as_str            # get tx with specific txid or empty list
/transaction/pendings                                   # get all transactions form the mempool
/transaction/pendings?amount=3                          # get thee transactions from the mining pool (handy for mining purposes)
/transaction/deserialize?data=raw_transaction_as_str    # convert raw transaction to readable format
/chain                                                  # get all chain of the blocks
/chain/block                                            # get last known block
/chain/block?heigth=<int>                               # get block at certain height
/chain/length                                           # get length of the current chain
/node                                                   # get list of all known pitcoin nodes
/balance?address=some_pitcoin_addr                      # get balance for some_pitcoin_addr address
/utxo                                                   # get all unspent outputs
/utxo?address=some_pitcoin_adr                          # get unspent outputs for certain address 
```

## Setting up two nodes interaction
Let's create simple pitcoin testnet consisting of two nodes. Assuming you've already done setup for one node:
* Clone repository once again in separate location.
* Repeat every step as if you were setting the node up first time. 
Be careful: this time you **have to change the port** in `pitcoin_modules/settings.py`, otherwise api.py wont start.
And make sure you run `initializer.py` for this node as well, otherwise api.pi will not work correctly.
* Run miner-cli of the second (newly created) node.

All actions described below assume the case, when more then one block is included in the chain of first (older one) node.
If not, both nodes have chain length equal to one and calling `consensus` command will result nothing.

In this case you want to mine on each of two nodes just to make at least one chain longer than the other one.
Every node will then use longest chain as main one.

The example below assumes, that first node in launched on the default ```5000``` port and the second node runs on port ```5001```.

* Run miner_cli for node at port ```5001```:    
```python miner_cli.py```
* Let your second node know about the first one.  
```(pitcoin-miner-cli) add_node http://127.0.0.1:5000```
* Call consensus and see if new chain gets loaded.
```
(pitcoin_modules-miner-cli) consensus```
Loaded new chain from  http://127.0.0.1:5000  with length  3
```

Great! Right now two nodes share same block history. 
However if one of them mines new block, it will be only passed to *known* nodes. 
In an example above second node (port ```5001```) knows about node at port ```5000```, but not vice versa.

This can be fixed easily:
* Switch to ```miner_cli``` of node at port ```5000```.
* Notify the node about another node out there
```(pitcoin-miner-cli) add_node http://127.0.0.1:5001```

**Important fact about known nodes**: those addresses added by ```add_node``` command are only stored in api.py program memory.
If you relaunch api.py, you have to redo ```add_node``` as just after launch ```api.py``` knows nothing about other pitcoin nodes.

Now to nodes know about each other's existence. 
You can easily make sure it works by mining a new block on one of the two nodes.
The other one will display newly mined block in it's history 
(considering the situation when histories of two nodes were same before mining started)

## Wallet CLI

## Miner CLI

## Testing
Running tests:
```
python -m unittest discover -s pitcoin_modules/tests/
```

Getting coverage information: 
```
coverage run -m --source=pitcoin_modules unittest discover -s pitcoin_modules/tests/
coverage report -m
```