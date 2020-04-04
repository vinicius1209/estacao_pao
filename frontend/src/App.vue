<template>
  <v-app>
    <Menu/>
    <v-content>
      <Loading ref="loading"/>
      <Notification ref="notification"/>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import Menu from './components/Menu';
import Loading from './components/Loading';
import Notification from './components/Notification';

export default {
  name: 'App',

  components: {
    Menu,
    Loading,
    Notification
  },

  data: () => ({
    
  }),
};
</script>