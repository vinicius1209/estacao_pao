import Vue from 'vue'
import VueRouter from 'vue-router'
import { isLoged } from '../auth.js'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import Itens from '../views/produtos/Itens.vue'
import UnidadeMedida from '../views/produtos/UnidadeMedida.vue'
import Fornecedores from '../views/produtos/Fornecedores.vue'
import Categorias from '../views/produtos/Categorias.vue'

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
    path: '/itens',
    name: 'Itens',
    component: Itens,
    meta: {
      title: 'Itens',
      metaTags: [
        {
          name: 'description',
          content: 'The Itens page of Panificadora.'
        },
        {
          property: 'og:description',
          content: 'The Itens page of Panificadora.'
        }
      ]
    }
  },
  {
    path: '/unidade-medida',
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
    path: '/fornecedores',
    name: 'Fornecedores',
    component: Fornecedores,
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
    path: '/categorias',
    name: 'Categorias',
    component: Categorias,
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
      router.push('/login');
    }
  }
  else if (to.path == '/login' || to.path == '/register' || to.path == '/auth') {
    next();
  }
  else {
    router.push('/login');
  }
});

export default router