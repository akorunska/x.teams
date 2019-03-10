<template>
  <div class="container">
    <br>

    <div v-if="$store.state.loggedIn">
      Tokens
    </div>

    <div v-else>
      Log in or generate new wallet to use this functional.
    </div>

  </div>

</template>

<script>
    export default {
      name: "Tokens.vue",
      created() {
        this.setupWeb3();
      },
      data() {
        return {
          web3js: '',
        };
      },
      methods: {
        async setupWeb3() {
          this.web3js = new Web3(new Web3.providers.WebsocketProvider("wss://ropsten.infura.io/ws"));
        },
      }
    }
</script>

<style scoped>

</style>

<!-- Naught coin for testing purposes -->
<!--0xd1dd3fd17c7ad4857dfd4a3cbcef477993c4ad4b-->
