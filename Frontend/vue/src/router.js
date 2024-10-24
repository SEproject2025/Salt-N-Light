import Vue from 'vue'
import Router from 'vue-router'
import AppHome from './components/AppHome.vue'
import AppLogin from './components/AppLogin.vue'

Vue.use(Router)
export default Router({
    routes: [
        {path:'/', component: AppHome},
        {path:'/AppLogin',component: AppLogin}
    ]
})