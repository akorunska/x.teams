<template>
    <div class="container">
      <br>
      <div class="card">
        <div class="card-body">
          <h5 class="card-title"> Currently pitcoin blockchain contains {{ chainLength }} blocks. </h5>
          <br>
          <h5 class="card-title">Blockchain meta info: </h5>
          <table class="table">
            <tbody>
              <tr>
                <td>Creating one block takes approximately <code>{{ meta['seconds_to_create_block_expected'] }}</code> seconds </td>
              </tr>
              <tr>
                <td>Original target is <code>{{ meta['original_target'] }}</code> </td>
              </tr>
              <tr>
                <td>Current target is <code>{{ meta['current_target'] }}</code> </td>
              </tr>
              <tr>
                <td>Current difficulty is <code>{{ meta['difficulty'] }}</code> </td>
              </tr>
              <tr>
                <td>Target updates every <code>{{ meta['target_update_frequency'] }}</code> blocks </td>
              </tr>
              <tr>
                <td>Current miner reward is <code>{{ meta['current_miner_reward'] }}</code> pitcoins </td>
              </tr>
              <tr>
                <td>Halving occurs every <code>{{ meta['halving_frequency'] }}</code> blocks </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
</template>

<script>
  import axios from 'axios';
  import settings from '../settings'

  export default {
    name: 'Home',
    created() {
      this.loadPitcoinInfo();
    },
    data() {
      return {
        chainLength: 0,
        meta: ''
      };
    },
    methods: {
      async loadPitcoinInfo() {
        let path = settings.pitcoinNodeUrl;

        let chainLen = await axios.get(path + '/chain/length');
        let meta = await axios.get(path + '/meta');

        this.chainLength = chainLen.data['chainlength'];
        this.meta = meta.data;

        setTimeout(this.loadPitcoinInfo, 50000);
      },
    },
  };
</script>

<style scoped>

</style>
