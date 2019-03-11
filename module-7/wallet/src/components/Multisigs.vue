<template>
  <div class="container">
    <br>

    <div v-if="$store.state.loggedIn">
      <div v-if="!contractInfo">
        <form class="form-group">
          <div>
            <label for="addressInput"> Multisig wallet address: </label>
            <input id="addressInput" type="text" class="form-control  my-1 mr-sm-2" v-model="contractAddress">
          </div>

          <button type="submit" class="btn btn-outline-info my-1 mr-sm-2" v-on:click="loadMultisigFromAddress">Load multisig from address</button>

          <div>
            <label for="ownersInput"> Add owners addresses separated by spaces: </label>
            <input id="ownersInput" type="text" class="form-control  my-1 mr-sm-2" v-model="ownerAddresses">

            <label for="signaturesRequired"> How many signatures are necessary to sign transaction: </label>
            <input id="signaturesRequired" type="number" class="form-control  my-1 mr-sm-2" v-model="signaturesRequired">
          </div>

          <button type="submit" class="btn btn-outline-info my-1 mr-sm-2" v-on:click="createNewMultisig">Create new multisig</button>
        </form>
      </div>

      <div v-if="contractInfo">

        <div class="card my-1 mr-sm-2 border-info">
          <div class="card-body">
            <h5 class="card-title"> Owners </h5>
            <ul class="list-group list-group-flush">
              <li class="list-group-item" v-for="item in contractInfo.owners">
                {{ item }}
              </li>
            </ul>
          </div>
        </div>

        <div class="card my-1 mr-sm-2 border-info">
          <div class="card-body">
            <h5 class="card-title"> Transactions </h5>
            <form>
              Get transaction info:
              <input type="number" class="form-control  my-1 mr-sm-2" v-model="txid">
              <button type="submit" class="btn btn-outline-info my-1 mr-sm-2" v-on:click="getTxInfo">Get Transaction Info</button>
            </form>

            <table class="table" v-if="txInfo">
              <tbody>
                <ul class="list-group list-group-flush">
                  <li class="list-group-item">
                    <tr  v-for="(item, key, index) in txInfo">
                      <td> {{ key }}</td>
                      <td> {{ item }} </td>
                    </tr>
                  </li>
                </ul>
              </tbody>
            </table>

            <br>
            <form>
              Create new transaction:
              <input type="number" class="form-control  my-1 mr-sm-2" v-model="valueToSend">
              <input type="text" class="form-control  my-1 mr-sm-2" v-model="addressToSend">
              <button type="submit" class="btn btn-outline-info my-1 mr-sm-2" v-on:click="sendNewTx">Send new proposal</button>
            </form>

            <br>
            <form>
              Confirm transaction:
              <input type="number" class="form-control  my-1 mr-sm-2" v-model="txidToConfirm">
              <button type="submit" class="btn btn-outline-info my-1 mr-sm-2" v-on:click="confirmTx">Confirm transaction</button>
            </form>
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
        contractAddress: '',
        contract: '',
        contractInfo: undefined,
        factoryContractAddress: '0x1bb48c5cf26a0e7a0103a1c229e66f3d52986d88',
        factory: undefined,
        addressOfCreatedMultigsig: "",
        ownerAddresses: '',
        signaturesRequired: 0,
        txid: 0,
        txInfo: undefined,
        valueToSend: 0,
        addressToSend: '',
        txidToConfirm: 0,
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

        this.contractInfo.address = this.contractAddress;
        console.log(this.contractInfo);
      },
      async createNewMultisig () {
        let privateKey = this.$store.state.accounts[this.$store.state.activeAccountIndex].privateKey;
        let address = this.$store.state.accounts[this.$store.state.activeAccountIndex].address;

        let addresses = this.ownerAddresses.split(" ");
        console.log(addresses);
        const functionAbi = this.factory.methods.create(addresses, this.signaturesRequired).encodeABI();

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
      },
      async getTxInfo() {
        let result = await this.contract.methods.transactions(this.txid).call();
        this.txInfo = {
          recipient: result.destination,
          wei_amount: result.value,
          is_confirmed: result.executed,
        }
      },
      async sendNewTx() {
        let privateKey = this.$store.state.accounts[this.$store.state.activeAccountIndex].privateKey;
        let address = this.$store.state.accounts[this.$store.state.activeAccountIndex].address;

        const functionAbi = this.contract.methods.submitTransaction(this.addressToSend, this.valueToSend).encodeABI();

        let rawTx = {
          nonce: this.web3js.utils.toHex(await this.web3js.eth.getTransactionCount(address)),
          gasPrice: this.web3js.utils.toHex(1000000000),
          gasLimit: this.web3js.utils.toHex(1300000),
          to: this.contractInfo.address,
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
          let responce = await this.web3js.eth.sendSignedTransaction(serializedTx);
          console.log(responce);
        } catch (e) {
          console.log(e);
        }
        console.log("sent tx");
      },
      async confirmTx() {
        let privateKey = this.$store.state.accounts[this.$store.state.activeAccountIndex].privateKey;
        let address = this.$store.state.accounts[this.$store.state.activeAccountIndex].address;

        const functionAbi = this.contract.methods.confirmTransaction(this.txidToConfirm).encodeABI();

        let rawTx = {
          nonce: this.web3js.utils.toHex(await this.web3js.eth.getTransactionCount(address)),
          gasPrice: this.web3js.utils.toHex(1000000000),
          gasLimit: this.web3js.utils.toHex(1300000),
          to: this.contractInfo.address,
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
          let responce = await this.web3js.eth.sendSignedTransaction(serializedTx);
          console.log(responce);
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


<!--0x80b354f420c591fE1eAc1404cA668aD7416e8bA5-->
