import 'bootstrap/dist/css/bootstrap.css';
import Vue from 'vue'
import App from './App'
import router from './router'
import store from "./_store/index";

Vue.config.productionTip = false;

/* eslint-disable no-new */

new Vue({
  el: '#app',
  store,
  router,
  components: { App },
  template: '<App/>'
});
