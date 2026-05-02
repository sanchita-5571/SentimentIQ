import { useMemo } from 'react'
import { useFilterStore } from '../../stores/filterStore'

export default function Navbar() {
  const filters = useFilterStore((state) => state.filters)

  const activeFilterCount = useMemo(
    () => Object.values(filters).filter((value) => value !== '').length,
    [filters],
  )

  return (
    <header className="sticky top-0 z-20 border-b border-white/10 bg-slate-950/70 px-4 py-4 backdrop-blur md:px-8">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.25em] text-orange-300">Live workspace</p>
          <h2 className="text-xl font-semibold text-white">Customer sentiment control room</h2>
        </div>
        <div className="flex items-center gap-3">
          <div className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-200">
            {activeFilterCount} active filters
          </div>
        </div>
      </div>
    </header>
  )
}
