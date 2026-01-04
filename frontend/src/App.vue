<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import TabPanels from 'primevue/tabpanels'
import TabPanel from 'primevue/tabpanel'
import ConfirmDialog from 'primevue/confirmdialog'
import Toast from 'primevue/toast'
import ObservationList from './components/ObservationList.vue'
import LocationList from './components/LocationList.vue'
import AccountPanel from './components/AccountPanel.vue'
import AuthCallback from './components/AuthCallback.vue'
import { useObservationStore } from './stores/observations'
import { useLocationStore } from './stores/locations'
import { useAuthStore } from './stores/auth'
import { useI18n } from './composables/useI18n'

const { t } = useI18n()
const activeTab = ref('0')
const observationStore = useObservationStore()
const locationStore = useLocationStore()
const authStore = useAuthStore()

const isAuthCallback = computed(() => window.location.pathname === '/auth/callback')
const isInitializing = ref(true)

onMounted(async () => {
  await authStore.initialize()

  if (!authStore.isAuthenticated && !isAuthCallback.value) {
    await authStore.login()
    return
  }

  isInitializing.value = false
})

// Refresh data when switching tabs
watch(activeTab, async (newTab) => {
  if (newTab === '0') {
    // Switching to Observasjoner - refresh observations
    await observationStore.fetchObservations(0, 10)
  } else if (newTab === '1') {
    // Switching to Steder - refresh locations
    await locationStore.fetchLocations(0, 10)
  }
})
</script>

<template>
  <div class="app">
    <Toast position="bottom-right" />
    <ConfirmDialog />
    <AuthCallback v-if="isAuthCallback" />
    <div v-else-if="isInitializing" class="loading">
      <div class="spinner"></div>
    </div>
    <template v-else>
      <header class="header">
        <div class="header-content">
          <h1>{{ t('app.title') }}</h1>
          <p>{{ t('app.subtitle') }}</p>
        </div>
      </header>
      <Tabs v-model:value="activeTab" class="tabs">
        <TabList>
          <Tab value="0">{{ t('navigation.observations') }}</Tab>
          <Tab value="1">{{ t('navigation.locations') }}</Tab>
          <Tab value="2">{{ t('navigation.account') }}</Tab>
        </TabList>
        <TabPanels>
          <TabPanel value="0">
            <div class="content">
              <ObservationList />
            </div>
          </TabPanel>
          <TabPanel value="1">
            <div class="content">
              <LocationList />
            </div>
          </TabPanel>
          <TabPanel value="2">
            <div class="content">
              <AccountPanel />
            </div>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </template>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  background: #f8f9fa;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.header {
  background: #10b981;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  text-align: center;
}

.header h1 {
  margin: 0;
  color: white;
  font-size: 2rem;
  font-weight: 600;
}

.header p {
  margin: 0.5rem 0 0;
  color: rgba(255,255,255,0.9);
}

.tabs {
  background: white;
}

.tabs :deep(.p-tablist) {
  background: white;
  border-bottom: 2px solid #e5e7eb;
  padding: 0 2rem;
  display: flex;
  gap: 0;
}

.tabs :deep(.p-tab) {
  padding: 1rem 1.5rem;
  border: none;
  border-bottom: 2px solid transparent;
  background: transparent;
  color: #6b7280;
  font-weight: 500;
  transition: all 0.2s;
  cursor: pointer;
  margin-bottom: -2px;
}

.tabs :deep(.p-tab:hover) {
  color: #10b981;
  background: #f0fdf4;
}

.tabs :deep(.p-tab[data-p-active="true"]) {
  color: #10b981;
  border-bottom-color: #10b981;
  background: transparent;
}

.tabs :deep(.p-tabpanels) {
  padding: 0;
  background: transparent;
}

.content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem 2rem;
}

@media (max-width: 640px) {
  .header {
    padding: 1rem;
  }

  .header h1 {
    font-size: 1.5rem;
  }

  .tabs :deep(.p-tablist) {
    padding: 0;
  }

  .tabs :deep(.p-tab) {
    flex: 1;
    justify-content: center;
    padding: 0.75rem 0.5rem;
  }

  .content {
    padding: 0 0.75rem 1rem;
  }
}
</style>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: #f8f9fa;
}

@media (max-width: 640px) {
  .p-toast {
    width: calc(100% - 1rem) !important;
    max-width: none !important;
    left: 50% !important;
    right: auto !important;
    transform: translateX(-50%) !important;
  }

  .p-toast-message {
    margin: 0 0 0.5rem 0 !important;
  }

  .p-toast-message-content {
    padding: 0.75rem !important;
  }

  .p-toast-message-text {
    margin: 0 0 0 0.75rem !important;
  }

  .p-toast-summary {
    font-size: 0.9rem !important;
  }

  .p-toast-detail {
    font-size: 0.85rem !important;
    word-break: break-word !important;
  }
}
</style>
