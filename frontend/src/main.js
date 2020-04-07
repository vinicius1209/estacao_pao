import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import money from 'v-money';
import VueTheMask from 'vue-the-mask'

Vue.config.productionTip = false

Vue.use(money, {precision: 4})
Vue.use(VueTheMask)

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
