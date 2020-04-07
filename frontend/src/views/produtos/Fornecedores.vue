<template>
  <v-container fluid grid-list-md>
    <v-layout row wrap>
      <v-flex lg12 md12 xs12>
        <v-data-table :headers="headers" :items="fornecedores" :search="search" class="elevation-1">
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>Produtos - Fornecedores</v-toolbar-title>
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
              <v-dialog v-model="dialog" max-width="640px" persistent>
                <v-form v-model="validRegistro" ref="formRegistro">
                  <v-card>
                    <v-card-title>
                      <span class="headline">{{ formTitle }}</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.cnpj"
                              v-mask="'##.###.###/####-##'"
                              label="CNPJ"
                              :counter="18"
                              required
                            >
                              <v-icon slot="prepend" color="primary">mdi-card-account-details-outline</v-icon>
                            </v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-text-field
                              v-model="editedItem.nome"
                              label="Nome"
                              :counter="45"
                              required
                              clearable
                            >
                              <v-icon slot="prepend" color="primary">mdi-rename-box</v-icon>
                            </v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="red" text @click="close">Cancelar</v-btn>
                      <v-btn color="green" text @click="save">Salvar</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-form>
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:item.acoes="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
            <v-icon small @click="callDeleteItem(item)">mdi-delete</v-icon>
          </template>
        </v-data-table>
      </v-flex>

      <!-- Dialogo de remoção -->
      <v-dialog v-model="dialog_del" persistent max-width="400">
        <v-card>
          <v-card-title class="headline">Remover Fornecedor</v-card-title>
          <v-card-text>Tem certeza de que deseja remover o Fornecedor selecionado?</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" text @click="dialog_del = false">Cancelar</v-btn>
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

export default {
  name: "Fornecedores",
  data() {
    return {
      search: "",
      dialog: false,
      dialog_del: false,
      validRegistro: false,
      regras: {},
      headers: [
        { text: "CNPJ", value: "cnpj" },
        { text: "Nome", value: "Nome" },
        { text: "Ações", value: "acoes", sortable: false }
      ],
      fornecedores: [],
      editedIndex: -1,
      deletedIndex: -1,
      editedItem: {
        id: "",
        cnpj: "",
        nome: ""
      },
      defaultItem: {
        id: "",
        cnpj: "",
        nome: ""
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
      this.fornecedores = [];
      var vm = this;
      axios
        .get("http://127.0.0.1:5000/fornecedores", {
          headers: {
            Authorization: getAuthorization(),
            "Content-Type": "application/json"
          }
        })
        .then(function(response) {
          if (response.status == 200) {
            response.data.forEach(item => {
              vm.fornecedores.push({
                id: item.id,
                cnpj: item.cnpj,
                nome: item.nome
              });
            });
          }
        })
        .catch(error => {
          console.log(error);
          if (error.response.status != 304) {
            vm.$root.$children[0].$refs.notification.makeNotification(
              "error",
              "Houve um erro ao buscar a listagem de fornecedores"
            );
          }
        });
    },

    editItem(item) {
      this.editedIndex = this.fornecedores.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    callDeleteItem(item) {
      const index = this.fornecedores.indexOf(item);
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
            "http://127.0.0.1:5000/fornecedores",
            {
              deletedId: this.fornecedores[this.deletedIndex].id
            },
            {
              headers: {
                Authorization: getAuthorization(),
                "Content-Type": "application/json"
              }
            }
          )
          .then(function(response) {
            if (response.status == 200) {
              vm.$root.$children[0].$refs.notification.makeNotification(
                "success",
                "Fornecedor removido com sucesso!"
              );
              vm.initialize();
            } else {
              vm.$root.$children[0].$refs.notification.makeNotification(
                "warning",
                response.data
              );
            }
          })
          .catch(error => {
            vm.$root.$children[0].$refs.notification.makeNotification(
              "error",
              "Erro ao remover Fornecedor"
            );
            console.log(error.reponseData);
          });
      } else {
        axios
          .post(
            "http://127.0.0.1:5000/fornecedores",
            {
              cnpj: this.editedItem.cnpj,
              nome: this.editedItem.nome
            },
            {
              headers: {
                Authorization: getAuthorization(),
                "Content-Type": "application/json"
              }
            }
          )
          .then(function(response) {
            if (response.status == 200) {
              vm.$root.$children[0].$refs.notification.makeNotification(
                "success",
                "Fornecedor cadastrado com sucesso!"
              );
              vm.initialize();
            } else {
              vm.$root.$children[0].$refs.notification.makeNotification(
                "warning",
                response.data
              );
            }
          })
          .catch(error => {
            vm.$root.$children[0].$refs.notification.makeNotification(
              "error",
              "Erro ao cadastrar Fornecedor"
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