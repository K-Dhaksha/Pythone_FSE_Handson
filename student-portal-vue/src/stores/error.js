import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useErrorStore = defineStore('error', () => {
  const activeError = ref(null)

  function setError(errorMsg) {
    activeError.value = errorMsg
    console.log(`[Global Error Store] Error registered: ${errorMsg}`)
  }

  function clearError() {
    activeError.value = null
    console.log('[Global Error Store] Error cleared.')
  }

  return {
    activeError,
    setError,
    clearError
  }
})
