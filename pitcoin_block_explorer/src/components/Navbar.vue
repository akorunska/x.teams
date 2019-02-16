<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="#">Pitcoin Block Explorer</a>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="#" v-on:click="updateContent('home')"> Home <span class="sr-only">(current)</span></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" v-on:click="updateContent('blocks')">Blocks</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" v-on:click="updateContent('transactions')">Transactions</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" v-on:click="updateContent('utxo_pool')">UTXO Pool</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" v-on:click="updateContent('pending_pool')">Pending Pool</a>
          </li>
        </ul>
        <form class="form-inline my-2 my-lg-0">
          <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
        </form>
      </div>
    </nav>

      <component
        v-bind:is="content"
      ></component>

  </div>
</template>

<script>
import Blocks from './Blocks'
import Transactions from './Transactions'

  export default {
    name: "Navbar",
    data() {
      return {
        content: '',
      };
    },
    methods: {
      updateContent(data) {
        if (data === 'home') {
          this.content = '';
        } else if (data === 'blocks') {
          this.content = Blocks;
        } else if (data === 'transactions') {
          this.content = Transactions;
        }
      },
    },
    created() {

    },
  }
</script>

<style scoped>
</style>
