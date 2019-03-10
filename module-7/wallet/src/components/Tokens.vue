<template>
  <div class="container">
    <br>

    <div v-if="$store.state.loggedIn">

      <div>
        <form class="form-group">
          <div>
            <label for="addressInput"> Enter ERC20 token address: </label>
            <input id="addressInput" type="text" class="form-control  my-1 mr-sm-2" v-model="contractAddress">
          </div>

          <button type="submit" class="btn btn-outline-info my-1 mr-sm-2" v-on:click="getInfoFromContract">Lets go</button>
        </form>
      </div>

      <div v-if="contractInfo">
        <div class="card my-1 mr-sm-2 border-info">
          <div class="card-body">
            <h5 class="card-title"> ERC20 Token info</h5>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">
                <table class="table">
                  <tbody>
                  <tr  v-for="(item, key, index) in contractInfo">
                    <td> {{ key }}</td>
                    <td> {{ item }} </td>
                  </tr>
                  </tbody>
                </table>
              </li>
              <li class="list-group-item">

                <table class="table">
                  <tbody>
                  <tr>
                    <td>
                      <form class="form-inline">
                        <input id="tokenOwnerAddress" type="text" class="form-inline  my-1 mr-sm-2" placeholder="token owner address" v-model="tokenOwnerAddress">
                        <button type="submit" class="btn btn-outline-info form-inline my-1 mr-sm-2" v-on:click="getTokenOwnerBalance(contractInfo.address)">Get balance</button>
                      </form>
                    </td>
                    <td> {{ tokenOwnerBalance }} </td>
                  </tr>
                  </tbody>
                </table>
              </li>

              <li class="list-group-item">

                <table class="table">
                  <tbody>
                  <tr>
                    <td>
                      <form class="form-inline">
                        <input type="text" class="form-inline  my-1 mr-sm-2" placeholder="address to send tokens to" v-model="recipient">
                        <input type="number" class="form-inline  my-1 mr-sm-2" min="0" v-model="tokensToSend">
                        <button type="submit" class="btn btn-outline-info form-inline my-1 mr-sm-2" v-on:click="sendTokensToAddress(contractInfo.address)">Send tokens</button>
                      </form>
                    </td>
                  </tr>
                  </tbody>
                </table>
              </li>
            </ul>

          </div>
        </div>
      </div>


    </div>

    <div v-else>
      Log in or generate new wallet to use this functional.
    </div>

  </div>

</template>

<script>
  const Tx = require('ethereumjs-tx');
  import Web3 from 'web3';
  let abi = require('human-standard-token-abi');

  export default {
    name: "Tokens.vue",
    created() {
      this.setupWeb3();
    },
    data() {
      return {
        web3js: '',
        contractAddress: '0xd1dd3fd17c7ad4857dfd4a3cbcef477993c4ad4b',
        contractInfo: undefined,
        tokenOwnerAddress: '',
        tokenOwnerBalance: '0',
        recipient: '',
        tokensToSend: 0,
        txInitiated: false,
        txResult: undefined,
        txError: undefined,
      };
    },
    methods: {
      async setupWeb3() {
        this.web3js = new Web3(new Web3.providers.WebsocketProvider("wss://ropsten.infura.io/ws"));
      },
      async getInfoFromContract() {
        const contract = new this.web3js.eth.Contract(abi, this.contractAddress);

        this.contractInfo = {
          address: this.contractAddress,
          name: await contract.methods.name.call(),
          symbol:  await contract.methods.symbol.call(),
          totalSupply: await contract.methods.totalSupply.call(),
        };

        console.log(this.contractInfo)
      },
      async getTokenOwnerBalance(contractAddress) {
        console.log(contractAddress);
        const contract = new this.web3js.eth.Contract(abi, contractAddress);

        this.tokenOwnerBalance = await contract.methods.balanceOf(this.tokenOwnerAddress).call();
      },
      async sendTokensToAddress(contractAddress) {
        const contract = new this.web3js.eth.Contract(abi, contractAddress);
        let privateKey = this.$store.state.accounts[this.$store.state.activeAccountIndex].privateKey;
        let address = this.$store.state.accounts[this.$store.state.activeAccountIndex].address;


        console.log(contract);
        const functionAbi = contract.methods.transfer(this.recipient, this.tokensToSend).encodeABI();

        let rawTx = {
          nonce: this.web3js.utils.toHex(await this.web3js.eth.getTransactionCount(address)),
          gasPrice: this.web3js.utils.toHex(2000000000),
          gasLimit: this.web3js.utils.toHex(1000000),
          to: contractAddress,
          data: functionAbi,
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
    }
  }
</script>

<style scoped>
</style>

<!-- Naught coin for testing purposes -->
<!--0xd1dd3fd17c7ad4857dfd4a3cbcef477993c4ad4b-->
