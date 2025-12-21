<script setup lang="ts">
import { ref } from 'vue'
import Button from 'primevue/button'
import Menu from 'primevue/menu'
import type { MenuItem } from 'primevue/menuitem'
import { useAuthStore } from '../stores/auth'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()
const authStore = useAuthStore()
const menu = ref()

const menuItems: MenuItem[] = [
  {
    label: t('auth.logout'),
    icon: 'pi pi-sign-out',
    command: () => authStore.logout()
  }
]

function toggleMenu(event: Event) {
  menu.value.toggle(event)
}
</script>

<template>
  <div class="user-menu">
    <Button
      v-if="!authStore.isAuthenticated"
      :label="t('auth.login')"
      icon="pi pi-sign-in"
      @click="authStore.login"
      outlined
    />
    <div v-else class="user-info">
      <Button
        :label="authStore.user?.name || authStore.user?.email"
        icon="pi pi-user"
        @click="toggleMenu"
        text
      />
      <Menu ref="menu" :model="menuItems" popup />
    </div>
  </div>
</template>

<style scoped>
.user-menu {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-menu :deep(.p-button) {
  color: white;
  border-color: rgba(255, 255, 255, 0.5);
}

.user-menu :deep(.p-button:hover) {
  background: rgba(255, 255, 255, 0.1);
  border-color: white;
}

.user-menu :deep(.p-button-text) {
  color: white;
}

.user-menu :deep(.p-button-text:hover) {
  background: rgba(255, 255, 255, 0.1);
}
</style>
