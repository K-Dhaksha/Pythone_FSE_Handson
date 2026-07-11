import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useErrorStore } from './stores/error'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Global Vue Error Handler configuration
app.config.errorHandler = (err, instance, info) => {
  console.error('[Vue Global Error Intercepted]:', err)
  console.error('Info context:', info)
  
  const errorStore = useErrorStore(pinia) // Pass pinia instance to resolve store outside components
  errorStore.setError(err.message || String(err))
}

app.mount('#app')
