<template>
  <v-overlay :value="loading">
    <v-dialog v-model="loading" hide-overlay persistent width="300">
      <v-card color="primary" dark>
        <v-card-text>
          Carregando
          <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-overlay>
</template>
<script>
export default {
  name: "Loading",
  data() {
    return {
      loading: false
    };
  },
  methods: {
    open: function() {
      this.loading = true;
    },
    close: function() {
      this.loading = false;
    }
  }
};
</script>