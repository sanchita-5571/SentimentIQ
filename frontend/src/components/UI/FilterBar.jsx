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
    <div className="grid w-full gap-3 rounded-[28px] border bg-card/80 p-4 backdrop-blur-sm md:grid-cols-2 2xl:grid-cols-4">
      {inputs.map((input) => (
        <label key={input.key} htmlFor={`filter-${input.key}`} className="space-y-2 text-sm text-muted-foreground">
          <span>{input.label}</span>
          {input.type === 'select' ? (
            <select
              id={`filter-${input.key}`}
              value={filters[input.key] || ''}
              onChange={(event) => setFilter(input.key, event.target.value)}
              className="w-full rounded-2xl border border-input bg-card/50 px-4 py-3 text-foreground ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
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
              className="w-full rounded-2xl border border-input bg-card/50 px-4 py-3 text-foreground ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              placeholder={input.type === 'text' ? 'Review content, topic, aspect...' : ''}
            />
          )}
        </label>
      ))}
      <button
        type="button"
        onClick={resetFilters}
        className="rounded-2xl border border-input bg-muted/50 hover:bg-muted px-4 py-3 text-sm font-medium text-muted-foreground transition hover:text-foreground"
      >
        Reset filters
      </button>
    </div>
  )
}
