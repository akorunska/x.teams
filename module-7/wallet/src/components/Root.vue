<template>
  <div>
    <h2>{{balance}}</h2>

  </div>

</template>

<script>
  import Web3 from 'web3';
  import settings from '../settings';
  import axios from 'axios';

export default {
  name: 'Root',
  async created() {
    this.setupWeb3();
    await this.getBalance();
  },
  data () {
    return {
      web3js: '',
      balance: 0,
      balanceEth: 0,
    }
  },
  methods: {
    async setupWeb3() {
      this.web3js = new Web3(web3.currentProvider);
    },
    async getBalance() {
      let response = await this.web3js.eth.getBalance('0xa3E1aB154F40d984E56fF07d1EEa46a50BD8ee36');
      this.balance = this.web3js.utils.fromWei(response);
    }
  },
}

</script>

<style scoped>
</style>
