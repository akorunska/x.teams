<template>
  <div>
    <div class="container">
      <br>
      <div id="app">

        <div v-if="$store.state.loggedIn === true">

          <div class="card my-1 mr-sm-2 border-info">
            <div class="card-body">
              <h5 class="card-title">  Welcome to Best Ethereum Wallet.</h5>

              <ul class="list-group list-group-flush">
                <li class="list-group-item">
                  Use dropdown menu to set an account as active. Click plus sign to generate more accounts.
                </li>
                <li class="list-group-item">
                  Use 'Balances' tab to quickly check the testnet balance of any eth account you want.
                </li>
                <li class="list-group-item">
                  Navigate to 'Send Ether' tab if you want to transfer ether. Transaction details will not be shown immediately but balances will be updated shortly.
                </li>
                <li class="list-group-item">
                  Use 'Tokens' tab for interaction with ERC20 tokens.
                </li>
                <li class="list-group-item">
                  Be sure to check out multisig wallets from 'Multisig' tab.
                </li>
                <li class="list-group-item">
                  Once you're done, click logout button.
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div v-else-if="initiatedMnemonicGeneration === true">
          <div> Please be sure to write down and/or save this words and keep them somewhere secure. </div>
          <div class="card my-1 mr-sm-2 border-info">
            <div class="card-body">
              <div>{{mnemonicProposed}}</div>
            </div>
          </div>
          <button class="btn btn-light my-1 mr-sm-2" v-on:click="acceptMnemonic">
            I have my mnemonic phrase securely backed up, continue.
          </button>
        </div>

        <div v-else-if="initiatedMnemonicImporting === true">
          <form class="form-row">
            <textarea class="form-control my-1 mr-sm-2" v-model="mnemonicInput"></textarea>
            <button class="btn btn-light my-1 mr-sm-2" v-on:click="validateMnemonic"> Import </button>
          </form>
          <div v-if="importedMnemonicIsUnvalid === true">
            It seems like mnemonic you are trying to import was not generated with this application.
            It may be invalid. Would you like to continue anyway?

            <form class="form-row">
              <button class="btn btn-light my-1 mr-sm-2" v-on:click="continueWithInvalidMnemonic"> Yes, continue </button>
            </form>
          </div>
        </div>

        <div v-else>
          Looks like you are not logged in. Would you like to generate new mnemonic or import one?
          <form class="form-row">
            <button class="btn btn-light my-1 mr-sm-2" v-on:click="generateMnemonic"> Generate mnemonic </button>
            <button class="btn btn-light my-1 mr-sm-2" v-on:click="importMnemonic"> Import mnemonic </button>
          </form>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex';
  import bip39 from 'bip39';

  export default {
    name: "Home",
    data() {
      return {
        msg: "home",
        initiatedMnemonicGeneration: false,
        initiatedMnemonicImporting: false,
        importedMnemonicIsUnvalid: false,
        mnemonicInput: '',
        mnemonicProposed: '',
      }
    },
    methods: {
      generateMnemonic () {
        this.initiatedMnemonicGeneration = true;
        this.mnemonicProposed = bip39.generateMnemonic();
      },
      importMnemonic () {
        this.initiatedMnemonicImporting = true;
      },
      validateMnemonic () {
        if (!bip39.validateMnemonic(this.mnemonicInput)) {
          this.importedMnemonicIsUnvalid = true;
        } else {
          this.mnemonicProposed = this.mnemonicInput;
          this.acceptMnemonic();
        }
      },
      continueWithInvalidMnemonic() {
        this.mnemonicProposed = this.mnemonicInput;
        this.acceptMnemonic();
      },
      acceptMnemonic() {
        this.initiatedMnemonicGeneration = false;
        this.initiatedMnemonicImporting = false;
        this.$store.commit('importMnemonic', { mnemonic: this.mnemonicProposed });
      }
    }
  }
</script>

<style scoped>
</style>

