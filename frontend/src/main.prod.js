// Vue Imports
import Vue from 'vue'

import BootstrapVue from 'bootstrap-vue'
import VueSweetalert2 from "vue-sweetalert2";
import VueIziToast from "vue-izitoast";
import Multiselect from 'vue-multiselect'
import VueCookies from 'vue-cookies'
import axios from 'axios'
import VueAxios from 'vue-axios'
import Vuex from 'vuex'
import VuexPersistence from "vuex-persist";
import {
    ValidationObserver,
    ValidationProvider,
    extend,
    localize
} from "vee-validate";
import en from "vee-validate/dist/locale/en.json";
import * as rules from "vee-validate/dist/rules";

// Other JS imports
import '@fortawesome/fontawesome-free/js/all.js'

// Local imports
import App from './App.vue'
import router from './router'
import i18n from './i18n'

// Install VeeValidate rules and localization
Object.keys(rules).forEach(rule => {
    extend(rule, rules[rule]);
});
localize("en", en);
// Install VeeValidate components globally
Vue.component("ValidationObserver", ValidationObserver);
Vue.component("ValidationProvider", ValidationProvider);

// JS Options
const iziToastOptions = {
    closeOnClick: true,
    drag: false,
    position: "topCenter",
    transitionIn: 'revealIn',
    transitionOut: 'fadeOut'
}

// Vue module registration
Vue.use(BootstrapVue)
Vue.use(VueSweetalert2)
Vue.use(VueIziToast, iziToastOptions);
Vue.use(VueCookies)
Vue.use(VueAxios, axios)
Vue.use(Vuex)
Vue.config.productionTip = false

Vue.component('multiselect', Multiselect)

// Combined style
import "@/assets/scss/index.scss"

// Vuex
const vuexStorage = new VuexPersistence({
    key: 'vuex',
    storage: window.localStorage
})

const store = new Vuex.Store({
    state: {
        backendURL: "",
        userToken: "",
        user: null,
        loggedIn: false
    },
    mutations: {
        setUserToken(state, userToken) {
            state.userToken = userToken
        },
        setUser(state, user) {
            state.user = user
        },
        setLoggedIn(state, logInStatus) {
            state.loggedIn = logInStatus
        }
    },
    plugins: [vuexStorage.plugin]
})

new Vue({
    router,
    i18n,
    store,
    render: h => h(App)
}).$mount('#app')

