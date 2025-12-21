<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import EntityTable from './EntityTable.vue'
import LocationForm from './LocationForm.vue'
import { useLocationStore } from '../stores/locations'
import { useObservationStore } from '../stores/observations'
import type { LocationWithCount } from '../types'
import type { TableColumn } from './EntityTable.vue'
import type { DataTablePageEvent, DataTableSortEvent } from 'primevue/datatable'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()
const store = useLocationStore()
const observationStore = useObservationStore()
const toast = useToast()
const confirm = useConfirm()

const showDialog = ref(false)
const editingLocation = ref<LocationWithCount | null>(null)
const rows = ref(10)
const first = ref(0)
const initialLoading = ref(true)
const sortBy = ref('id')
const sortOrder = ref('desc')

const columns: TableColumn<LocationWithCount>[] = [
  { field: 'name', header: t('locations.columns.name'), sortable: true },
  {
    field: 'address',
    header: t('locations.columns.address'),
    sortable: true,
    formatter: (data: LocationWithCount) => data.address || '-'
  },
  {
    header: t('locations.columns.coordinates'),
    formatter: (data: LocationWithCount) => {
      if (!data.latitude || !data.longitude) return '-'
      return `${data.latitude.toFixed(4)}, ${data.longitude.toFixed(4)}`
    }
  },
  {
    field: 'observation_count',
    header: t('locations.columns.observations'),
    sortable: true,
    component: (data: LocationWithCount) => h('span', { class: 'count-badge' }, data.observation_count)
  },
  {
    field: 'description',
    header: t('locations.columns.description'),
    formatter: (data: LocationWithCount) => data.description || '-'
  }
]

onMounted(async () => {
  await loadLocations()
  initialLoading.value = false
})

async function loadLocations() {
  await store.fetchLocations(first.value, rows.value, sortBy.value, sortOrder.value)
}

function onPage(event: DataTablePageEvent) {
  first.value = event.first
  rows.value = event.rows
  loadLocations()
}

function onSort(event: DataTableSortEvent) {
  sortBy.value = event.sortField as string
  sortOrder.value = event.sortOrder === 1 ? 'asc' : 'desc'
  loadLocations()
}

function handleCreate() {
  editingLocation.value = null
  showDialog.value = true
}

function handleEdit(location: LocationWithCount) {
  editingLocation.value = { ...location }
  showDialog.value = true
}

function handleDelete(location: LocationWithCount) {
  confirm.require({
    message: t('locations.delete_confirm', { name: location.name }),
    header: t('locations.delete_header'),
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: t('confirmDialog.accept'),
    rejectLabel: t('confirmDialog.reject'),
    accept: async () => {
      try {
        await store.deleteLocation(location.id!)
        await loadLocations()
        // Refresh observations to clear deleted location references
        await observationStore.fetchObservations(0, 10)
        toast.add({
          severity: 'success',
          summary: t('toast.success'),
          detail: t('locations.messages.deleted'),
          life: 3000
        })
      } catch {
        toast.add({
          severity: 'error',
          summary: t('toast.error'),
          detail: t('locations.messages.error_delete'),
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
      :data="store.locations"
      :columns="columns"
      :loading="initialLoading"
      :total-records="store.totalRecords"
      :rows="rows"
      :first="first"
      :create-button-label="t('locations.new')"
      empty-icon="pi pi-map-marker"
      :empty-message="t('locations.none_found')"
      @create="handleCreate"
      @edit="handleEdit"
      @delete="handleDelete"
      @page="onPage"
      @sort="onSort"
    />

    <LocationForm
      v-model:visible="showDialog"
      :location="editingLocation"
      @saved="loadLocations"
    />
  </div>
</template>

<style scoped>
.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 2rem;
  padding: 0.25rem 0.5rem;
  background: #e0f2fe;
  color: #0369a1;
  border-radius: 1rem;
  font-weight: 600;
  font-size: 0.875rem;
}
</style>
