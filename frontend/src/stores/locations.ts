import { defineStore } from 'pinia'
import { ref } from 'vue'
import { locationApi } from '../api'
import type { Location, LocationWithCount } from '../types'

export const useLocationStore = defineStore('locations', () => {
  const locations = ref<LocationWithCount[]>([])
  const totalRecords = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchLocations(skip: number = 0, limit: number = 10, sortBy?: string, sortOrder?: string) {
    error.value = null
    try {
      const response = await locationApi.getAll(skip, limit, sortBy, sortOrder)
      locations.value = response.data.data
      totalRecords.value = response.data.total
    } catch (e) {
      error.value = 'Kunne ikke laste steder'
      console.error(e)
    }
  }

  async function createLocation(location: Location) {
    loading.value = true
    error.value = null
    try {
      const response = await locationApi.create(location)
      // Refetch to get updated observation count
      await fetchLocations()
      return response.data
    } catch (e) {
      error.value = 'Kunne ikke opprette sted'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateLocation(id: number, data: Partial<Location>) {
    loading.value = true
    error.value = null
    try {
      const response = await locationApi.update(id, data)
      const index = locations.value.findIndex(l => l.id === id)
      if (index !== -1) {
        // Keep observation_count from existing
        locations.value[index] = { ...response.data, observation_count: locations.value[index].observation_count }
      }
    } catch (e) {
      error.value = 'Kunne ikke oppdatere sted'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteLocation(id: number) {
    loading.value = true
    error.value = null
    try {
      await locationApi.delete(id)
      locations.value = locations.value.filter(l => l.id !== id)
    } catch (e) {
      error.value = 'Kunne ikke slette sted'
      console.error(e)
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    locations,
    totalRecords,
    loading,
    error,
    fetchLocations,
    createLocation,
    updateLocation,
    deleteLocation
  }
})
