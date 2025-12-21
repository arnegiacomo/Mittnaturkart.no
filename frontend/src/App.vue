<script setup lang="ts">
import { ref, watch } from 'vue'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import ObservationList from './components/ObservationList.vue'
import LocationList from './components/LocationList.vue'
import { useObservationStore } from './stores/observations'
import { useLocationStore } from './stores/locations'

const activeTab = ref(0)
const observationStore = useObservationStore()
const locationStore = useLocationStore()

// Refresh data when switching tabs
watch(activeTab, async (newTab) => {
  if (newTab === 0) {
    // Switching to Observasjoner - refresh observations
    await observationStore.fetchObservations(0, 10)
  } else if (newTab === 1) {
    // Switching to Steder - refresh locations
    await locationStore.fetchLocations(0, 10)
  }
})
</script>

<template>
  <div class="app">
    <header class="header">
      <h1>Mitt Naturkart</h1>
      <p>Spor dine naturobservasjoner</p>
    </header>
    <TabView v-model:activeIndex="activeTab" class="tabs">
      <TabPanel header="Observasjoner" :value="0">
        <div class="content">
          <ObservationList />
        </div>
      </TabPanel>
      <TabPanel header="Steder" :value="1">
        <div class="content">
          <LocationList />
        </div>
      </TabPanel>
    </TabView>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  background: #f8f9fa;
}

.header {
  background: #10b981;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
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
  border-bottom: 2px solid #e5e7eb;
}

.tabs :deep(.p-tabview-nav) {
  background: white;
  border-bottom: none;
  margin-bottom: 0;
  padding: 0 2rem;
}

.tabs :deep(.p-tabview-panels) {
  padding: 0;
  background: transparent;
}

.content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem 2rem;
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
</style>
