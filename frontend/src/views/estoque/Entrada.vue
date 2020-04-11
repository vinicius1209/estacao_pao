<template>
  <v-container fluid grid-list-md>
    <v-layout row wrap>
      <v-flex lg12 md12 xs12>
        <v-data-table
          :headers="headers_entrada"
          :items="entradas"
          :search="search"
          class="elevation-1"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>Entrada de Produtos</v-toolbar-title>
              <v-spacer></v-spacer>
              <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Buscar"
                single-line
                hide-details
              ></v-text-field>
              <v-toolbar-items>
                <v-btn text color="primary" @click="dialog = true">Novo</v-btn>
              </v-toolbar-items>
              <!--Dialogo de inserção / edição -->
              <v-dialog
                v-model="dialog"
                fullscreen
                hide-overlay
                transition="dialog-bottom-transition"
                persistent
              >
                <v-card class="elevation-3">
                  <v-toolbar dark color="primary">
                    <v-btn icon dark @click="close">
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                    <v-toolbar-title>{{ formTitle }}</v-toolbar-title>
                  </v-toolbar>
                  <v-card-text>
                    <v-container fluid grid-list-md>
                      <v-stepper v-model="step_cadastro">
                        <v-stepper-header>
                          <v-stepper-step
                            :complete="step_cadastro > 1"
                            editable
                            step="1"
                          >Seleção de Produtos</v-stepper-step>
                          <v-divider></v-divider>
                          <v-stepper-step editable step="2" :complete="step_cadastro > 2">Quantidade</v-stepper-step>
                        </v-stepper-header>
                        <v-stepper-items>
                          <v-stepper-content step="1">
                            <v-data-table
                              :headers="headers_selecao"
                              :items="produtos"
                              :search="search_produtos"
                              multi-sort
                              item-key="id"
                              show-select
                              :loading="carregando_table"
                              loading-text="Buscando registros..."
                              class="elevation-1"
                              @item-selected="selecionaItem"
                              @toggle-select-all="selecionaTodos"
                            >
                              <template v-slot:top>
                                <v-toolbar flat>
                                  <v-toolbar-title>Produtos</v-toolbar-title>
                                  <v-spacer></v-spacer>
                                  <v-text-field
                                    v-model="search_produtos"
                                    append-icon="mdi-magnify"
                                    label="Buscar"
                                    single-line
                                    hide-details
                                  ></v-text-field>
                                  <v-toolbar-items></v-toolbar-items>
                                </v-toolbar>
                              </template>
                              <template v-slot:item.qtd_estoque="{ item }">
                                <v-chip
                                  :color="getColor(item.qtd_estoque, item.qtd_min)"
                                  dark
                                >{{ item.qtd_estoque }}</v-chip>
                              </template>
                              <template v-slot:item.preco_compra="{ item }">R$ {{item.preco_compra}}</template>
                              <template v-slot:item.preco_venda="{ item }">R$ {{item.preco_venda}}</template>
                              <template v-slot:item.unidade="{ item }">{{item.unidade.abreviacao}}</template>
                              <template
                                v-slot:item.ativado="{ item }"
                              >{{ item.ativado == true ? 'Ativado' : 'Desativado' }}</template>
                            </v-data-table>
                            <v-row>
                              <v-col>
                                <v-btn
                                  color="primary"
                                  :disabled="editedItem.produtos.length == 0 ? true : false"
                                  @click="step_cadastro = 2"
                                >Continuar</v-btn>
                              </v-col>
                            </v-row>
                          </v-stepper-content>
                          <v-stepper-content step="2">
                            <v-data-table
                              :headers="headers_produtos"
                              :items="editedItem.produtos"
                              multi-sort
                              item-key="id"
                              class="elevation-1"
                            >
                              <template v-slot:item.qtd_entrada="{item}">
                                <v-edit-dialog :return-value.sync="item.qtd_entrada">
                                  {{ item.qtd_entrada }}
                                  <template v-slot:input>
                                    <v-text-field
                                      v-model="item.qtd_entrada"
                                      label="Quantidade"
                                      single-line
                                      type="number"
                                    ></v-text-field>
                                  </template>
                                </v-edit-dialog>
                              </template>
                            </v-data-table>
                            <v-row>
                              <v-col>
                                <v-btn
                                  color="primary"
                                  :disabled="editedItem.produtos.qtd_entrada ? true : false"
                                  @click="saveItem"
                                >Salvar</v-btn>
                              </v-col>
                            </v-row>
                          </v-stepper-content>
                        </v-stepper-items>
                      </v-stepper>
                    </v-container>
                  </v-card-text>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:item.acoes="{ item }">
            <v-icon small @click="callDeleteItem(item)">mdi-delete</v-icon>
          </template>
        </v-data-table>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script>
