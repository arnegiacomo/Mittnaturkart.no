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
