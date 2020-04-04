<template>
  <div id="menu">
    <v-navigation-drawer v-model="drawer" app dark clipped>
      <v-list dense>
        <!-- Dashboard -->
        <v-list-item link to="/">
          <v-list-item-action>
            <v-icon>mdi-view-dashboard</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Dashboard</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <!-- Caixa -->
        <v-list-group prepend-icon="mdi-cash-register" no-action>
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title>Caixa</v-list-item-title>
            </v-list-item-content>
          </template>

          <v-list-item link to="/caixa/venda">
            <v-list-item-content>
              <v-list-item-title>Venda</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

        </v-list-group>
        <!-- end Caixa -->

        <!-- Estoque -->
        <v-list-group prepend-icon="mdi-package" no-action>
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title>Estoque</v-list-item-title>
            </v-list-item-content>
          </template>

          <v-list-item link to="/estoque">
            <v-list-item-content>
              <v-list-item-title>Itens</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

        </v-list-group>
        <!-- end Estoque -->

        <!-- Relatórios -->
        <v-list-item link to="/relatorios">
          <v-list-item-action>
            <v-icon>mdi-poll</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Relatórios</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <!-- end Relatorios -->
      </v-list>
    </v-navigation-drawer>

    <!-- Top Bar -->
    <v-app-bar app clipped-left dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />

      <v-toolbar-title>Pães e Variedades</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn class="ma-2" text icon to="/minha-conta">
        <v-icon>mdi-account</v-icon>
      </v-btn>

      <v-btn class="ma-2" text icon @click="logout = true">
        <v-icon>mdi-exit-to-app</v-icon>
      </v-btn>
    </v-app-bar>
    <!-- END -->

    <v-dialog v-model="logout" persistent max-width="350">
      <v-card>
        <v-card-title class="headline">Sair da Panificadora</v-card-title>
        <v-card-text>Voce será redirecionado para a tela de Login.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="logout = false">Cancelar</v-btn>
          <v-btn color="red darken-1" text @click="doLogout()">Confirmar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: "Menu",
  data: () => ({
    drawer: null,
    logout: false
  }),
  methods: {
    doLogout() {
      this.$root.$children[0].$refs.notification.makeNotification(
        "success",
        "Logout efetuado com sucesso :)"
      );
      this.logout = false;
    }
  }
};
</script>