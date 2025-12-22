<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()
const authStore = useAuthStore()
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  const urlParams = new URLSearchParams(window.location.search)
  const code = urlParams.get('code')

  if (!code) {
    error.value = t('auth.messages.no_code')
    loading.value = false
    return
  }

  try {
    await authStore.handleCallback(code)
    window.location.href = '/'
  } catch (e) {
    console.error('Auth callback error:', e)
    error.value = t('auth.messages.callback_error')
    loading.value = false
  }
})
</script>

<template>
  <div class="auth-callback">
    <div v-if="loading" class="loading">
      <i class="pi pi-spinner pi-spin" style="font-size: 2rem"></i>
      <p>{{ t('auth.messages.logging_in') }}</p>
    </div>
    <div v-else-if="error" class="error">
      <i class="pi pi-times-circle" style="font-size: 2rem; color: #ef4444"></i>
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<style scoped>
.auth-callback {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #f8f9fa;
}

.loading,
.error {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.loading p,
.error p {
  margin: 0;
  color: #6b7280;
  font-size: 1rem;
}
</style>
