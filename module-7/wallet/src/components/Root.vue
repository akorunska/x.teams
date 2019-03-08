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
      </div>
    </nav>

    <component v-bind:is="content"></component>

  </div>
</template>

<script>
  import Home from './Home'
  import Balances from './Balances'

  export default {
    name: "Navbar",
    created() {
      this.updateContent(this.active_component)
    },
    data() {
      return {
        tabs: ['Home', '', '', '', '', 'Balances'],
        active_component: 'Home',
        content: "",
      };
    },
    methods: {
      updateContent(data) {
        this.active_component = data;
        if (data === 'Home') {
          this.content = Home;
        } else if (data === 'Balances') {
          this.content = Balances;
        }
      },
    },
  }
</script>

<style scoped>
</style>
