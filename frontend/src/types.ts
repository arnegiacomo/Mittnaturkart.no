export interface Observation {
  id?: number
  species: string
  date: string
  location_id?: number | null
  notes?: string
  category: string
  created_at?: string
  updated_at?: string
}

export interface Location {
  id?: number
  name: string
  latitude?: number | null
  longitude?: number | null
  description?: string | null
  address?: string | null
  created_at?: string
  updated_at?: string
}

export interface LocationWithCount extends Location {
  observation_count: number
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
}

export interface User {
  id: number
  keycloak_id: string
  email: string
  name: string
  created_at: string
  updated_at: string
}

export interface AuthToken {
  access_token: string
  token_type: string
  expires_in: number
}

export interface AuthState {
  user: User | null
  token: string | null
  tokenExpiry: number | null
  isAuthenticated: boolean
}
