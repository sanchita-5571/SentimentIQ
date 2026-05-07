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
    <div className="glass-panel grid w-full gap-3 rounded-[30px] border border-white/10 p-4 shadow-xl shadow-slate-950/10 backdrop-blur-sm md:grid-cols-2 2xl:grid-cols-4">
      {inputs.map((input) => (
        <label key={input.key} htmlFor={`filter-${input.key}`} className="space-y-2 text-sm text-muted-foreground">
          <span className="pl-1 text-[11px] font-semibold uppercase tracking-[0.24em]">{input.label}</span>
          {input.type === 'select' ? (
            <select
              id={`filter-${input.key}`}
              value={filters[input.key] || ''}
              onChange={(event) => setFilter(input.key, event.target.value)}
              className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-foreground ring-offset-background transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
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
              id={`filter-${input.key}`}
              type={input.type}
              value={filters[input.key] || ''}
              onChange={(event) => setFilter(input.key, event.target.value)}
              className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-foreground ring-offset-background transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              placeholder={input.type === 'text' ? 'Review content, topic, aspect...' : ''}
            />
          )}
        </label>
      ))}
      <button
        type="button"
        onClick={resetFilters}
        className="rounded-2xl border border-white/10 bg-[linear-gradient(135deg,hsl(var(--primary)/0.18),hsl(var(--secondary)/0.16))] px-4 py-3 text-sm font-semibold text-foreground transition hover:brightness-110"
      >
        Reset filters
      </button>
    </div>
  )
}
