<script lang="ts" generic="T">
export interface TableColumn<T> {
  field?: keyof T | string
  header: string
  sortable?: boolean
  formatter?: (data: T) => string | number
  component?: (data: T) => any
}
</script>

<script setup lang="ts" generic="T">
import { ref } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Menu from 'primevue/menu'
import type { DataTablePageEvent, DataTableSortEvent } from 'primevue/datatable'
import type { MenuItem } from 'primevue/menuitem'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()
const menu = ref()
const selectedItem = ref<T | null>(null)

interface Props {
  data: T[]
  columns: TableColumn<T>[]
  loading?: boolean
  totalRecords: number
  rows?: number
  first?: number
  createButtonLabel: string
  createButtonIcon?: string
  emptyIcon?: string
  emptyMessage: string
  showActions?: boolean
}

withDefaults(defineProps<Props>(), {
  loading: false,
  rows: 10,
  first: 0,
  createButtonIcon: 'pi pi-plus',
  emptyIcon: 'pi pi-inbox',
  showActions: true
})

const emit = defineEmits<{
  create: []
  edit: [item: T]
  delete: [item: T]
  page: [event: DataTablePageEvent]
  sort: [event: DataTableSortEvent]
}>()

const menuItems = ref<MenuItem[]>([
  {
    label: t('common.edit'),
    icon: 'pi pi-pencil',
    command: () => {
      if (selectedItem.value) {
        emit('edit', selectedItem.value)
      }
    }
  },
  {
    label: t('common.delete'),
    icon: 'pi pi-trash',
    command: () => {
      if (selectedItem.value) {
        emit('delete', selectedItem.value)
      }
    }
  }
])

const toggleMenu = (event: Event, item: T) => {
  event.stopPropagation()
  selectedItem.value = item
  menu.value.toggle(event)
}

const onRowClick = (event: any) => {
  emit('edit', event.data)
}
</script>

<template>
  <div>
    <div class="toolbar">
      <Button
        :label="createButtonLabel"
        :icon="createButtonIcon"
        @click="emit('create')"
        severity="success"
      />
    </div>

    <DataTable
      :value="data"
      :loading="loading"
      lazy
      paginator
      :rows="rows"
      :totalRecords="totalRecords"
      :first="first"
      @page="emit('page', $event)"
      @sort="emit('sort', $event)"
      @row-click="onRowClick"
      tableStyle="min-width: 50rem"
      class="entity-table"
    >
      <template #empty>
        <div class="empty-state">
          <i :class="emptyIcon" style="font-size: 3rem; color: #94a3b8;"></i>
          <p>{{ emptyMessage }}</p>
        </div>
      </template>

      <Column
        v-for="column in columns"
        :key="String(column.field || column.header)"
        :field="String(column.field)"
        :header="column.header"
        :sortable="column.sortable"
      >
        <template v-if="column.formatter || column.component" #body="{ data }">
          <component v-if="column.component" :is="column.component(data)" />
          <template v-else-if="column.formatter">
            {{ column.formatter(data) }}
          </template>
        </template>
      </Column>

      <Column v-if="showActions" :style="{ width: '4rem' }">
        <template #body="{ data }">
          <Button
            icon="pi pi-ellipsis-v"
            text
            rounded
            @click="(event) => toggleMenu(event, data)"
            aria-label="Meny"
          />
        </template>
      </Column>
    </DataTable>

    <Menu ref="menu" :model="menuItems" popup />
  </div>
</template>

<style scoped>
.toolbar {
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}

.entity-table {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.entity-table :deep(tbody) {
  transition: opacity 0.2s ease-in-out;
}

.entity-table :deep(tbody tr) {
  cursor: pointer;
}

.entity-table :deep(tbody tr:hover) {
  background-color: #f8fafc;
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
</style>