import EntradaService from "../../services/EntradaService.js";
import ProdutoService from "../../services/ProdutoService.js";

export default {
  name: "Entrada",
  data() {
    return {
      search: "",
      search_produtos: "",
      step_cadastro: 1,
      carregando_table: false,
      dialog: false,
      validRegistro: false,
      selected: [],
      entradas: [],
      produtos: [],
      headers_entrada: [
        { text: "ID", value: "id" },
        { text: "Data", value: "data" },
        { text: "Entrada por", value: "usuario", sortable: false }
      ],
      headers_selecao: [
        { text: "Código", value: "cod_venda" },
        { text: "Descrição", value: "nome" },
        { text: "Estoque", value: "qtd_estoque" },
        { text: "Unidade Medida", value: "unidade" },
        { text: "Preço de Compra", value: "preco_compra" },
        { text: "Preço de Venda", value: "preco_venda" },
        { text: "Ativado", value: "ativado" }
      ],
      headers_produtos: [
        { text: "Código", value: "cod_venda" },
        { text: "Descrição", value: "nome" },
        { text: "Quantidade", value: "qtd_entrada" }
      ],
      deletedIndex: -1,
      editedItem: {
        id: "",
        data: "",
        usuario: "",
        produtos: []
      },
      defaultItem: {
        id: "",
        data: "",
        usuario: "",
        produtos: []
      }
    };
  },
  created() {
    this.initialize();
  },
  computed: {
    formTitle() {
      return this.deletedIndex === -1 ? "Nova Entrada" : "Estornar Entrada";
    }
  },
  methods: {
    initialize() {
      ProdutoService.get().then(data => {
        this.produtos = data;
      });
      EntradaService.get().then(data => {
        this.entradas = data;
      });
    },
    checkItemSelecionado(item) {
      return item.value == true;
    },
    checkQtdVazia(item){
      return item.qtd_entrada == '';
    },
    selecionaItem(item) {
      const index = this.editedItem.produtos.indexOf(item.item);
      if (index > -1) {
        if (item.value == false) {
          this.editedItem.produtos.splice(index, 1);
        } else {
          this.editedItem.produtos.push(item.item);
        }
      } else {
        this.editedItem.produtos.push(item.item);
      }
      console.log(this.editedItem);
    },
    selecionaTodos(items) {
      if (items.value) {
        this.editedItem.produtos = Object.assign([], items.items);
      } else {
        this.editedItem.produtos = Object.assign(
          [],
          items.items.filter(this.checkItemSelecionado)
        );
      }
      console.log(this.editedItem);
    },
    getColor(qtd, min) {
      if (qtd == 0) return "red";
      else if (qtd <= min) return "orange";
      else return "green";
    },
    saveItem() {
      if (this.editedItem.produtos.length > 0) {
        console.log(this.editedItem);
        /*
        EntradaService.post(this.editedItem.produtos).then(data => {
          if (data.status == 200) {
            this.$root.$children[0].$refs.notification.makeNotification(
              "success",
              data.msg
            );
            //this.initialize();
            this.close();
          } else {
            this.$root.$children[0].$refs.notification.makeNotification(
              "warning",
              data.msg
            );
          }
        });
        */
      }
    },
    close() {
      this.dialog = false;
      this.dialog_del = false;
      this.deletedIndex = -1;
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.$refs.formRegistro.resetValidation();
        this.$refs.formRegistro.reset();
      }, 300);
    }
  }
};
</script>