import type { SortOrder } from './enums'

export interface PaginationParams {
  limit?: number
  offset?: number
  sort?: string
  order?: SortOrder
}

export interface PaginationMeta {
  total: number
  limit: number
  offset: number
  hasMore: boolean
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: PaginationMeta
}
