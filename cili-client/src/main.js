// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

import axios from 'axios';
Vue.config.productionTip = false
Vue.use(ElementUI);

Vue.prototype.httpGet = function (url, success, failed) {
  axios.get(url).then(success).catch(e => failed(e.response))
};

Vue.prototype.httpPost = function (url, content, success, failed) {
  axios.post(url, content).then(success).catch(e => failed(e.response))
};

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
