<script setup>
import { RouterView } from 'vue-router'
import Header from './components/Header.vue'
import { useErrorStore } from './stores/error'

const errorStore = useErrorStore()
</script>

<template>
  <Header />
  
  <!-- Global Error Banner -->
  <div v-if="errorStore.activeError" class="global-error-banner" role="alert">
    <div class="banner-content">
      <span class="warning-icon">⚠</span>
      <span class="error-msg"><strong>Application Alert:</strong> {{ errorStore.activeError }}</span>
    </div>
    <button @click="errorStore.clearError" class="close-banner-btn" aria-label="Dismiss error">✕</button>
  </div>

  <main>
    <RouterView v-slot="{ Component }">
      <transition name="view" mode="out-in">
        <component :is="Component" />
      </transition>
    </RouterView>
  </main>
</template>

<style scoped>
.global-error-banner {
  background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
  color: #ffffff;
  padding: 12px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
  position: relative;
  z-index: 99;
  animation: slide-down 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.warning-icon {
  font-size: 1.25rem;
}

.error-msg {
  font-size: 0.95rem;
}

.close-banner-btn {
  background: transparent;
  border: none;
  color: #ffffff;
  font-size: 1.1rem;
  cursor: pointer;
  opacity: 0.8;
  transition: opacity 0.2s;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}

.close-banner-btn:hover {
  opacity: 1;
}

@keyframes slide-down {
  from {
    transform: translateY(-100%);
  }
  to {
    transform: translateY(0);
  }
}
</style>
