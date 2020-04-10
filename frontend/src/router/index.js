import Vue from 'vue'
import VueRouter from 'vue-router'
import { isLoged } from '../auth.js'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import Venda from '../views/caixa/Venda.vue'
import Produto from '../views/estoque/Produto.vue'
import Entrada from '../views/estoque/Entrada.vue'
import UnidadeMedida from '../views/configuracoes/UnidadeMedida.vue'
import Fornecedor from '../views/configuracoes/Fornecedor.vue'
import Categoria from '../views/configuracoes/Categoria.vue';

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      title: 'Login',
      metaTags: [
        {
          name: 'description',
          content: 'The Login page of Panificadora.'
        },
        {
          property: 'og:description',
          content: 'The Login page of Panificadora.'
        }
      ]
    }
  },
  {
    path: '/dashboard',
    name: 'Home',
    component: Home,
    meta: {
      title: 'Panificadora',
      metaTags: [
        {
          name: 'description',
          content: 'The home page of Panificadora.'
        },
        {
          property: 'og:description',
          content: 'The home page of Panificadora.'
        }
      ]
    }
  },
  {
    path: '/caixa/venda',
    name: 'Venda',
    component: Venda,
    meta: {
      title: 'Venda',
      metaTags: [
        {
          name: 'description',
          content: 'The Venda page of Panificadora.'
        },
        {
          property: 'og:description',
          content: 'The Venda page of Panificadora.'
        }
      ]
    }
  },
  {
    path: '/estoque/produtos',
    name: 'Produtos',
    component: Produto,
    meta: {
      title: 'Produto',
      metaTags: [
        {
          name: 'description',
          content: 'The Produto page of Panificadora.'
        },
        {
          property: 'og:description',
          content: 'The Produto page of Panificadora.'
        }
      ]
    }
  },
  {
    path: '/estoque/entrada',
    name: 'Entrada',
    component: Entrada,
    meta: {
      title: 'Entrada',
      metaTags: [
        {
          name: 'description',
          content: 'The Entrada page of Panificadora.'
        },
        {
          property: 'og:description',
          content: 'The Entrada page of Panificadora.'
        }
      ]
    }
  },
  {
    path: '/configuracoes/unidade-medida',
    name: 'UnidadeMedida',
    component: UnidadeMedida,
    meta: {
      title: 'Unidade',
      metaTags: [
        {
          name: 'description',
          content: 'The Unidade Medida page of Panificadora.'
        },
        {
          property: 'og:description',
          content: 'The Unidade Medida page of Panificadora.'
        }
      ]
    }
  },
  {
    path: '/configuracoes/fornecedores',
    name: 'Fornecedor',
    component: Fornecedor,
    meta: {
      title: 'Fornecedores',
      metaTags: [
        {
          name: 'description',
          content: 'The Fornecedores page of Panificadora.'
        },
        {
          property: 'og:description',
          content: 'The Fornecedores page of Panificadora.'
        }
      ]
    }
  },
  {
    path: '/configuracoes/categorias',
    name: 'Categoria',
    component: Categoria,
    meta: {
      title: 'Categorias',
      metaTags: [
        {
          name: 'description',
          content: 'The Categorias page of Panificadora.'
        },
        {
          property: 'og:description',
          content: 'The Categorias page of Panificadora.'
        }
      ]
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})


router.beforeEach((to, from, next) => {

  if (to.path != '/login' && to.path != '/register' && to.path != '/auth') {
    if (isLoged()) {

      const nearestWithTitle = to.matched.slice().reverse().find(r => r.meta && r.meta.title);
      const nearestWithMeta = to.matched.slice().reverse().find(r => r.meta && r.meta.metaTags);

      if (nearestWithTitle) document.title = nearestWithTitle.meta.title;

      Array.from(document.querySelectorAll('[data-vue-router-controlled]')).map(el => el.parentNode.removeChild(el));

      if (!nearestWithMeta) return next();

      nearestWithMeta.meta.metaTags.map(tagDef => {
        const tag = document.createElement('meta');

        Object.keys(tagDef).forEach(key => {
          tag.setAttribute(key, tagDef[key]);
        });

        tag.setAttribute('data-vue-router-controlled', '');

        return tag;
      }).forEach(tag => document.head.appendChild(tag));

      next();
    } else {
      window.location.href = '/login';
    }
  }
  else if (to.path == '/login' || to.path == '/register' || to.path == '/auth') {
    next();
  }
  else {
    window.location.href = '/login';
  }
});

export default router