# PART 01: EOS Onboarding


### get EOS  chain_id
```
$ cleos get info
{
  "server_version": "ea08cfd3",
  "chain_id": "cf057bbfb72640471fd910bcb67639c22df9f92470936cddc1ade0e2f2e7dc4f",
  "head_block_num": 9714,
  "last_irreversible_block_num": 9713,
  "last_irreversible_block_id": "000025f1db4737019697e11b43ace86eeaa1d57431aae51faad4877b1b6531b2",
  "head_block_id": "000025f29f125cbfd221c1015edca6cdbe0e7ca09c9d13cbab61a45b8418e2b1",
  "head_block_time": "2019-03-16T17:38:49.000",
  "head_block_producer": "eosio",
  "virtual_block_cpu_limit": 200000000,
  "virtual_block_net_limit": 1048576000,
  "block_cpu_limit": 199900,
  "block_net_limit": 1048576,
  "server_version_string": "v1.5.0"
}


```

### generate pair of keys using eosjs
generate_keypair.js can be found in eos_onboarding/task_01
```
$ node generate_keypair.js 
5JNFM5TmWj1Lzn8Recg5NuCryEBtQnrEYed5Q2WK2qkUBL6dVnc
EOS763scBTBemUCCfkNKK4PmwV4c1R7ErkVzXscxMM4NkDFYBwHC3
```

### get all Block Producers (BPs) in the network

```
$ cleos -u http://api.eosnewyork.io:80 system listproducers
Producer      Producer key                                              Url                                                         Scaled votes
eoslaomaocom  EOS8QgURqo875qu3a8vgZ58qBeu2cTehe9zAWRfpdCXAQipicu1Fi     https://eoslaomao.com                                       0,0201
eosliquideos  EOS4v1n2j5kXbCum8LLEc8zQLpeLK9rKVFmsUgLCWgMDN38P6PcrW     http://vote.liquideos.com                                   0,0192
eoshuobipool  EOS5XKswW26cR5VQeDGwgNb5aixv1AMcKkdDNrC59KzNSBfnH6TR7     http://eoshuobipool.com                                     0,0190
starteosiobp  EOS4wZZXm994byKANLuwHD6tV3R3Mu3ktc41aSVXCBaGnXJZJ4pwF     https://www.starteos.io                                     0,0186
eosiosg11111  EOS7zVBQMhV7dZ5zRQwBgDmmbFCHA6YcmwW6Dq5CePGpqLR1ZsVAc     https://eosio.sg                                            0,0183
zbeosbp11111  EOS7rhgVPWWyfMqjSbNdndtCK8Gkza3xnDbUupsPLMZ6gjfQ4nX81     https://www.zbeos.com                                       0,0180
atticlabeosb  EOS7PfA3A4UdfMu2wKbuXdbHn8EWAxbMnFoFWui4X2zsr2oPwdQJP     https://atticlab.net                                        0,0180
helloeoscnbp  EOS79cHpaEittzgJWgj79tdRhgzLEWy8wXmmQ3fL7kkDjmYYiGNet     https://www.helloeos.com.cn                                 0,0180
jedaaaaaaaaa  EOS6nB9Ar5sghWjqk27bszCiA9zxQtXZCaAaEkf2nwUm9iP5MEJTT     https://www.eosjapan.org                                    0,0178

```

### install scatter and cleos, create accounts in testnet (find a purse that supports testnet, find a way to create accounts in testnet, get yourself testEOS)

![akorunska115 jungel balance](pictures/jungle_balance_akorunska115.png)

### find the top 21 (eos system table)
First 21 are top ones :)
```
$ cleos -u http://api.eosnewyork.io:80 system listproducers

```

### 

```

```

### 

```

```

### 

```

```


