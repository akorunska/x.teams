import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    mnemonic: '',
    loggedIn: false
  },
  mutations: {
    importMnemonic(state, { mnemonic }) {
      state.loggedIn = true;
      state.mnemonic = mnemonic;
    },
    logOut(state) {
      state.loggedIn = false;
      state.mnemonic = '';
    }
  }
});
