import { useFilterStore } from '../../stores/filterStore'

export default function FilterBar({ options = {} }) {
  const filters = useFilterStore((state) => state.filters)
  const setFilter = useFilterStore((state) => state.setFilter)
  const resetFilters = useFilterStore((state) => state.resetFilters)

  const inputs = [
    { key: 'search', label: 'Search', type: 'text' },
    { key: 'source', label: 'Source', type: 'select', options: options.sources || [] },
    { key: 'product', label: 'Product', type: 'select', options: options.products || [] },
    { key: 'category', label: 'Category', type: 'select', options: options.categories || [] },
    { key: 'sentiment_label', label: 'Sentiment', type: 'select', options: ['positive', 'neutral', 'negative'] },
    { key: 'language', label: 'Language', type: 'select', options: options.languages || [] },
    { key: 'start_date', label: 'From', type: 'date' },
    { key: 'end_date', label: 'To', type: 'date' },
  ]

  return (
    <div className="grid gap-3 rounded-[28px] border border-white/10 bg-white/5 p-4 md:grid-cols-2 xl:grid-cols-4">
      {inputs.map((input) => (
        <label key={input.key} className="space-y-2 text-sm text-slate-300">
          <span>{input.label}</span>
          {input.type === 'select' ? (
            <select
              value={filters[input.key] || ''}
              onChange={(event) => setFilter(input.key, event.target.value)}
              className="w-full rounded-2xl border border-white/10 bg-slate-900/70 px-4 py-3 text-white outline-none"
            >
              <option value="">All</option>
              {input.options.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          ) : (
            <input
              type={input.type}
              value={filters[input.key] || ''}
              onChange={(event) => setFilter(input.key, event.target.value)}
              className="w-full rounded-2xl border border-white/10 bg-slate-900/70 px-4 py-3 text-white outline-none"
              placeholder={input.type === 'text' ? 'Review content, topic, aspect...' : ''}
            />
          )}
        </label>
      ))}
      <button
        type="button"
        onClick={resetFilters}
        className="rounded-2xl border border-orange-300/30 bg-orange-400/10 px-4 py-3 text-sm font-medium text-orange-100 transition hover:bg-orange-400/20"
      >
        Reset filters
      </button>
    </div>
  )
}
