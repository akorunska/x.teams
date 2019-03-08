<template>
  <div>
    <div class="container">
      {{msg}}

      <div id="app">
        <p>{{ count }}</p>
        <p>
          <button @click="increment">+</button>
          <button @click="decrement">-</button>
        </p>
      </div>

    </div>
  </div>

</template>

<script>
  import { mapState, mapActions } from 'vuex';

  export default {
    name: "Home",
    data() {
      return {
        msg: "home",
      }
    },
    computed: {
      ...mapState({
        count: state => state.count
      })
    },
    methods: {
      increment () {
        this.$store.commit('increment');
      },
      decrement () {
        this.$store.commit('decrement');
      }
    }
  }
</script>

<style scoped>

</style>

