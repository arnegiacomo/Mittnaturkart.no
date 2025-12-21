<script setup lang="ts">
import { ref, watch, onMounted, nextTick } from 'vue'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Button from 'primevue/button'
import Select from 'primevue/select'
import DatePicker from 'primevue/datepicker'
import { useToast } from 'primevue/usetoast'
import { useObservationStore } from '../stores/observations'
import { useLocationStore } from '../stores/locations'
import type { Observation } from '../types'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()

const props = defineProps<{
  visible: boolean
  observation: Observation | null
}>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
  'saved': []
}>()

const store = useObservationStore()
const locationStore = useLocationStore()
const toast = useToast()

const categories = [
  { label: t('observations.categories.bird'), value: 'Fugl' },
  { label: t('observations.categories.mammal'), value: 'Pattedyr' },
  { label: t('observations.categories.insect'), value: 'Insekt' },
  { label: t('observations.categories.plant'), value: 'Plante' },
  { label: t('observations.categories.fish'), value: 'Fisk' },
  { label: t('observations.categories.other'), value: 'Annet' }
]

onMounted(async () => {
  // Load all locations for the dropdown
  await locationStore.fetchLocations(0, 100)
})

const formData = ref<Observation>({
  species: '',
  date: new Date().toISOString(),
  location_id: null,
  notes: '',
  category: 'Fugl'
})

const selectedDate = ref<Date>(new Date())
const selectedTime = ref<Date>(new Date())
const formModified = ref<boolean>(false)

watch(() => props.observation, async (newVal) => {
  if (newVal) {
    formData.value = { ...newVal }
    const date = new Date(newVal.date)
    selectedDate.value = date
    selectedTime.value = date
    await nextTick()
    formModified.value = false
  } else {
    resetForm()
  }
}, { immediate: true })

watch([formData, selectedDate, selectedTime], () => {
  formModified.value = true
}, { deep: true })

async function resetForm() {
  const now = new Date()
  formData.value = {
    species: '',
    date: now.toISOString(),
    location_id: null,
    notes: '',
    category: 'Fugl'
  }
  selectedDate.value = now
  selectedTime.value = now
  await nextTick()
  formModified.value = false
}

async function handleSubmit() {
  try {
    const combinedDateTime = new Date(
      selectedDate.value.getFullYear(),
      selectedDate.value.getMonth(),
      selectedDate.value.getDate(),
      selectedTime.value.getHours(),
      selectedTime.value.getMinutes(),
      0,
      0
    )

    const submitData = {
      ...formData.value,
      date: combinedDateTime.toISOString()
    }

    if (props.observation?.id) {
      await store.updateObservation(props.observation.id, submitData)
      toast.add({
        severity: 'success',
        summary: t('toast.success'),
        detail: t('observations.messages.updated'),
        life: 3000
      })
    } else {
      await store.createObservation(submitData)
      toast.add({
        severity: 'success',
        summary: t('toast.success'),
        detail: t('observations.messages.created'),
        life: 3000
      })
    }
    // Refresh locations to update observation counts
    await locationStore.fetchLocations(0, 100)
    emit('saved')
    emit('update:visible', false)
    resetForm()
  } catch {
    toast.add({
      severity: 'error',
      summary: t('toast.error'),
      detail: t('observations.messages.error_create'),
      life: 3000
    })
  }
}

function handleCancel() {
  emit('update:visible', false)
  resetForm()
}

function handleClose() {
  if (formModified.value) {
    const confirmed = window.confirm(t('common.unsaved_changes_warning'))
    if (!confirmed) {
      return
    }
  }
  emit('update:visible', false)
  resetForm()
}
</script>

<template>
  <Dialog
    :visible="visible"
    @update:visible="(val) => !val && handleClose()"
    :header="observation ? t('observations.edit') : t('observations.new')"
    :style="{ width: '500px' }"
    modal
    dismissableMask
  >
    <form @submit.prevent="handleSubmit" class="form">
      <div class="field">
        <label for="species">{{ t('observations.fields.species') }} *</label>
        <InputText
          id="species"
          v-model="formData.species"
          required
          class="w-full"
        />
      </div>

      <div class="field">
        <label for="category">{{ t('observations.fields.category') }} *</label>
        <Select
          id="category"
          v-model="formData.category"
          :options="categories"
          optionLabel="label"
          optionValue="value"
          required
          class="w-full"
        />
      </div>

      <div class="field">
        <label for="date">{{ t('observations.fields.date') }} *</label>
        <DatePicker
          id="date"
          v-model="selectedDate"
          dateFormat="yy-mm-dd"
          required
          class="w-full"
        />
      </div>

      <div class="field">
        <label for="time">{{ t('observations.fields.time') }} *</label>
        <DatePicker
          id="time"
          v-model="selectedTime"
          timeOnly
          hourFormat="24"
          required
          class="w-full"
        />
      </div>

      <div class="field">
        <label for="location">{{ t('observations.fields.location') }} ({{ t('common.optional') }})</label>
        <Select
          id="location"
          v-model="formData.location_id"
          :options="locationStore.locations"
          optionLabel="name"
          optionValue="id"
          :placeholder="t('observations.placeholders.select_location')"
          showClear
          class="w-full"
        />
      </div>

      <div class="field">
        <label for="notes">{{ t('observations.fields.notes') }}</label>
        <Textarea
          id="notes"
          v-model="formData.notes"
          rows="3"
          class="w-full"
        />
      </div>

      <div class="form-actions">
        <Button
          :label="t('common.cancel')"
          severity="secondary"
          text
          @click="handleCancel"
          type="button"
        />
        <Button
          :label="t('common.save')"
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
