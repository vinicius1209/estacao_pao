<template>
  <v-container fluid grid-list-md>
    <v-layout row wrap>
      <v-flex lg12 md12 xs12>
        <v-data-table
          :headers="headers"
          :items="produtos"
          :search="search"
          multi-sort
          :loading="carregando_table"
          loading-text="Buscando registros..."
          class="elevation-1"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>Produtos</v-toolbar-title>
              <v-spacer></v-spacer>
              <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Buscar"
                single-line
                hide-details
              ></v-text-field>
              <v-toolbar-items>
                <v-btn text @click="dialog = true" color="primary">Novo</v-btn>
              </v-toolbar-items>
              <!--Dialogo de inserção / edição -->
              <v-dialog v-model="dialog" max-width="640px" persistent>
                <v-form v-model="validRegistro" ref="formRegistro">
                  <v-card>
                    <v-card-title>
                      <span
                        class="headline"
                        v-if="editedItem.cod_venda != ''"
                      >{{ formTitle }} - {{ editedItem.cod_venda }}</span>
                      <span class="headline" v-else>{{ formTitle }}</span>
                    </v-card-title>
                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="12" md="6">
                            <v-text-field
                              v-model="editedItem.cod_venda"
                              label="Código"
                              :counter="10"
                              type="number"
                              required
                            >
                              <v-icon slot="prepend" color="primary">mdi-barcode</v-icon>
                            </v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="6">
                            <v-text-field
                              v-model="editedItem.nome"
                              label="Descrição"
                              :counter="120"
                              required
                              clearable
                            >
                              <v-icon slot="prepend" color="primary">mdi-rename-box</v-icon>
                            </v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="6">
                            <v-text-field
                              v-model="editedItem.preco_compra"
                              v-money="money"
                              label="Preço de Compra"
                              required
                            >
                              <v-icon slot="prepend" color="primary">mdi-currency-brl</v-icon>
                            </v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="6">
                            <v-text-field
                              v-model="editedItem.preco_venda"
                              v-money="money"
                              label="Preço de Venda"
                              required
                            >
                              <v-icon slot="prepend" color="primary">mdi-currency-brl</v-icon>
                            </v-text-field>
                          </v-col>
                          <v-col cols="12" sm="12" md="6">
                            <v-combobox
                              v-model="editedItem.unidade"
                              :items="unidades"
                              item-value="id"
                              item-text="abreviacao"
                              label="Unidade Medida"
                            >
                              <v-icon slot="prepend" color="primary">mdi-format-list-bulleted-type</v-icon>
                            </v-combobox>
                          </v-col>
                          <v-col cols="12" sm="12" md="6">
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
                      <v-btn color="green" text @click="save">Salvar</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-form>
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:item.qtd_estoque="{ item }">
            <v-chip :color="getColor(item.qtd_estoque, item.qtd_min)" dark>{{ item.qtd_estoque }}</v-chip>
          </template>
          <template v-slot:item.preco_compra="{ item }">R$ {{item.preco_compra}}</template>
          <template v-slot:item.preco_venda="{ item }">R$ {{item.preco_venda}}</template>
          <template v-slot:item.unidade="{ item }">{{item.unidade.abreviacao}}</template>
          <template
            v-slot:item.ativado="{ item }"
          >{{ item.ativado == true ? 'Ativado' : 'Desativado' }}</template>
          <template v-slot:item.acoes="{ item }">
            <v-icon
              small
              class="mr-2"
              @click="callChangeStatusItem(item)"
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
      <!-- end -->

      <!-- Dialogo de status -->
      <v-dialog v-model="dialog_status" persistent max-width="350">
        <v-card>
          <v-card-title class="headline">Alterar status do Item</v-card-title>
          <v-card-text>Tem certeza de que deseja alterar o status do item selecionado para: {{ editedItem.ativado }}?</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" text @click="close">Cancelar</v-btn>
            <v-btn color="red darken-1" text @click="save">Confirmar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <!-- end -->
    </v-layout>
  </v-container>
