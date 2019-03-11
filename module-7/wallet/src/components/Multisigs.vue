<template>
  <div class="container">
    <br>

    <div v-if="$store.state.loggedIn">
      <div>
        <form class="form-group">
          <div>
            <label for="addressInput"> Multisig wallet address: </label>
            <input id="addressInput" type="text" class="form-control  my-1 mr-sm-2" v-model="contractAddress">
          </div>

          <button type="submit" class="btn btn-outline-info my-1 mr-sm-2" v-on:click="loadMultisigFromAddress">Load multisig from address</button>
          <button type="submit" class="btn btn-outline-info my-1 mr-sm-2" v-on:click="createNewMultisig">Create new multisig</button>
        </form>
      </div>

      <div v-if="contractInfo">
        {{ contractInfo }}
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
  import { multisigContractAbi, factoryContractAbi } from "../contractABIs"

  export default {
    name: "Multisigs",
    created() {
      this.setupWeb3();
      this.factory = new this.web3js.eth.Contract(factoryContractAbi, this.factoryContractAddress);
    },
    data() {
      return {
        web3js: '',
        contractAddress:'',
        contract: '',
        contractInfo: undefined,
        factoryContractAddress: '0x47509984eff8c424c652424d6326e48466a674b8',
        factory: undefined,
        addressOfCreatedMultigsig: "",
      };
    },
    methods: {
      async setupWeb3() {
        this.web3js = new Web3(new Web3.providers.WebsocketProvider("wss://ropsten.infura.io/ws"));
      },
      async loadMultisigFromAddress() {
        this.contract = new this.web3js.eth.Contract(multisigContractAbi, this.contractAddress);

        this.contractInfo = {
          owners: await this.contract.methods.getOwners.call(),
        };

      },
      async createNewMultisig () {
        let privateKey = this.$store.state.accounts[this.$store.state.activeAccountIndex].privateKey;
        let address = this.$store.state.accounts[this.$store.state.activeAccountIndex].address;

        const functionAbi = this.factory.methods.create([ address ], 1).encodeABI();

        let rawTx = {
          nonce: this.web3js.utils.toHex(await this.web3js.eth.getTransactionCount(address)),
          gasPrice: this.web3js.utils.toHex(1000000000),
          gasLimit: this.web3js.utils.toHex(1300000),
          to: this.factoryContractAddress,
          data: functionAbi,
          chainId: 3,
        };

        const tx = new Tx(rawTx);

        let p = new Buffer(privateKey, 'hex');
        tx.sign(p);

        console.log(tx);
        let serializedTx = "0x" + tx.serialize().toString('hex');


        console.log(serializedTx);
        try {
          this.addressOfCreatedMultigsig = await this.web3js.eth.sendSignedTransaction(serializedTx);
          console.log(addressOfCreatedMultigsig);
        } catch (e) {
          console.log(e);
        }
        console.log("sent tx");

      }
    }
  }
</script>

<style scoped>

</style>


<!--0x1771A544E3D38489d25455043D940FBb74145fdE-->
