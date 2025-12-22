<script setup lang="ts">
import Button from 'primevue/button'
import Card from 'primevue/card'
import { useAuthStore } from '../stores/auth'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()
const authStore = useAuthStore()
</script>

<template>
  <div class="account-panel">
    <Card class="account-card">
      <template #title>{{ t('account.title') }}</template>
      <template #content>
        <div class="user-info">
          <div class="info-row">
            <span class="label">{{ t('account.name') }}:</span>
            <span class="value">{{ authStore.user?.name }}</span>
          </div>
          <div class="info-row">
            <span class="label">{{ t('account.email') }}:</span>
            <span class="value">{{ authStore.user?.email }}</span>
          </div>
        </div>
        <div class="actions">
          <Button
            :label="t('auth.logout')"
            icon="pi pi-sign-out"
            severity="secondary"
            @click="authStore.logout"
          />
        </div>
      </template>
    </Card>
  </div>
</template>

<style scoped>
.account-panel {
  padding-top: 2rem;
}

.account-card {
  max-width: 500px;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.info-row {
  display: flex;
  gap: 0.5rem;
}

.label {
  font-weight: 600;
  color: #374151;
}

.value {
  color: #6b7280;
}

.actions {
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}
</style>
