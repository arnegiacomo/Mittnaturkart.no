<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import EntityTable from './EntityTable.vue'
import ObservationForm from './ObservationForm.vue'
import { useObservationStore } from '../stores/observations'
import { useLocationStore } from '../stores/locations'
import type { Observation } from '../types'
import type { TableColumn } from './EntityTable.vue'
import type { DataTablePageEvent } from 'primevue/datatable'

const store = useObservationStore()
const locationStore = useLocationStore()
const toast = useToast()
const confirm = useConfirm()

const showDialog = ref(false)
const editingObservation = ref<Observation | null>(null)
const rows = ref(10)
const first = ref(0)
const initialLoading = ref(true)

const columns: TableColumn<Observation>[] = [
  { field: 'species', header: 'Art', sortable: true },
  { field: 'category', header: 'Kategori', sortable: true },
  {
    field: 'date',
    header: 'Dato',
    sortable: true,
    formatter: (data: Observation) => new Date(data.date).toLocaleDateString('no-NO')
  },
  {
    field: 'notes',
    header: 'Notater',
    formatter: (data: Observation) => data.notes || '-'
  }
]

onMounted(async () => {
  await loadObservations()
  initialLoading.value = false
})

async function loadObservations() {
  await store.fetchObservations(first.value, rows.value)
}

function onPage(event: DataTablePageEvent) {
  first.value = event.first
  rows.value = event.rows
  loadObservations()
}

function handleCreate() {
  editingObservation.value = null
  showDialog.value = true
}

function handleEdit(observation: Observation) {
  editingObservation.value = { ...observation }
  showDialog.value = true
}

function handleDelete(observation: Observation) {
  confirm.require({
    message: `Er du sikker på at du vil slette observasjonen av ${observation.species}?`,
    header: 'Bekreft sletting',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Ja',
    rejectLabel: 'Nei',
    accept: async () => {
      try {
        await store.deleteObservation(observation.id!)
        await loadObservations()
        // Refresh locations to update observation counts
        await locationStore.fetchLocations(0, 100)
        toast.add({
          severity: 'success',
          summary: 'Slettet',
          detail: 'Observasjonen ble slettet',
          life: 3000
        })
      } catch {
        toast.add({
          severity: 'error',
          summary: 'Feil',
          detail: 'Kunne ikke slette observasjonen',
          life: 3000
        })
      }
    }
  })
}
</script>

<template>
  <div>
    <EntityTable
      :data="store.observations"
      :columns="columns"
      :loading="initialLoading"
      :total-records="store.totalRecords"
      :rows="rows"
      :first="first"
      create-button-label="Ny observasjon"
      empty-message="Ingen observasjoner funnet"
      @create="handleCreate"
      @edit="handleEdit"
      @delete="handleDelete"
      @page="onPage"
    />

    <ObservationForm
      v-model:visible="showDialog"
      :observation="editingObservation"
      @saved="loadObservations"
    />
  </div>
</template>
