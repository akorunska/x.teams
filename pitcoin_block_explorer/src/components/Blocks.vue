<template>
  <div class="container">
    <br>

    <div>
      <form class="form-row">
        <select class="col-2 custom-select my-1 mr-sm-2" id="inlineFormCustomSelectPref">
          <option v-for="param in search_params" v-on:click="updateSearchParam(param)"> {{ param }}</option>
        </select>

        <div class="col-8" v-show="search_param === 'Block Height' ">
          <input type="number" class="form-control  my-1 mr-sm-2" placeholder="" min=0 v-model="filter">
        </div>

        <div class="col-8" v-show="search_param === 'Block Hash' ">
          <input type="text" class="form-control my-1 mr-sm-2" placeholder="" v-model="filter">
        </div>

        <button type="submit" class="btn btn-light my-1 mr-sm-2" v-on:click="updateBlockData">Search</button>
      </form>
     </div>

    <div v-if="status === 200" class="card my-1 mr-sm-2 border-success">

      <div class="card-body">
        <h5 class="card-title">Block header</h5>
        <h6 class="card-subtitle mb-2 text-muted">{{ block['hash_value'] }}</h6>

        <table class="table">
          <tbody>
            <tr>
              <td>timestamp</td>
              <td> {{ block['timestamp'] }} </td>
            </tr>
            <tr>
              <td>nonce</td>
              <td> {{ block['nonce'] }} </td>
            </tr>
            <tr>
              <td>merkle root</td>
              <td> {{ block['merkle_root'] }} </td>
            </tr>
            <tr>
              <td>target</td>
              <td> {{ block['target'] }} </td>
            </tr>
            <tr>
              <td>previous block</td>
              <td>
                <a href="#" v-on:click="redirectToBlock(block['previous_block_hash'])">
                  {{ block['previous_block_hash'] }}
                </a>
              </td>
            </tr>

          </tbody>
        </table>
      </div>

      <div class="card-body">
        <h5 class="card-title">Transactions</h5>
        <h6 class="card-subtitle mb-2 text-muted"> block contains {{ block['transactions'].length }} transactions</h6>
          <ul class="list-group list-group-flush">

            <li v-for="transaction in block['transactions']" class="list-group-item"> {{transaction}} </li>
          </ul>
      </div>
    </div>

    <div v-else-if="status === 400" class="card my-1 mr-sm-2 border-danger">
      <div class="card-body">
        <h5 class="card-title"> Error </h5>
        <h6 class="card-subtitle mb-2 text-muted">{{ block }}</h6>
      </div>
    </div>

  </div>

</template>

<script>
import axios from 'axios';
import settings from '../settings'


export default {
  name: 'Blocks',
  data() {
    return {
      search_params: ['Block Height', 'Block Hash'],
      search_param: 'Block Height',
      block: '',
      status: 0,
      filter: 0,
    };
  },
  methods: {
    updateSearchParam(param) {
      this.search_param = param;
      this.block = '';
      this.status = 0;
    },
    async updateBlockData() {
      let path = settings.pitcoinNodeUrl + '/block';
      if (this.search_param === 'Block Height') {
        path += '?block_height=' + this.filter
      }
      if (this.search_param === 'Block Hash') {
        path += '?block_hash=' + this.filter
      }

      try {
        let res = await axios.get(path);
        this.status = res.status;
        this.block = res.data['block'];
        if (this.block === 'no block on such height') {
          this.status = 400;
        } else if (this.block === 'no block with such hash') {
          this.status = 400
        }
      } catch (e) {
        console.log(e)
      }
    },
    async redirectToBlock(block_hash) {
      if (block_hash !== '0000000000000000000000000000000000000000000000000000000000000000') {
        this.search_param = 'Block Hash';
        this.filter = block_hash;
        await this.updateBlockData();
      }
    }
  },
};
</script>
