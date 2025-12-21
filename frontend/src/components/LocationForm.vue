<script setup lang="ts">
import { ref, watch } from 'vue'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Textarea from 'primevue/textarea'
import Button from 'primevue/button'
import { useToast } from 'primevue/usetoast'
import { useLocationStore } from '../stores/locations'
import type { Location, LocationWithCount } from '../types'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()

const props = defineProps<{
  visible: boolean
  location: LocationWithCount | null
}>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
  'saved': []
}>()

const store = useLocationStore()
const toast = useToast()

const formData = ref<Location>({
  name: '',
  latitude: null,
  longitude: null,
  description: '',
  address: ''
})

watch(() => props.location, (newVal) => {
  if (newVal) {
    formData.value = {
      name: newVal.name,
      latitude: newVal.latitude,
      longitude: newVal.longitude,
      description: newVal.description,
      address: newVal.address
    }
  } else {
    resetForm()
  }
}, { immediate: true })

function resetForm() {
  formData.value = {
    name: '',
    latitude: null,
    longitude: null,
    description: '',
    address: ''
  }
}

async function handleSubmit() {
  try {
    if (props.location?.id) {
      await store.updateLocation(props.location.id, formData.value)
      toast.add({
        severity: 'success',
        summary: t('toast.success'),
        detail: t('locations.messages.updated'),
        life: 3000
      })
    } else {
      await store.createLocation(formData.value)
      toast.add({
        severity: 'success',
        summary: t('toast.success'),
        detail: t('locations.messages.created'),
        life: 3000
      })
    }
    emit('saved')
    emit('update:visible', false)
    resetForm()
  } catch {
    toast.add({
      severity: 'error',
      summary: t('toast.error'),
      detail: t('locations.messages.error_create'),
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
    :header="location ? t('locations.edit') : t('locations.new')"
    :style="{ width: '500px' }"
    modal
  >
    <form @submit.prevent="handleSubmit" class="form">
      <div class="field">
        <label for="name">{{ t('locations.fields.name') }} *</label>
        <InputText
          id="name"
          v-model="formData.name"
          required
          class="w-full"
        />
      </div>

      <div class="field">
        <label for="address">{{ t('locations.fields.address') }}</label>
        <InputText
          id="address"
          v-model="formData.address"
          class="w-full"
        />
      </div>

      <div class="field-group">
        <div class="field">
          <label for="latitude">{{ t('locations.fields.latitude') }}</label>
          <InputNumber
            id="latitude"
            v-model="formData.latitude"
            :minFractionDigits="4"
            :maxFractionDigits="6"
            class="w-full"
          />
        </div>

        <div class="field">
          <label for="longitude">{{ t('locations.fields.longitude') }}</label>
          <InputNumber
            id="longitude"
            v-model="formData.longitude"
            :minFractionDigits="4"
            :maxFractionDigits="6"
            class="w-full"
          />
        </div>
      </div>

      <div class="field">
        <label for="description">{{ t('locations.fields.description') }}</label>
        <Textarea
          id="description"
          v-model="formData.description"
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

.field-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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
