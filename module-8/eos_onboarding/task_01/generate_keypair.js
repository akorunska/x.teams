let {PrivateKey, PublicKey, Signature, Aes, key_utils, config} = require('eosjs-ecc')

let privateWif;

PrivateKey.randomKey().then(privateKey => {
    privateWif = privateKey.toString();

    let pubkey = PrivateKey.fromString(privateWif).toPublic().toString();

    console.log(privateWif);
    console.log(pubkey);
});


