<template>
<div>

  <div class="container">
    <br>

    <div>
      <form class="form-row">

        <div class="col-10">
          <input type="text" class="form-control  my-1 mr-sm-2" v-model="filter">
        </div>

        <button type="submit" class="btn  btn-outline-info  my-1 mr-sm-2" v-on:click="getBalance">Get balance</button>
      </form>
    </div>

    <div v-if="status === 200">
      <div class="card my-1 mr-sm-2 border-info">
        <div class="card-body">
          <div v-if="filter !== ''">
            <h4 class="card-title">{{filter}}</h4>
          </div>
          <div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">{{balance}} ETH </li>
            </ul>
          </div>

        </div>
      </div>
    </div>
    <div v-else-if="status === 400">
      <div class="card my-1 mr-sm-2 border-danger">
        <div class="card-body">
          <h4 class="card-title">Error</h4>
          {{errorMessage}}
        </div>
      </div>
    </div>

    <!--<div v-if="$store.state.loggedIn">-->
        <!--<div v-for="account in $store.state.accounts">-->
          <!--{{account}}-->
        <!--</div>-->
    <!--</div>-->

  </div>

</div>

</template>

<script>
  import Web3 from 'web3';

  export default {
    name: 'Balances',
    async created() {
      this.setupWeb3();
    },
    data () {
      return {
        web3js: '',
        balance: 0,
        filter: '',
        status: 0,
        errorMessage: '',
      }
    },
    methods: {
      async setupWeb3() {
        this.web3js = new Web3(new Web3.providers.WebsocketProvider("wss://ropsten.infura.io/ws"));
      },
      async getBalance() {
        try {
          let response = await this.web3js.eth.getBalance(this.filter);
          this.balance = this.web3js.utils.fromWei(response);
          this.status = 200;
        } catch (e) {
          this.status = 400;
          this.errorMessage = e.message;
        }
      },
    },
  }

</script>

<style scoped>
</style>

