import axios from 'axios'
import type { Observation, Location, LocationWithCount, PaginatedResponse, User, AuthToken } from './types'

const TOKEN_KEY = 'auth_token'
const TOKEN_EXPIRY_KEY = 'auth_token_expiry'

const api = axios.create({
  baseURL: '/api/v1'
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY)
  const expiry = localStorage.getItem(TOKEN_EXPIRY_KEY)

  if (token && expiry && Date.now() < Number(expiry)) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(TOKEN_EXPIRY_KEY)

      // Reload page to trigger auth check, which will redirect to login
      if (window.location.pathname !== '/auth/callback') {
        window.location.href = '/'
      }
    }
    return Promise.reject(error)
  }
)

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

export const authApi = {
  getLoginUrl: async () => {
    const response = await api.get<{ url: string }>('/auth/login-url')
    return response.data.url
  },
  callback: (code: string) => api.post<AuthToken>('/auth/callback', null, { params: { code } }),
  getLogoutUrl: async () => {
    const response = await api.get<{ url: string }>('/auth/logout-url')
    return response.data.url
  },
  getCurrentUser: () => api.get<User>('/auth/me')
}
