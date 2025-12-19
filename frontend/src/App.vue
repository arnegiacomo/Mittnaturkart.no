<script setup lang="ts">
import { onMounted } from 'vue'
import ObservationList from './components/ObservationList.vue'
import { useObservationStore } from './stores/observations'

const store = useObservationStore()

onMounted(() => {
  store.fetchObservations()
})
</script>

<template>
  <div class="app">
    <header class="header">
      <h1>Mitt Naturkart</h1>
      <p>Spor dine naturobservasjoner</p>
    </header>
    <main class="main">
      <ObservationList />
    </main>
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

.main {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
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
