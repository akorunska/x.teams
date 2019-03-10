<template>
  <div class="container">
    <br>

    <div v-if="$store.state.loggedIn">
      Multisigs
    </div>

    <div v-else>
      Log in or generate new wallet to use this functional.
    </div>

  </div>

</template>

<script>
    export default {
        name: "Multisigs"
    }
</script>

<style scoped>

</style>
