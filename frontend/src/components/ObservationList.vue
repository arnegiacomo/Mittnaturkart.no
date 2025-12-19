<script setup lang="ts">
import { ref, onMounted } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import { useToast } from 'primevue/usetoast'
import ConfirmDialog from 'primevue/confirmdialog'
import { useConfirm } from 'primevue/useconfirm'
import ObservationForm from './ObservationForm.vue'
import { useObservationStore } from '../stores/observations'
import type { Observation } from '../types'
import type { DataTablePageEvent } from 'primevue/datatable'

const store = useObservationStore()
const toast = useToast()
const confirm = useConfirm()

const showDialog = ref(false)
const editingObservation = ref<Observation | null>(null)
const rows = ref(10)
const first = ref(0)
const initialLoading = ref(true)

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

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString('no-NO')
}

function formatCoordinates(lat: number, lon: number) {
  return `${lat.toFixed(4)}, ${lon.toFixed(4)}`
}
</script>

<template>
  <div>
    <Toast />
    <ConfirmDialog />

    <div class="toolbar">
      <Button
        label="Ny observasjon"
        icon="pi pi-plus"
        @click="handleCreate"
        severity="success"
      />
    </div>

    <DataTable
      :value="store.observations"
      :loading="initialLoading"
      stripedRows
      lazy
      paginator
      :rows="rows"
      :totalRecords="store.totalRecords"
      :first="first"
      @page="onPage"
      tableStyle="min-width: 50rem"
      class="observation-table"
    >
      <template #empty>
        <div class="empty-state">
          <i class="pi pi-inbox" style="font-size: 3rem; color: #94a3b8;"></i>
          <p>Ingen observasjoner funnet</p>
        </div>
      </template>

      <Column field="species" header="Art" sortable />
      <Column field="category" header="Kategori" sortable />
      <Column field="date" header="Dato" sortable>
        <template #body="{ data }">
          {{ formatDate(data.date) }}
        </template>
      </Column>
      <Column header="Posisjon">
        <template #body="{ data }">
          {{ formatCoordinates(data.latitude, data.longitude) }}
        </template>
      </Column>
      <Column field="notes" header="Notater">
        <template #body="{ data }">
          {{ data.notes || '-' }}
        </template>
      </Column>
      <Column header="Handlinger">
        <template #body="{ data }">
          <div class="actions">
            <Button
              icon="pi pi-pencil"
              size="small"
              text
              @click="handleEdit(data)"
            />
            <Button
              icon="pi pi-trash"
              size="small"
              severity="danger"
              text
              @click="handleDelete(data)"
            />
          </div>
        </template>
      </Column>
    </DataTable>

    <ObservationForm
      v-model:visible="showDialog"
      :observation="editingObservation"
      @saved="loadObservations"
    />
  </div>
</template>

<style scoped>
.toolbar {
  margin-bottom: 1.5rem;
}

.observation-table {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.observation-table :deep(tbody) {
  transition: opacity 0.2s ease-in-out;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #64748b;
}

.empty-state p {
  margin-top: 1rem;
  font-size: 1.1rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
}
</style>
