<template>
  <v-container fluid grid-list-md>
    <!-- Cards informativos -->
    <v-layout row wrap>
     
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
        title: "SmartX",
        subtitle: "Usuários",
        qtd: 32,
        icon: "mdi-account-multiple",
        color: "indigo darken-4"
      },
      {
        title: "Educacional",
        subtitle: "Instituições",
        qtd: 687,
        icon: "mdi-alpha-e-box",
        color: "purple darken-4"
      },
      {
        title: "Escalabilidade",
        subtitle: "Vendas",
        qtd: 58,
        icon: "mdi-cart",
        color: "teal darken-1"
      },
      {
        title: "Mensagens",
        subtitle: "Total",
        qtd: 17,
        icon: "mdi-message",
        color: "teal darken-4"
      }
    ]
  })
};
</script>
<style scoped>
.v-card{
  cursor: pointer;
}
</style>