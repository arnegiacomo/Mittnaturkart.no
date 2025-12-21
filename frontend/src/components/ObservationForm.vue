<script setup lang="ts">
import { ref, watch } from 'vue'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Button from 'primevue/button'
import Select from 'primevue/select'
import DatePicker from 'primevue/datepicker'
import { useToast } from 'primevue/usetoast'
import { useObservationStore } from '../stores/observations'
import type { Observation } from '../types'

const props = defineProps<{
  visible: boolean
  observation: Observation | null
}>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
  'saved': []
}>()

const store = useObservationStore()
const toast = useToast()

const categories = [
  'Fugl',
  'Pattedyr',
  'Insekt',
  'Plante',
  'Fisk',
  'Annet'
]

const formData = ref<Observation>({
  species: '',
  date: new Date().toISOString().split('T')[0],
  location_id: null,
  notes: '',
  category: 'Fugl'
})

const selectedDate = ref<Date>(new Date())

watch(() => props.observation, (newVal) => {
  if (newVal) {
    formData.value = { ...newVal }
    selectedDate.value = new Date(newVal.date)
  } else {
    resetForm()
  }
}, { immediate: true })

function resetForm() {
  formData.value = {
    species: '',
    date: new Date().toISOString().split('T')[0],
    location_id: null,
    notes: '',
    category: 'Fugl'
  }
  selectedDate.value = new Date()
}

async function handleSubmit() {
  try {
    const submitData = {
      ...formData.value,
      date: selectedDate.value.toISOString().split('T')[0]
    }

    if (props.observation?.id) {
      await store.updateObservation(props.observation.id, submitData)
      toast.add({
        severity: 'success',
        summary: 'Oppdatert',
        detail: 'Observasjonen ble oppdatert',
        life: 3000
      })
    } else {
      await store.createObservation(submitData)
      toast.add({
        severity: 'success',
        summary: 'Opprettet',
        detail: 'Observasjonen ble opprettet',
        life: 3000
      })
    }
    emit('saved')
    emit('update:visible', false)
    resetForm()
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Feil',
      detail: 'Kunne ikke lagre observasjonen',
      life: 3000
    })
  }
}

function handleCancel() {
  emit('update:visible', false)
  resetForm()
}
</script>

<template>
  <Dialog
    :visible="visible"
    @update:visible="emit('update:visible', $event)"
    :header="observation ? 'Rediger observasjon' : 'Ny observasjon'"
    :style="{ width: '500px' }"
    modal
  >
    <form @submit.prevent="handleSubmit" class="form">
      <div class="field">
        <label for="species">Art *</label>
        <InputText
          id="species"
          v-model="formData.species"
          required
          class="w-full"
        />
      </div>

      <div class="field">
        <label for="category">Kategori *</label>
        <Select
          id="category"
          v-model="formData.category"
          :options="categories"
          required
          class="w-full"
        />
      </div>

      <div class="field">
        <label for="date">Dato *</label>
        <DatePicker
          id="date"
          v-model="selectedDate"
          dateFormat="yy-mm-dd"
          required
          class="w-full"
        />
      </div>

      <div class="field">
        <label for="notes">Notater</label>
        <Textarea
          id="notes"
          v-model="formData.notes"
          rows="3"
          class="w-full"
        />
      </div>

      <div class="form-actions">
        <Button
          label="Avbryt"
          severity="secondary"
          text
          @click="handleCancel"
          type="button"
        />
        <Button
          label="Lagre"
          type="submit"
          :loading="store.loading"
        />
      </div>
    </form>
  </Dialog>
</template>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.field label {
  font-weight: 500;
  color: #374151;
}

.w-full {
  width: 100%;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 0.5rem;
}
</style>
