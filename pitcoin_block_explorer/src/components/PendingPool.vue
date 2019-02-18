<template>
  <div class="container">
    <br>

    <div>
      <form class="form-row">
        <select class="col-2 custom-select my-1 mr-sm-2" id="inlineFormCustomSelectPref">
          <option v-for="param in search_params" v-on:click="updateSearchParam(param)"> {{ param }}</option>
        </select>

        <div class="col-8" v-show="search_param === 'Search by txid' ">
          <input type="text" class="form-control  my-1 mr-sm-2" v-model="filter">
        </div>

        <div class="col-8" v-show="search_param === 'Get all' ">
          <input type="text" class="form-control  my-1 mr-sm-2" disabled v-model="filter">
        </div>

        <div class="col-8" v-show="search_param === 'Deserialize Raw' ">
          <textarea class="form-control my-1 mr-sm-2" v-model="filter"></textarea>
        </div>

        <button type="submit" class="btn btn-light my-1 mr-sm-2" v-on:click="updateTransactionsData">Search</button>
      </form>
     </div>

    <div v-if="status === 200">
      <div v-for="transaction in transactions" class="card my-1 mr-sm-2 border-success">
        <div class="card-body">
          <h5 class="card-title">Transaction</h5>
          <h6 class="card-subtitle mb-2 text-muted">{{ transaction['txid'] }}</h6>

          <br>
          <ul class="list-group list-group-flush">
            <li class="list-group-item">
              <table class="table">
                <thead>
                  <tr>
                    <th>Senders</th>
                  </tr>
                </thead>
                <tbody>
                  <td v-if="transaction['senders'].length > 0">
                    <tr v-for="sender in transaction['senders']">{{sender}}</tr>
                  </td>
                  <td v-else>
                    <h6 class="card-subtitle mb-2 text-muted">This is coinbase transaction</h6>
                  </td>
                </tbody>
              </table>
            </li>
          </ul>
          <ul  class="list-group list-group-flush">
            <li class="list-group-item">
              <table class="table">
                <thead>
                  <tr>
                    <th>Recipients</th>
                  </tr>
                </thead>
                <tbody>
                  <td>
                    <tr v-for="recipient in transaction['recipients']">{{recipient}}</tr>
                  </td>
                </tbody>
              </table>
            </li>
          </ul>

          <br>
          <h5 class="card-title">Header</h5>
          <ul class="list-group list-group-flush">
             <li class="list-group-item">
              <table class="table">
                <tbody>
                  <tr>
                    <td>version</td>
                    <td> {{ transaction['version'] }} </td>
                  </tr>
                  <tr>
                    <td>locktime</td>
                    <td> {{ transaction['locktime'] }} </td>
                  </tr>
                </tbody>
              </table>
            </li>
          </ul>

          <br>
          <h5 class="card-title">Inputs</h5>
          <ul class="list-group list-group-flush">
            <li  v-for="input in transaction['inputs']" class="list-group-item">
               <table class="table">
                <tbody>
                  <tr>
                    <td>txid</td>
                    <td> {{ input['txid'] }} </td>
                  </tr>
                  <tr>
                    <td>vout</td>
                    <td> {{ input['vout'] }} </td>
                  </tr>
                  <tr>
                    <td>scriptsig</td>
                    <td> {{ input['scriptsig'] }} </td>
                  </tr>
                </tbody>
              </table>
            </li>
          </ul>

          <br>
          <h5 class="card-title">Outputs</h5>
          <ul class="list-group list-group-flush">
            <li v-for="output in transaction['outputs']" class="list-group-item">
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
  name: 'PendingPool',
  data() {
    return {
      search_params: ['Get all', 'Search by txid'],
      search_param: 'Get all',
      transactions: [],
      status: 0,
      filter: ""
    };
  },
  methods: {
    updateSearchParam(param) {
      this.search_param = param;
      this.filter = "";
      this.transactions = [];
      this.status = 0;
    },
    async updateTransactionsData() {
      let path = settings.pitcoinNodeUrl + '/transaction/pendings';

      if (this.search_param === 'Search by txid')
        path += '?txid=' + this.filter;

      try {
        let res = await axios.get(path);
        console.log(res.data.length);
        if (res.data.length === 0 && this.search_param === 'Search by txid') {
          this.status = 400;
          this.transactions = "no transactions with such txid";
        } else if (res.data.length === 0 ) {
          this.status = 400;
          this.transactions = "no unconfirmed transactions yet";
        } else {

          this.status = res.status;
          this.transactions = res.data;
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

