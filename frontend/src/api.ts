import axios from 'axios'
import type { Observation, PaginatedResponse } from './types'

const api = axios.create({
  baseURL: '/api/v1'
})

export const observationApi = {
  getAll: (skip: number = 0, limit: number = 10) =>
    api.get<PaginatedResponse<Observation>>('/observations', { params: { skip, limit } }),
  getById: (id: number) => api.get<Observation>(`/observations/${id}`),
  create: (data: Observation) => api.post<Observation>('/observations', data),
  update: (id: number, data: Partial<Observation>) => api.put<Observation>(`/observations/${id}`, data),
  delete: (id: number) => api.delete(`/observations/${id}`)
}
