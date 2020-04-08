<template>
  <div id="menu">
    <v-navigation-drawer v-model="drawer" app clipped>
      <v-list dense>
        <!-- Dashboard -->
        <v-list-item link to="/dashboard">
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

        <!-- Produtos -->
        <v-list-group prepend-icon="mdi-package" no-action value="true">
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title>Produtos</v-list-item-title>
            </v-list-item-content>
          </template>

          <v-list-item link to="/itens">
            <v-list-item-content>
              <v-list-item-title>Itens</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item link to="/categorias">
            <v-list-item-content>
              <v-list-item-title>Categorias</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item link to="/fornecedores">
            <v-list-item-content>
              <v-list-item-title>Fornecedores</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item link to="/unidade-medida">
            <v-list-item-content>
              <v-list-item-title>Unidade Medida</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-group>
        <!-- end Produtos -->

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
    <v-app-bar app clipped-left dark color="primary" :value="menu_top">
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
import { isLoged, logout } from "../auth.js";

export default {
  name: "Menu",
  data: () => ({
    drawer: false,
    menu_top: false,
    logout: false
  }),
  mounted: function() {
    if (isLoged()) {
      this.drawer = true;
      this.menu_top = true;
    } else {
      this.drawer = false;
      this.menu_top = false;
    }
  },
  methods: {
    doLogout() {
      logout();
      window.location.href = "/login";
    }
  }
};
</script>