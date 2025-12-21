import axios from 'axios'
import type { Observation, Location, LocationWithCount, PaginatedResponse } from './types'

const api = axios.create({
  baseURL: '/api/v1'
})

export const observationApi = {
  getAll: (skip: number = 0, limit: number = 10, sortBy?: string, sortOrder?: string) =>
    api.get<PaginatedResponse<Observation>>('/observations', { params: { skip, limit, sort_by: sortBy, sort_order: sortOrder } }),
  getById: (id: number) => api.get<Observation>(`/observations/${id}`),
  create: (data: Observation) => api.post<Observation>('/observations', data),
  update: (id: number, data: Partial<Observation>) => api.put<Observation>(`/observations/${id}`, data),
  delete: (id: number) => api.delete(`/observations/${id}`)
}

export const locationApi = {
  getAll: (skip: number = 0, limit: number = 10, sortBy?: string, sortOrder?: string) =>
    api.get<PaginatedResponse<LocationWithCount>>('/locations', { params: { skip, limit, sort_by: sortBy, sort_order: sortOrder } }),
  getById: (id: number) => api.get<LocationWithCount>(`/locations/${id}`),
  create: (data: Location) => api.post<Location>('/locations', data),
  update: (id: number, data: Partial<Location>) => api.put<Location>(`/locations/${id}`, data),
  delete: (id: number) => api.delete(`/locations/${id}`)
}
