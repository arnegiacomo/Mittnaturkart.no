<script setup lang="ts" generic="T">
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import type { DataTablePageEvent, DataTableSortEvent } from 'primevue/datatable'

export interface TableColumn<T> {
  field?: keyof T | string
  header: string
  sortable?: boolean
  formatter?: (data: T) => string | number
  component?: (data: T) => any
}

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
      stripedRows
      lazy
      paginator
      :rows="rows"
      :totalRecords="totalRecords"
      :first="first"
      @page="emit('page', $event)"
      @sort="emit('sort', $event)"
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

      <Column v-if="showActions" header="Handlinger">
        <template #body="{ data }">
          <div class="actions">
            <Button
              icon="pi pi-pencil"
              size="small"
              text
              @click="emit('edit', data)"
            />
            <Button
              icon="pi pi-trash"
              size="small"
              severity="danger"
              text
              @click="emit('delete', data)"
            />
          </div>
        </template>
      </Column>
    </DataTable>
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
