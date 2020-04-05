<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-toolbar dark color="primary">
          <v-toolbar-title>Pães e Variedades</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>

        <v-tabs centered v-model="view">
          <v-tab :href="`#tab-login`">Entrar</v-tab>
          <v-tab :href="`#tab-signup`">Registrar-se</v-tab>
        </v-tabs>

        <v-tabs-items v-model="view">
          <!-- Tab login -->
          <v-tab-item :value="`tab-login`">
            <v-card flat>
              <v-card-text>
                <v-form ref="login_form" :model="login_form" lazy-validation>
                  <v-text-field
                    prepend-icon="mdi-account"
                    label="Usuário"
                    type="text"
                    v-model="login_form.username"
                    :rules="login_form.rules.usernameRules"
                    :counter="64"
                    required
                  ></v-text-field>
                  <v-text-field
                    prepend-icon="mdi-lock"
                    label="Senha"
                    type="password"
                    v-model="login_form.password"
                    :rules="login_form.rules.passwordRules"
                    required
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-btn color="primary" @click="doLogin()">Entrar</v-btn>
              </v-card-actions>
            </v-card>
          </v-tab-item>
          <!-- Tab signup -->
          <v-tab-item :value="`tab-signup`">
            <v-card flat>
              <v-card-text>
                <v-form ref="signup_form" :model="signup_form" lazy-validation>
                  <v-text-field
                    prepend-icon="mdi-account"
                    label="Usuário"
                    type="text"
                    v-model="signup_form.username"
                    :counter="64"
                    required
                  ></v-text-field>
                  <v-text-field
                    prepend-icon="mdi-lock"
                    label="Senha"
                    type="password"
                    v-model="signup_form.password"
                    required
                  ></v-text-field>
                  <v-text-field
                    prepend-icon="mdi-lock"
                    label="Confirmar Senha"
                    type="password"
                    v-model="signup_form.repassword"
                    required
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-btn color="primary" @click="doSignup()">Registrar</v-btn>
              </v-card-actions>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import {login} from '../auth.js';

export default {
  name: "Login",
  props: {
    source: String
  },
  data: () => ({
    view: "tab-login",
    login_form: {
      username: "",
      password: "",
      rules: {
        usernameRules: [
          v => !!v || "É necessário preencher o Usuário",
          v => v.length <= 64 || "Usuário deve possuir até 64 characters"
        ],
        passwordRules: [v => !!v || "É necessário preencher a Senha"]
      }
    },
    signup_form: {
      username: "",
      password: "", 
      repassword: ""
    },
    valid: false
  }),
  methods: {
    doLogin() {
      var vm = this
      if (this.$refs.login_form.validate()) {
        axios
          .post(
            "http://127.0.0.1:5000/auth",
            {
              username: this.login_form.username,
              password: this.login_form.password
            },
            {
              headers: {
                "Content-Type": "application/json"
              }
            }
          )
          .then(function(response) {
            if (response.status == "200") {
              login(response.data.access_token);
              window.location.href = '/dashboard';
            } else {
              vm.$root.$children[0].$refs.notification.makeNotification(
                "warning",
                response.statusText
              );
            }
          })
          .catch(error => {
            vm.$root.$children[0].$refs.notification.makeNotification(
              "error",
              "Erro ao efetuar o login do usuário"
            );
            console.log(error);
          });
      }
    },
    doSignup() {
      if (this.$refs.signup_form.validate()) {
        var vm = this;
        axios
          .post(
            "http://127.0.0.1:5000/signup",
            {
              username: this.signup_form.username,
              password: this.signup_form.password
            },
            {
              headers: {
                "Content-Type": "application/json"
              }
            }
          )
          .then(function(response) {
            if (response.data.status == "200") {
              vm.$root.$children[0].$refs.notification.makeNotification(
                "success",
                "Registro efetuado com sucesso"
              );
              vm.view = "tab-login";
            } else {
              vm.$root.$children[0].$refs.notification.makeNotification(
                "warning",
                response.data.msg
              );
            }
          })
          .catch(error => {
            console.log(error);
            vm.$root.$children[0].$refs.notification.makeNotification(
              "error",
              "Erro ao efetuar o registro de usuário"
            );
          });
      }
    }
  }
};
</script>