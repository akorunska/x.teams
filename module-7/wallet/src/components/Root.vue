<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="navbar-brand"> Best Ethereum Wallet </div>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <div v-for="tab in tabs">
            <li v-if="tab === active_component" class="nav-item active">
              <a class="nav-link" href="#" v-on:click="updateContent(tab)"> {{ tab }} <span class="sr-only">(current)</span></a>
            </li>
            <li v-else class="nav-item">
              <a class="nav-link" href="#" v-on:click="updateContent(tab)"> {{ tab }} </a>
            </li>
          </div>
        </ul>

        <ul class="nav navbar-nav navbar-right" v-if="$store.state.loggedIn">
          <form class="navbar-form">
              <div class="btn-group" role="group" aria-label="...">
                <div class="btn border-secondary">
                  {{ parseFloat(accountBalance).toFixed(4) }} ETH
                </div>
                <select class="btn border-secondary">
                  <option v-for="account in $store.state.accounts" v-on:click="setAccountAsActive(account.index)"> {{ account.address }}</option>
                </select>
                <button class="btn btn-outline-info" v-on:click="getNewAccount"> + </button>
              </div>
            <button class="btn btn-outline-info" v-on:click="logOut"> Log out </button>
          </form>

        </ul>
      </div>
    </nav>

    <component v-bind:is="content"></component>

  </div>
</template>

<script>
  import { mapGetters } from 'vuex';
  import Web3 from 'web3';
  import Home from './Home'
  import Balances from './Balances'
  import Transactions from './Transactions'

  export default {
    name: "Navbar",
    created() {
      this.updateContent(this.active_component);
      this.setupWeb3();
    },
    computed: {
      ...mapGetters([
        'activeAccount',
      ]),
    },
    data() {
      return {
        tabs: ['Home', 'Balances', 'Send Ether', 'Tokens', 'Multisigs', ],
        active_component: 'Home',
        content: "",
        web3js: '',
        accountBalance: 0,
      };
    },
    methods: {
      async setupWeb3() {
        this.web3js = new Web3(web3.currentProvider);
      },
      updateContent(data) {
        this.active_component = data;
        if (data === 'Home') {
          this.content = Home;
        } else if (data === 'Balances') {
          this.content = Balances;
        } else if (data === 'Send Ether') {
          this.content = Transactions;
        }
      },
      setAccountAsActive(index) {
        this.$store.commit('changeActiveAccount', {'index': index});
        this.recountAccountBalance();
      },
      getNewAccount() {
        this.$store.commit('generateNewAccount');
      },
      logOut() {
        this.$store.commit('logOut');
      },
      async recountAccountBalance() {
        let address = this.$store.state.accounts[this.$store.state.activeAccountIndex].address;
        try {
          let response = await this.web3js.eth.getBalance(address);
          this.accountBalance = this.web3js.utils.fromWei(response);
        } catch (e) {
          console.log(e);
        }
        setTimeout(this.recountAccountBalance, 5000);
      }

    },
  }
</script>

<style scoped>
</style>
