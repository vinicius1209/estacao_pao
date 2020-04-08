<template>
  <v-container fluid grid-list-md>
    <v-layout row wrap>
      <v-flex lg12 md12 xs12>
        <v-data-table :headers="headers" :items="produtos" class="elevation-1">
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>Produtos - Itens</v-toolbar-title>
              <v-spacer></v-spacer>
              <v-toolbar-items>
                <v-btn text @click="dialog = true">Novo</v-btn>
              </v-toolbar-items>
              <!--Dialogo de inserção / edição -->
              <v-dialog v-model="dialog" max-width="640px" persistent>
                <v-form v-model="validRegistro" ref="formRegistro">
                  <v-card>
                    <v-card-title>
                      <span class="headline">{{ formTitle }} - {{ editedItem.codigo }}</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.codigo"
                              label="Código"
                              :counter="10"
                              type="number"
                              required
                            >
                              <v-icon slot="prepend" color="primary">mdi-barcode</v-icon>
                            </v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.descricao"
                              label="Descrição"
                              :counter="120"
                              required
                              clearable
                            >
                              <v-icon slot="prepend" color="primary">mdi-rename-box</v-icon>
                            </v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="4">
                            <v-combobox
                              v-model="editedItem.unidade_medida"
                              :items="unidades"
                              item-value="id"
                              item-text="abreviacao"
                              label="Unidade Medida"
                            >
                              <v-icon slot="prepend" color="primary">mdi-format-list-bulleted-type</v-icon>
                            </v-combobox>
                          </v-col>
                          <v-col cols="12" sm="12" md="4">
                            <v-text-field
                              v-model="editedItem.preco"
                              v-money="money"
                              label="Preço"
                              required
                            >
                              <v-icon slot="prepend" color="primary">mdi-currency-brl</v-icon>
                            </v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="4">
                            <v-text-field
                              v-model="editedItem.qtd_min"
                              label="Qtd. Mínima"
                              type="number"
                              required
                            >
                              <v-icon slot="prepend" color="primary">mdi-filter-minus</v-icon>
                            </v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="6">
                            <v-combobox
                              v-model="editedItem.categoria"
                              :items="categorias"
                              item-value="id"
                              item-text="nome"
                              label="Categoria"
                            >
                              <v-icon slot="prepend" color="primary">mdi-clipboard-list-outline</v-icon>
                            </v-combobox>
                          </v-col>
                          <v-col cols="12" sm="12" md="6">
                            <v-combobox
                              v-model="editedItem.fornecedor"
                              :items="fornecedores"
                              item-value="id"
                              item-text="nome"
                              label="Fornecedor"
                            >
                              <v-icon slot="prepend" color="primary">mdi-truck-delivery-outline</v-icon>
                            </v-combobox>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="red" text @click="close">Cancelar</v-btn>
                      <v-btn color="green" text @click="close">Salvar</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-form>
              </v-dialog>
            </v-toolbar>
          </template>
          <template
            v-slot:item.status="{ item }"
          >{{ item.ativado == true ? 'Ativado' : 'Desativado' }}</template>
          <template v-slot:item.acoes="{ item }">
            <v-icon
              small
              class="mr-2"
              @click="changeStatus(item)"
            >{{ item.status === true ? 'mdi-account-cancel' : 'mdi-account-check'}}</v-icon>
            <v-icon small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
            <v-icon small @click="callDeleteItem(item)">mdi-delete</v-icon>
          </template>
        </v-data-table>
      </v-flex>

      <!-- Dialogo de remoção -->
      <v-dialog v-model="dialog_del" persistent max-width="350">
        <v-card>
          <v-card-title class="headline">Remover Item</v-card-title>
          <v-card-text>Tem certeza de que deseja remover o item selecionado?</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" text @click="close">Cancelar</v-btn>
            <v-btn color="red darken-1" text @click="save">Confirmar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
  </v-container>
</template>
<script>
import axios from "axios";
import { getAuthorization } from "../../auth.js";
//import UnidadeMedidaService from "../../services/UnidadeMedidaService.js";

