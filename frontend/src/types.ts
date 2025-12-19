export interface Observation {
  id?: number
  species: string
  date: string
  latitude: number
  longitude: number
  notes?: string
  category: string
  created_at?: string
  updated_at?: string
}