</template>
<script>
import CategoriaService from "../../services/CategoriaService.js";
import FornecedorService from "../../services/FornecedorService.js";
import UnidadeMedidaService from "../../services/UnidadeMedidaService.js";
import ProdutoService from "../../services/ProdutoService.js";

export default {
  name: "Produto",
  data() {
    return {
      search: "",
      carregando_table: false,
      dialog: false,
      dialog_del: false,
      dialog_status: false,
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
        { text: "Código", value: "cod_venda" },
        { text: "Descrição", value: "nome" },
        { text: "Estoque", value: "qtd_estoque" },
        { text: "Unidade Medida", value: "unidade" },
        { text: "Preço de Compra", value: "preco_compra" },
        { text: "Preço de Venda", value: "preco_venda" },
        { text: "Ativado", value: "ativado" },
        { text: "Ações", value: "acoes", sortable: false }
      ],
      produtos: [],
      fornecedores: [],
      categorias: [],
      unidades: [],
      editedIndex: -1,
      deletedIndex: -1,
      editedItem: {
        id: "",
        nome: "",
        cod_venda: "",
        unidade: "",
        preco_venda: "",
        preco_compra: "",
        qtd_min: "",
        categoria: "",
        fornecedor: "",
        ativado: false
      },
      defaultItem: {
        id: "",
        nome: "",
        cod_venda: "",
        unidade: "",
        preco_venda: "",
        preco_compra: "",
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
      this.carregando_table = true;
      CategoriaService.get().then(data => {
        this.categorias = data;
      });
      FornecedorService.get().then(data => {
        this.fornecedores = data;
      });
      UnidadeMedidaService.get().then(data => {
        this.unidades = data;
      });
      ProdutoService.get().then(data => {
        this.produtos = data;
        this.carregando_table = false;
      });
    },

    editItem(item) {
      this.editedIndex = this.produtos.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    callChangeStatusItem(item) {
      this.editedIndex = this.produtos.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.editedItem.ativado = !this.editedItem.ativado;
      this.dialog_status = true;
    },

    callDeleteItem(item) {
      const index = this.produtos.indexOf(item);
      this.deletedIndex = index;
      this.dialog_del = true;
    },

    close() {
      this.dialog = false;
      this.dialog_del = false;
      this.dialog_status = false;
      this.deletedIndex = -1;
      this.editedIndex = -1;
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.$refs.formRegistro.resetValidation();
        this.$refs.formRegistro.reset();
      }, 300);
    },

    save() {
      if (this.deletedIndex > -1) {
        ProdutoService.delete(this.produtos[this.deletedIndex].id).then(
          response => {
            if (response.status == 200) {
              this.$root.$children[0].$refs.notification.makeNotification(
                "success",
                response.msg
              );
              this.initialize();
            } else {
              this.$root.$children[0].$refs.notification.makeNotification(
                "warning",
                response.msg
              );
            }
          }
        );
      } else {
        ProdutoService.post(
          this.editedItem.id,
          this.editedItem.nome,
          this.editedItem.cod_venda,
          this.editedItem.preco_venda,
          this.editedItem.preco_compra,
          this.editedItem.qtd_min,
          this.editedItem.ativado,
          this.editedItem.unidade,
          this.editedItem.categoria,
          this.editedItem.fornecedor
        ).then(response => {
          if (response.status == 200) {
            this.$root.$children[0].$refs.notification.makeNotification(
              "success",
              response.msg
            );
            this.initialize();
          } else {
            this.$root.$children[0].$refs.notification.makeNotification(
              "warning",
              response.msg
            );
          }
        });
      }
      this.close();
    },

    getColor(qtd, min) {
      if (qtd == 0) return "red";
      else if (qtd <= min) return "orange";
      else return "green";
    }
  }
};
</script>
<style scoped>
</style>