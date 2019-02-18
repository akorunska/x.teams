<template>
  <div class="container">
    <br>

    <div>
      <form class="form-row">
        <select class="col-2 custom-select my-1 mr-sm-2" id="inlineFormCustomSelectPref">
          <option v-for="param in search_params" v-on:click="updateSearchParam(param)"> {{ param }}</option>
        </select>

        <div class="col-8" v-show="search_param === 'Search by address'">
          <input type="text" class="form-control  my-1 mr-sm-2" v-model="filter">
        </div>

        <div class="col-8" v-show="search_param === 'Get all' ">
          <input type="text" class="form-control  my-1 mr-sm-2" disabled v-model="filter">
        </div>

        <button type="submit" class="btn btn-light my-1 mr-sm-2" v-on:click="updateOutputsData">Search</button>
      </form>
     </div>

    <div v-if="status === 200">
      <div v-for="output in outputs" class="card my-1 mr-sm-2 border-success">
        <div class="card-body">
          <h5 class="card-title">Unspent Transaction Output</h5>
          <div v-if="filter !== ''">
             <h6 class="card-subtitle mb-2 text-muted">for {{ filter }} address</h6>
          </div>
          <ul class="list-group list-group-flush">
            <li class="list-group-item">
              <table class="table">
                <tbody>
                  <tr>
                    <td>value</td>
                    <td> {{ output['value'] }} </td>
                  </tr>
                  <tr>
                    <td>scriptpubkey</td>
                    <td> {{ output['scriptpubkey'] }} </td>
                  </tr>
                </tbody>
              </table>
            </li>
          </ul>

        </div>
      </div>
    </div>

    <div v-else-if="status === 400" class="card my-1 mr-sm-2 border-danger">
      <div class="card-body">
        <h5 class="card-title"> Error </h5>
        <h6 class="card-subtitle mb-2 text-muted">{{ transactions }}</h6>
      </div>
    </div>

  </div>

</template>


<script>
import axios from 'axios';
import settings from '../settings'


export default {
  name: 'UTXOPool',
  data() {
    return {
      search_params: ['Get all', 'Search by address'],
      search_param: 'Get all',
      outputs: [],
      status: 0,
      filter: "",
    };
  },
  methods: {
    updateSearchParam(param) {
      this.search_param = param;
      this.filter = "";
      this.outputs = [];
      this.status = 0;
    },
    async updateOutputsData() {
      let path = settings.pitcoinNodeUrl + '/utxo';

      if (this.search_param === 'Search by address') {
        path += '?address=' + this.filter;
      }

      try {
        let res = await axios.get(path);

        console.log(res.data.length);
        if (res.data.length === 0) {
          this.status = 400;
          this.outputs = "no utxo for this address";
        } else {
          this.status = res.status;
          this.outputs = res.data;
        }
      } catch (e) {
        console.log(e)
      }
    },
  },
};
</script>


<style scoped>
  table {
    table-layout: fixed;
  }

  table tr td {
    word-wrap: break-word;
  }
</style>

