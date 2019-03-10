import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    mnemonic: '',
    accounts: [],
    loggedIn: false
  },
  mutations: {
    importMnemonic(state, { mnemonic }) {
      state.loggedIn = true;
      state.mnemonic = mnemonic;

      let bip39 = require("bip39");
      let hdkey = require('ethereumjs-wallet/hdkey');
      let hdwallet = hdkey.fromMasterSeed(bip39.mnemonicToSeed(mnemonic));
      let wallet_hdpath = "m/44'/60'/0'/0/";

      for (let i = 0; i < 10; i++) {
        let wallet = hdwallet.derivePath(wallet_hdpath + i).getWallet();
        let address = '0x' + wallet.getAddress().toString("hex");
        let privateKey = wallet.getPrivateKey().toString("hex");
        state.accounts.push({address: address, privateKey: privateKey});
      }

    },
    logOut(state) {
      state.loggedIn = false;
      state.mnemonic = '';
    }
  }
});


// function generateAddressesFromSeed(seed, count) {
//   let bip39 = require("bip39");
//   let hdkey = require('ethereumjs-wallet/hdkey');
//   let hdwallet = hdkey.fromMasterSeed(bip39.mnemonicToSeed(seed));
//   let wallet_hdpath = "m/44'/60'/0'/0/";
//
//   let accounts = [];
//   for (let i = 0; i < 10; i++) {
//
//     let wallet = hdwallet.derivePath(wallet_hdpath + i).getWallet();
//     let address = '0x' + wallet.getAddress().toString("hex");
//     let privateKey = wallet.getPrivateKey().toString("hex");
//     accounts.push({address: address, privateKey: privateKey});
//   }
//
//   return accounts;
// }
