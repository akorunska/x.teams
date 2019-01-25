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

#

Running tests from root directory:
```
python -m unittest discover -s pitcoin/tests/
```

Getting coverage information: 
```
coverage run -m --source=pitcoin unittest discover -s pitcoin/tests/
coverage report -m
```