import axios from 'axios'
import type { Observation } from './types'

const api = axios.create({
  baseURL: '/api/v1'
})

export const observationApi = {
  getAll: () => api.get<Observation[]>('/observations'),
  getById: (id: number) => api.get<Observation>(`/observations/${id}`),
  create: (data: Observation) => api.post<Observation>('/observations', data),
  update: (id: number, data: Partial<Observation>) => api.put<Observation>(`/observations/${id}`, data),
  delete: (id: number) => api.delete(`/observations/${id}`)
}
