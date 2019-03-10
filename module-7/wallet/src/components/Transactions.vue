<template>
  <div class="container">
    <br>
    <div v-if="$store.state.loggedIn">

      <div>
        <form class="form-group">
          <div>
            <label for="recipientInput"> Enter recipient address: </label>
            <input id="recipientInput" type="text" class="form-control  my-1 mr-sm-2" v-model="recipient">
          </div>

          <div>
            <label for="txAmountInput"> Enter amount to send in ethers: </label>
            <input id="txAmountInput" type="number" step="0.00000001" min="0" class="form-control  my-1 mr-sm-2" v-model="ethAmount">
          </div>


          <button type="submit" class="btn btn-outline-info my-1 mr-sm-2" v-on:click="sendTransaction">Send transaction</button>
        </form>
      </div>
      <br>

      <div v-if="txInitiated === true">
        Your transaction was sent to the network. Processing it will take a while.
      </div>

      <div v-if="txResult !== undefined">
        <div class="card my-1 mr-sm-2 border-info">
          <div class="card-body">
            <h5 class="card-title">
              <a :href="'https://ropsten.etherscan.io/tx/' + txResult['transactionHash']">
                {{ txResult['transactionHash'] }}
              </a>
            </h5>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">
                <table class="table">
                  <tbody>
                  <tr>
                    <td> blockHash</td>
                    <td> {{ txResult['blockHash'] }} </td>
                  </tr>
                  <tr>
                    <td>blockNumber</td>
                    <td> {{ txResult['blockNumber'] }} </td>
                  </tr>
                  <tr>
                    <td>from</td>
                    <td> {{ txResult['from'] }} </td>
                  </tr>
                  <tr>
                    <td>to</td>
                    <td> {{ txResult['to'] }} </td>
                  </tr>
                  <tr>
                    <td>status</td>
                    <td> {{ txResult['status'] }} </td>
                  </tr>
                  </tbody>
                </table>
              </li>
            </ul>

          </div>
        </div>
      </div>

      <div v-if="txError !== undefined">
        {{ txError }}
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
        txInitiated: false,
        txResult: undefined,
        txError: undefined,
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

        this.txInitiated = true;
        try {
          let result = await this.web3js.eth.sendSignedTransaction(serializedTx);
          this.txInitiated = false;
          this.txResult = result;
        } catch (e) {
          this.txInitiated = false;
          this.txError = e;
        }
        console.log("sent tx");
      }

    },
  }
</script>


<!--{ "blockHash": "0x0a6b614bb7c7f4b4e14f58cb50cc3fbabefe9f04235669aac8bdfccc73fa2db5", "blockNumber": 5177716, "contractAddress": null, "cumulativeGasUsed": 51730, "from": "0x4897e6f798329e1f87815f250692c9dafb7ad09c", "gasUsed": 21004, "logs": [], "logsBloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000", "status": true, "to": "0xa3e1ab154f40d984e56ff07d1eea46a50bd8ee36", "transactionHash": "0xc6a74a72c08b17233a369b3c336b09e6f14cb92bf1f7dfa4d21316e7bf1911d2", "transactionIndex": 1 }-->

<style scoped>
</style>
