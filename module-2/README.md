# Satoshi Way: module 2

The aim of second week is to improve some modules of the system to be more bitcoin-like.
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

When typing ```help``` inside ```wallet_cli``` following list of command appears.
```
balance  broadcast  help  import  new  quit  remember_privkey  send
```

Every command above is documented. 
It means that by typing ```help command_name``` in the cli you can see small explanation + usage info.

**Example of workflow with wallet_cli**

* First we start by getting help about the system.
```
(pitcoin-wallet-cli) help

Documented commands (type help <topic>):
========================================
balance  broadcast  help  import  new  quit  remember_privkey  send
```

You can also check out usage information for every specific command.

* Let's create new address by calling command ```new```.
If you want this address to be saved in a ```pitcoin_modules/address``` file, call command with ```-a``` option.

**Important note:** If you rewrite the address in ```pitcoin_modules/address``` and you also wish to mine pitcoins using this address,
update ```pitcoin_modules/minerkey``` with corresponding private key in hex format.
```
(pitcoin-wallet-cli) new
hex private key |  676595aad53004ad4b9b0d32e9651d5360ecd83e65402e4df44c0f94e87dc5ba
wif private key |  5JbpiPQo1Fo3eNUrTBEoqELABuc7Fj2ntf6ea9etvjREVQsdL66
public key      |  041ac2dabe2ebb4a96b4b887beee9b7d0ddb11aa63418c23211ce2e191371ae9f7b809e92aeeb610f8c3c51a72192a96072509d3b3ffdc11bac262f1713e1381b9
pitcoin address |  14wc26VyerPrjrorSguL9JngNcTHc8esya
```

* It is also possible to use compressed public keys. To do so, use ```-c``` option.
```
(pitcoin-wallet-cli) new -c
using compressed public key for address creation
hex private key |  f04656230e354565e5185b89b14b42e223977dd7ce45994682f905fd62dc1a4e
wif private key |  5Ke75TAzbrZkCNTNqk8NRK3R56RsH2xtuo7kiykf9X3VhFKQq7m
public key      |  0341ac7dc06cfbb4e6d5372c54abab81e506e43f9c3905b69afd82b85b22570c79
pitcoin address |  1LsmyP2Z6snhNVNgeFMSKt5J6oBq8WLDwG
```

* You can use some existing private key by importing them it wif format.
Flags ```-a``` and ```-c``` work for ```import``` command as well.

```
(pitcoin-wallet-cli) import pitcoin_modules/minerkey
hex private key |  936abdc0429eb4b38a045fcb8f531ff7cf3888c3a83797df5d033106c4ea6a20
wif private key |  5JwD9eKwBsYQJTc2Sx9wFa1jYvb7WRHespU56J6ZtWXipb1kgLN
public key      |  0450e829ca678c60031a11b990fea865e03ba35d0579aa62750b918b98c4b935d803ecc57a4bb2fc2ab1193a87fca5386d71516aca89df267fc907bcb3b84d396a
pitcoin address |  1NERjvtBxL5ErAKhCC3mfgWbp3QMd8y6ba
```

* Let's try to ```send``` some pitcoins. It will only work if we specify private key first.
```
(pitcoin-wallet-cli) send
please, specify your private key using <remember_privkey> command before calling send
```

* ```remember_privkey``` command is going to tell miner_cli which private key to use in transactions. 
Note that private key you specify must correspond with address in ```pitcoin_modules/address```.
```
(pitcoin-wallet-cli) remember_privkey 936abdc0429eb4b38a045fcb8f531ff7cf3888c3a83797df5d033106c4ea6a20
```

