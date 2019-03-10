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
            <h5 class="card-title"> ERC20 Coin at {{ contractAddress }}</h5>
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
        contractAddress: '',
        contractInfo: undefined,
      };
    },
    methods: {
      async setupWeb3() {
        this.web3js = new Web3(new Web3.providers.WebsocketProvider("wss://ropsten.infura.io/ws"));
      },
      async getInfoFromContract() {
        const contract = new this.web3js.eth.Contract(abi, this.contractAddress);

        this.contractInfo = {
          name: await contract.methods.name.call(),
          symbol:  await contract.methods.symbol.call(),
          totalSupply: await contract.methods.totalSupply.call(),
        };

        console.log(this.contractInfo)
      }
    }
  }
</script>

<style scoped>

</style>

<!-- Naught coin for testing purposes -->
<!--0xd1dd3fd17c7ad4857dfd4a3cbcef477993c4ad4b-->
