<template>
  <v-container fluid grid-list-md>
    <!-- Cards informativos -->
    <v-layout row wrap>
      <v-flex lg4 md4 xs12 v-for="(item, index) in cards" :key="index">
        <v-hover v-slot:default="{ hover }">
          <v-card raised :elevation="hover ? 12 : 2">
            <div class="d-flex flex-no-wrap justify-space-between">
              <v-avatar class="ma-3" tile size="65">
                <v-icon large :color="item.color">{{item.icon}}</v-icon>
              </v-avatar>
              <div>
                <v-card-title class="headline" v-text="item.title"></v-card-title>
                <v-card-subtitle class="justify-start" v-text="item.subtitle"></v-card-subtitle>
              </div>
            </div>
          </v-card>
        </v-hover>
      </v-flex>
    </v-layout>
    <!-- END -->
  </v-container>
</template>

<script>
export default {
  name: "Home",
  data: () => ({
    cards: [
      {
        title: "Venda",
        subtitle: "Efetuar uma venda",
        icon: "mdi-account-multiple",
        color: "purple"
      }
    ]
  })
};
</script>
<style scoped>
.v-card {
  cursor: pointer;
}
</style>