export default {
  name: "Itens",
  data() {
    return {
      dialog: false,
      dialog_del: false,
      validRegistro: false,
      money: {
        decimal: ",",
        thousands: ".",
        prefix: "",
        suffix: "",
        precision: 2,
        masked: false
      },
      regras: {},
      headers: [
        { text: "Descrição", value: "nome" },
        { text: "Código", value: "codigo" },
        { text: "Unidade Medida", value: "unidade_medida" },
        { text: "Preço", value: "preco" },
        { text: "Ativado", value: "ativado" },
        { text: "Ações", value: "acoes", sortable: false }
      ],
      produtos: [],
      fornecedores: [
        { id: 1, nome: "Estação do Pão" },
        { id: 2, nome: "Pão Nosso" }
      ],
      categorias: [
        { id: 1, nome: "Confeitaria" },
        { id: 2, nome: "Padaria" }
      ],
      unidades: [
        { id: 1, abreviacao: "Kg" },
        { id: 2, abreviacao: "G" }
      ],
      editedIndex: -1,
      deletedIndex: -1,
      editedItem: {
        id: "",
        nome: "",
        codigo: "",
        unidade_medida: "",
        preco: "",
        qtd_min: "",
        categoria: "",
        fornecedor: "",
        ativado: false
      },
      defaultItem: {
        id: "",
        nome: "",
        codigo: "",
        unidade_medida: "",
        preco: "",
        qtd_min: "",
        categoria: "",
        fornecedor: "",
        ativado: true
      }
    };
  },
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "Novo Registro" : "Editar Registro";
    }
  },
  created() {
    this.initialize();
  },
  methods: {
    initialize() {
      var vm = this;
      axios
        .get("http://127.0.0.1:5000/produtos", {
          headers: {
            Authorization: getAuthorization(),
            "Content-Type": "application/json"
          }
        })
        .then(function(response) {
          if (response.status == 200) {
            response.data.forEach(item => {
              vm.produtos.push({
                id: item.id,
                nome: item.nome,
                cod_venda: item.cod_venda,
                preco: item.preco,
                qtd_estoque: item.qtd_estoque,
                qtd_min: item.qtd_min,
                ativado: item.ativado,
                unidade: item.unidade,
                categoria: item.categoria,
                fornecedor: item.fornecedor
              });
            });
          }
        })
        .catch(error => {
          vm.$root.$children[0].$refs.notification.makeNotification(
            "error",
            "Erro ao buscar os itens"
          );
          console.log(error);
        });
    },

    editItem(item) {
      this.editedIndex = this.produtos.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    callDeleteItem(item) {
      const index = this.produtos.indexOf(item);
      this.deletedIndex = index;
      this.dialog_del = true;
    },

    close() {
      this.dialog = false;
      this.dialog_del = false;
      this.deletedIndex = -1;
      this.editedIndex = -1;
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.$refs.formRegistro.resetValidation();
        this.$refs.formRegistro.reset();
      }, 300);
    },

    save() {
      var vm = this;
      if (this.deletedIndex > -1) {
        axios
          .post(
            "http://127.0.0.1:5000/produtos",
            {
              deletedId: this.produtos[this.deletedIndex].id
            },
            {
              headers: {
                Authorization: getAuthorization(),
                "Content-Type": "application/json"
              }
            }
          )
          .then(function(response) {
            if (response.data.status == 200) {
              vm.$root.$children[0].$refs.notification.makeNotification(
                "success",
                response.data.msg
              );
              vm.initialize();
            } else {
              vm.$root.$children[0].$refs.notification.makeNotification(
                "warning",
                response.data.msg
              );
            }
          })
          .catch(error => {
            vm.$root.$children[0].$refs.notification.makeNotification(
              "error",
              "Erro ao remover o Produto"
            );
            console.log(error.reponseData);
          });
      } else {
        axios
          .post(
            "http://127.0.0.1:5000/produtos",
            {
                id: this.editedItem.id,
                nome: this.editedItem.nome,
                cod_venda: this.editedItem.cod_venda,
                preco: this.editedItem.preco,
                qtd_estoque: this.editedItem.qtd_estoque,
                qtd_min: this.editedItem.qtd_min,
                ativado: this.editedItem.ativado,
                unidade: this.editedItem.unidade,
                categoria: this.editedItem.categoria,
                fornecedor: this.editedItem.fornecedor
            },
            {
              headers: {
                Authorization: getAuthorization(),
                "Content-Type": "application/json"
              }
            }
          )
          .then(function(response) {
            if (response.data.status == 200) {
              vm.$root.$children[0].$refs.notification.makeNotification(
                "success",
                response.data.msg
              );
              vm.initialize();
            } else {
              vm.$root.$children[0].$refs.notification.makeNotification(
                "warning",
                response.data.msg
              );
            }
          })
          .catch(error => {
            vm.$root.$children[0].$refs.notification.makeNotification(
              "error",
              "Erro ao cadastrar o Produto"
            );
            console.log(error.reponseData);
          });
      }
      this.close();
    }
  }
};
</script>
<style scoped>
</style>