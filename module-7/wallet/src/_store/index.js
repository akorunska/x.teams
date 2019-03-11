import Vue from 'vue'
import Vuex from 'vuex'
import Clipboard from 'v-clipboard'

Vue.use(Vuex);
Vue.use(Clipboard);

export default new Vuex.Store({
  state: {
    mnemonic: '',
    accounts: [],
    activeAccountIndex: 0,
    loggedIn: false,
  },
  mutations: {
    importMnemonic(state, { mnemonic }) {
      state.loggedIn = true;
      state.mnemonic = mnemonic;

      let bip39 = require("bip39");
      let hdkey = require('ethereumjs-wallet/hdkey');
      let hdwallet = hdkey.fromMasterSeed(bip39.mnemonicToSeed(mnemonic));
      let wallet_hdpath = "m/44'/60'/0'/0/";

      for (let i = 0; i < 3; i++) {
        let wallet = hdwallet.derivePath(wallet_hdpath + i).getWallet();
        let address = '0x' + wallet.getAddress().toString("hex");
        let privateKey = wallet.getPrivateKey().toString("hex");
        state.accounts.push(
          {
            address: address,
            privateKey: privateKey,
            index: i,
          });
      }
      state.accounts.activeAccountIndex = 0;
    },
    generateNewAccount(state) {
      let i = state.accounts.length;

      let bip39 = require("bip39");
      let hdkey = require('ethereumjs-wallet/hdkey');
      let hdwallet = hdkey.fromMasterSeed(bip39.mnemonicToSeed(state.mnemonic));
      let wallet_hdpath = "m/44'/60'/0'/0/";
      let wallet = hdwallet.derivePath(wallet_hdpath + i).getWallet();
      let address = '0x' + wallet.getAddress().toString("hex");
      let privateKey = wallet.getPrivateKey().toString("hex");
      state.accounts.push(
        {
          address: address,
          privateKey: privateKey,
          index: i,
        });
      state.activeAccountIndex = i;
    },
    changeActiveAccount(state, { index }) {
      if (0 <= index < state.accounts.length) {
        state.activeAccountIndex = index;
      }
    },
    logOut(state) {
      state.loggedIn = false;
      state.mnemonic = '';
      state.accounts = [];
      state.activeAccountIndex = -1;
    }
  },
  getters: {
    activeAccount: state => {
      if (state.accounts.length !== 0) {
        return state.accounts[state.activeAccountIndex];
      }
      return undefined;
    },
  },
});


// address clock hammer exhibit eight feature injury nose flash matter ridge scan
