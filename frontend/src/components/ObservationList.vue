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
import type { DataTablePageEvent, DataTableSortEvent } from 'primevue/datatable'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()
const store = useObservationStore()
const locationStore = useLocationStore()
const toast = useToast()
const confirm = useConfirm()

const showDialog = ref(false)
const editingObservation = ref<Observation | null>(null)
const rows = ref(10)
const first = ref(0)
const initialLoading = ref(true)
const sortBy = ref('id')
const sortOrder = ref('desc')

const columns: TableColumn<Observation>[] = [
  { field: 'species', header: t('observations.columns.species'), sortable: true },
  { field: 'category', header: t('observations.columns.category'), sortable: true },
  {
    field: 'date',
    header: t('observations.columns.date_time'),
    sortable: true,
    formatter: (data: Observation) => {
      const date = new Date(data.date)
      return `${date.toLocaleDateString('nb-NO')} ${date.toLocaleTimeString('nb-NO', { hour: '2-digit', minute: '2-digit' })}`
    }
  },
  {
    field: 'notes',
    header: t('observations.columns.notes'),
    formatter: (data: Observation) => data.notes || '-'
  }
]

onMounted(async () => {
  await loadObservations()
  initialLoading.value = false
})

async function loadObservations() {
  await store.fetchObservations(first.value, rows.value, sortBy.value, sortOrder.value)
}

function onPage(event: DataTablePageEvent) {
  first.value = event.first
  rows.value = event.rows
  loadObservations()
}

function onSort(event: DataTableSortEvent) {
  sortBy.value = event.sortField as string
  sortOrder.value = event.sortOrder === 1 ? 'asc' : 'desc'
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
    message: t('observations.delete_confirm', { species: observation.species }),
    header: t('observations.delete_header'),
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: t('confirmDialog.accept'),
    rejectLabel: t('confirmDialog.reject'),
    accept: async () => {
      try {
        await store.deleteObservation(observation.id!)
        await loadObservations()
        // Refresh locations to update observation counts
        await locationStore.fetchLocations(0, 100)
        toast.add({
          severity: 'success',
          summary: t('toast.success'),
          detail: t('observations.messages.deleted'),
          life: 3000
        })
      } catch {
        toast.add({
          severity: 'error',
          summary: t('toast.error'),
          detail: t('observations.messages.error_delete'),
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
      :create-button-label="t('observations.new')"
      :empty-message="t('observations.none_found')"
      @create="handleCreate"
      @edit="handleEdit"
      @delete="handleDelete"
      @page="onPage"
      @sort="onSort"
    />

    <ObservationForm
      v-model:visible="showDialog"
      :observation="editingObservation"
      @saved="loadObservations"
    />
  </div>
</template>
