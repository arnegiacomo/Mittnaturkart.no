import { defineStore } from 'pinia'
import { ref } from 'vue'
import { observationApi } from '../api'
import type { Observation } from '../types'

export const useObservationStore = defineStore('observations', () => {
  const observations = ref<Observation[]>([])
  const totalRecords = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchObservations(skip: number = 0, limit: number = 10, sortBy?: string, sortOrder?: string) {
    error.value = null
    try {
      const response = await observationApi.getAll(skip, limit, sortBy, sortOrder)
      observations.value = response.data.data
      totalRecords.value = response.data.total
    } catch (e) {
      error.value = 'Kunne ikke laste observasjoner'
      console.error(e)
    }
  }

  async function createObservation(observation: Observation) {
    loading.value = true
    error.value = null
    try {
      const response = await observationApi.create(observation)
      observations.value.push(response.data)
    } catch (e) {
      error.value = 'Kunne ikke opprette observasjon'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateObservation(id: number, data: Partial<Observation>) {
    loading.value = true
    error.value = null
    try {
      const response = await observationApi.update(id, data)
      const index = observations.value.findIndex(o => o.id === id)
      if (index !== -1) {
        observations.value[index] = response.data
      }
    } catch (e) {
      error.value = 'Kunne ikke oppdatere observasjon'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteObservation(id: number) {
    loading.value = true
    error.value = null
    try {
      await observationApi.delete(id)
      observations.value = observations.value.filter(o => o.id !== id)
    } catch (e) {
      error.value = 'Kunne ikke slette observasjon'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    observations,
    totalRecords,
    loading,
    error,
    fetchObservations,
    createObservation,
    updateObservation,
    deleteObservation
  }
})
