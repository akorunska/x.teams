# Satoshi Way: module 1

The aim of week one is to prototype a simple bitcoin-like system step-by-step using python.

Key points of what should be implemented:
* cryptography 
* transactions creation, serialization, deserialization and validation
* mempool for storing unconfirmed transactions
* block structure, calculating merkle root
* mining and PoW
* several possible roles at the system: simple user and the miner
* creating the testnet
* wallet-cli and miner-cli
* test coverage for different system modules

## Setup instructions
* Clone the repository
* Create virtualenv with python3 and activate it
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
/transaction/pendings
/transaction/pendings?amount=3
/chain
/chain/block
/chain/block?heigth=<int>
/chain/length
/node
/balance
```

##
Running tests:
```
python -m unittest discover -s pitcoin/tests/
```

Getting coverage information: 
```
coverage run -m --source=. unittest discover -s pitcoin/tests/
coverage report -m
```