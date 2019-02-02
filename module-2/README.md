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
* Now enter the pitcoin directory. It contains some scripts that should be launched before you begin exploring pitcoin.
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

```
/transaction   # get list of all transaction included in known blocks
/transaction?txid=txid_of_transaction_as_str    # get tx with specific txid or empty list
/transaction/pendings
/transaction/pendings?amount=3
/transaction/deserialize?data=raw_transaction_as_str    # convert raw transaction to readable format
/chain
/chain/block    # returns last known block
/chain/block?heigth=<int>
/chain/length
/node
/balance?address=some_pitcoin_adr
/utxo
/utxo?address=some_pitcoin_adr
```

##
Running tests:
```
python -m unittest discover -s pitcoin_modules/tests/
```

Getting coverage information: 
```
coverage run -m --source=pitcoin_modules unittest discover -s pitcoin_modules/tests/
coverage report -m
```