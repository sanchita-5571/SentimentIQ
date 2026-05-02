import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const defaultFilters = {
  search: '',
  source: '',
  product: '',
  category: '',
  sentiment_label: '',
  language: '',
  start_date: '',
  end_date: '',
}

export const useFilterStore = create(
  persist(
    (set) => ({
      filters: defaultFilters,
      setFilter: (key, value) =>
        set((state) => ({
          filters: {
            ...state.filters,
            [key]: value,
          },
        })),
      setFilters: (nextFilters) => set(() => ({ filters: { ...defaultFilters, ...nextFilters } })),
      resetFilters: () => set({ filters: defaultFilters }),
    }),
    {
      name: 'sentimentiq-filters',
    },
  ),
)
