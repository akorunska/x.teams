<template>
  <div class="container">
    <br>
    <div v-if="$store.state.loggedIn">

      <div>
        <form class="form-row">

          <div>
            <label> Recipient </label>
            <input type="text" class="form-control  my-1 mr-sm-2" v-model="recipient">
          </div>

          <div>
            <label> Amount </label>
            <input type="number" step="0.00000001" min="0" class="form-control  my-1 mr-sm-2" v-model="ethAmount">
          </div>

          <button type="submit" class="btn btn-light my-1 mr-sm-2" v-on:click="sendTransaction">Send transaction</button>
        </form>
      </div>

    </div>

    <div v-else>
      Log in or generate new wallet to use this functional.
    </div>
  </div>
</template>

<script>
  const Tx = require('ethereumjs-tx');
  import util from 'ethereumjs-util';
  import Web3 from 'web3';

  export default {
    name: "Transactions",
    created() {
      this.setupWeb3();
    },
    data() {
      return {
        web3js: '',
        recipient: '',
        ethAmount: '',
      };
    },
    methods: {
      async setupWeb3() {
        this.web3js = web3 = new Web3(new Web3.providers.WebsocketProvider("wss://ropsten.infura.io/ws"));
      },
      async sendTransaction() {
        console.log( this.recipient,  this.ethAmount);

        let privateKey = this.$store.state.accounts[this.$store.state.activeAccountIndex].privateKey;
        let address = this.$store.state.accounts[this.$store.state.activeAccountIndex].address;

        console.log(privateKey, address);


        let amount = this.web3js.utils.toWei(this.ethAmount);
        console.log(amount);

        let rawTx = {
          nonce: this.web3js.utils.toHex(await this.web3js.eth.getTransactionCount(address)),
          gasPrice: this.web3js.utils.toHex(2000000000),
          gasLimit: this.web3js.utils.toHex(1000000),
          to: this.recipient,
          value: this.web3js.utils.toHex(amount),
          data: '0x00',
          chainId: 3,
        };

        const tx = new Tx(rawTx);
        console.log(tx);

        let p = new Buffer(privateKey, 'hex');
        tx.sign(p);
        let serializedTx = "0x" + tx.serialize().toString('hex');
        console.log(serializedTx);

        try {
          let result = await this.web3js.eth.sendSignedTransaction(serializedTx);
          console.log('RESULT');
          console.log(result);
        } catch (e) {
          console.log(e);
        }
        console.log("sent tx");
      }

    },
  }
</script>

<style scoped>
</style>
