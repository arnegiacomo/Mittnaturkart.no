import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import Lara from '@primevue/themes/lara'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'
import App from './App.vue'
import { primeVueNbNO } from './i18n/primevue-nb-NO'

import 'primeicons/primeicons.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(PrimeVue, {
  theme: {
    preset: Lara,
    options: {
      darkModeSelector: false
    }
  },
  locale: primeVueNbNO
})
app.use(ToastService)
app.use(ConfirmationService)

app.mount('#app')
