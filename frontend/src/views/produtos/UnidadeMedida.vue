<template>
  <v-container fluid grid-list-md>
    <v-layout row wrap>
      <v-flex lg12 md12 xs12>
        <v-data-table :headers="headers" :items="unidades" :search="search" class="elevation-1">
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>Produtos - Unidade Medida</v-toolbar-title>
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
                          <v-col cols="12" sm="12" md="6">
                            <v-text-field
                              v-model="editedItem.abreviacao"
                              label="Abreviação"
                              :counter="3"
                              required
                            >
                              <v-icon slot="prepend" color="primary">mdi-barcode</v-icon>
                            </v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="6">
                            <v-text-field
                              v-model="editedItem.descricao"
                              label="Descrição"
                              :counter="45"
                              required
                              clearable
                            >
                              <v-icon slot="prepend" color="primary">mdi-rename-box</v-icon>
                            </v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="12">
                            <v-checkbox
                              v-model="editedItem.fracionavel"
                              label="Fracionável"
                              required
                            ></v-checkbox>
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
          <template
            v-slot:item.fracionavel="{ item }"
          >{{ item.fracionavel == true ? 'Sim' : 'Não' }}</template>
          <template v-slot:item.acoes="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
            <v-icon small @click="callDeleteItem(item)">mdi-delete</v-icon>
          </template>
        </v-data-table>
      </v-flex>

      <!-- Dialogo de remoção -->
      <v-dialog v-model="dialog_del" persistent max-width="400">
        <v-card>
          <v-card-title class="headline">Remover Unidade de Medida</v-card-title>
          <v-card-text>Tem certeza de que deseja remover a Unidade de Medida selecionada?</v-card-text>
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
  name: "UnidadeMedida",
  data() {
    return {
      search: "",
      dialog: false,
      dialog_del: false,
      validRegistro: false,
      regras: {},
      headers: [
        { text: "Abreviação", value: "abreviacao" },
        { text: "Descrição", value: "descricao" },
        { text: "Fracionável", value: "fracionavel" },
        { text: "Ações", value: "acoes", sortable: false }
      ],
      unidades: [],
      editedIndex: -1,
      deletedIndex: -1,
      editedItem: {
        id: "",
        abreviacao: "",
        descricao: "",
        fracionavel: false
      },
      defaultItem: {
        id: null,
        abreviacao: "",
        descricao: "",
        fracionavel: false
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
      this.unidades = [];
      var vm = this;
      axios
        .get("http://127.0.0.1:5000/unidade-medida", {
          headers: {
            Authorization: getAuthorization(),
            "Content-Type": "application/json"
          }
        })
        .then(function(response) {
          if (response.status == 200) {
            response.data.forEach(item => {
              vm.unidades.push({
                id: item.id,
                abreviacao: item.abreviacao,
                descricao: item.descricao,
                fracionavel: item.fracionavel
              });
            });
          }
        })
        .catch(error => {
          console.log(error);
          if (error.response.status != 304) {
            vm.$root.$children[0].$refs.notification.makeNotification(
              "error",
              "Houve um erro ao buscar a listagem de unidade de medida"
            );
          }
        });
    },

    editItem(item) {
      this.editedIndex = this.unidades.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    callDeleteItem(item) {
      const index = this.unidades.indexOf(item);
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
            "http://127.0.0.1:5000/unidade-medida",
            {
              deletedId: this.unidades[this.deletedIndex].id
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
                "Unidade de Medida removida com sucesso!"
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
              "Erro ao remover a Unidade de Medida"
            );
            console.log(error.reponseData);
          });
      } else {
        axios
          .post(
            "http://127.0.0.1:5000/unidade-medida",
            {
              abreviacao: this.editedItem.abreviacao,
              descricao: this.editedItem.descricao,
              fracionavel: this.editedItem.fracionavel
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
                "Unidade de Medida cadastrada com sucesso!"
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
              "Erro ao cadastrar a Unidade de Medida"
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