* After specifying private key you can call send command. 
Hex string below is pitcoin raw_transaction. Copy it, so you can use it in your next step.
```
(pitcoin-wallet-cli) send 1KV2VGQiTB1B5KPEyyEPvifcqfS6PUxdxj 900
{"version": 1, "inputs": [{"txid": "07c0efe33946c5f81b5a86d79eda89e47979d4796d5ec675a9fccde7c31c4f50", "vout": 1, "scriptsig": "404bb493aa8509356c1295c65acd3a44c339729d865422a47cb15631cda545ee3fc2eb86b418a5bb90202040430b723fdbf8429ff232bfa521c25da09539644093410450e829ca678c60031a11b990fea865e03ba35d0579aa62750b918b98c4b935d803ecc57a4bb2fc2ab1193a87fca5386d71516aca89df267fc907bcb3b84d396a"}], "outputs": [{"value": 900, "scriptpubkey": "76a914cabf271134a5f9228132598c8b4e6ad4586532f888ac", "txid": "1423215db125380dd21051c0d22f31fd4be2a25794b8789796343f4015c1baff", "vout": 1}, {"value": 4999999100, "scriptpubkey": "76a914e8e4b375038b0a1a1dc70543eab7ea6ce279df4388ac", "txid": "1423215db125380dd21051c0d22f31fd4be2a25794b8789796343f4015c1baff", "vout": 2}], "locktime": 0, "txid": "1423215db125380dd21051c0d22f31fd4be2a25794b8789796343f4015c1baff"}
0100000001504f1cc3e7cdfca975c65e6d79d47979e489da9ed7865a1bf8c54639e3efc0070100000083404bb493aa8509356c1295c65acd3a44c339729d865422a47cb15631cda545ee3fc2eb86b418a5bb90202040430b723fdbf8429ff232bfa521c25da09539644093410450e829ca678c60031a11b990fea865e03ba35d0579aa62750b918b98c4b935d803ecc57a4bb2fc2ab1193a87fca5386d71516aca89df267fc907bcb3b84d396affffffff0284030000000000001976a914cabf271134a5f9228132598c8b4e6ad4586532f888ac7cee052a010000001976a914e8e4b375038b0a1a1dc70543eab7ea6ce279df4388ac00000000 
```

* It is time to broadcast your transaction to the network.
Use hex string from previous step as the parameter for this command.
You will either get False of True result, depending on if transaction was successfully accepted by node's mempool.
```
(pitcoin-wallet-cli) broadcast 0100000001504f1cc3e7cdfca975c65e6d79d47979e489da9ed7865a1bf8c54639e3efc0070100000083404bb493aa8509356c1295c65acd3a44c339729d865422a47cb15631cda545ee3fc2eb86b418a5bb90202040430b723fdbf8429ff232bfa521c25da09539644093410450e829ca678c60031a11b990fea865e03ba35d0579aa62750b918b98c4b935d803ecc57a4bb2fc2ab1193a87fca5386d71516aca89df267fc907bcb3b84d396affffffff0284030000000000001976a914cabf271134a5f9228132598c8b4e6ad4586532f888ac7cee052a010000001976a914e8e4b375038b0a1a1dc70543eab7ea6ce279df4388ac00000000
{'result': True} 
```
If broadcasting returned True, you can check out API ```http://127.0.0.1:port/transaction/pendings``` and find your transaction there.

* Finally, you can check balance of certain address.
Note that transaction must necessarily be included in the block before being inculed in calculating balance.
```
(pitcoin-wallet-cli) balance 1KV2VGQiTB1B5KPEyyEPvifcqfS6PUxdxj
900
```

* Once you're done, type ```quit``` to exit wallet_cli.
```
(pitcoin-wallet-cli) quit
Thank you for using pitcoin-wallet-cli
```


## Miner CLI

**Important info about using this system as a miner**

You must provide file called ```minerkey``` inside ```pitcoin_modules``` folder.
Initially this file exists in the repo and contains sample private key in hex format. 
If you with to change it, edit this file along with file ```pitcoin_modules/address```, 
that must contain corresponding address in mainnet format.

* Getting help about the system:

(pitcoin-miner-cli) help
```
Documented commands (type help <topic>):
========================================
add_node  consensus  help  mine  quit
```

* Adding node to the list of known nodes:
```
(pitcoin_modules-miner-cli) add_node http://127.0.0.1:5002
```

* Switching to the longest valid chain among known nodes:
```
(pitcoin_modules-miner-cli) consensus
Loaded new chain from  http://127.0.0.1:5000  with length  3
```

* Calling ```mine```:
```
(pitcoin-miner-cli) mine
block was mined and broadcasted to other nodes
hash of the new block:  0046cc50bc59bcbcb1adc5a5b45ee0ae703e00418f51706583e1d39f05af3ef1
```

* Once you're done, type ```quit``` to exit miner_cli.
```
(pitcoin_modules-miner-cli) quit
Thank you for using pitcoin-miner-clii
```

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