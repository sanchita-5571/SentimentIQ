import { useState } from 'react'
import { Filter, X, ChevronDown } from 'lucide-react'
import clsx from 'clsx'

export default function Filters({
  filters = {},
  onFiltersChange,
  className = ''
}) {
  const [isOpen, setIsOpen] = useState(false)

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value }
    onFiltersChange?.(newFilters)
  }

  const removeFilter = (key) => {
    const newFilters = { ...filters }
    delete newFilters[key]
    onFiltersChange?.(newFilters)
  }

  const clearAllFilters = () => {
    onFiltersChange?.({})
  }

  const activeFiltersCount = Object.keys(filters).length

  return (
    <div className={clsx('relative', className)}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={clsx(
          'flex items-center gap-2 px-4 py-2 rounded-lg border border-border bg-card hover:bg-muted transition-colors',
          activeFiltersCount > 0 && 'border-primary'
        )}
      >
        <Filter className="w-4 h-4" />
        <span>Filters</span>
        {activeFiltersCount > 0 && (
          <span className="bg-primary text-primary-foreground text-xs px-2 py-1 rounded-full">
            {activeFiltersCount}
          </span>
        )}
        <ChevronDown className={clsx(
          'w-4 h-4 transition-transform',
          isOpen && 'rotate-180'
        )} />
      </button>

      {isOpen && (
        <>
          {}
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />

          {}
          <div className="absolute top-full left-0 mt-2 w-80 bg-card border border-border rounded-lg shadow-lg z-20 p-4">
            <div className="space-y-4">
              {}
              <div>
                <label className="block text-sm font-medium mb-2">Date Range</label>
                <div className="flex gap-2">
                  <input
                    type="date"
                    value={filters.startDate || ''}
                    onChange={(e) => handleFilterChange('startDate', e.target.value)}
                    className="flex-1 px-3 py-2 text-sm rounded border border-border bg-background"
                  />
                  <input
                    type="date"
                    value={filters.endDate || ''}
                    onChange={(e) => handleFilterChange('endDate', e.target.value)}
                    className="flex-1 px-3 py-2 text-sm rounded border border-border bg-background"
                  />
                </div>
              </div>

              {}
              <div>
                <label className="block text-sm font-medium mb-2">Source</label>
                <select
                  value={filters.source || ''}
                  onChange={(e) => handleFilterChange('source', e.target.value)}
                  className="w-full px-3 py-2 text-sm rounded border border-border bg-background"
                >
                  <option value="">All Sources</option>
                  <option value="csv">CSV</option>
                  <option value="excel">Excel</option>
                  <option value="reddit">Reddit</option>
                </select>
              </div>

              {}
              <div>
                <label className="block text-sm font-medium mb-2">Sentiment</label>
                <select
                  value={filters.sentiment || ''}
                  onChange={(e) => handleFilterChange('sentiment', e.target.value)}
                  className="w-full px-3 py-2 text-sm rounded border border-border bg-background"
                >
                  <option value="">All Sentiments</option>
                  <option value="positive">Positive</option>
                  <option value="negative">Negative</option>
                  <option value="neutral">Neutral</option>
                </select>
              </div>

              {}
              <div>
                <label className="block text-sm font-medium mb-2">Rating</label>
                <select
                  value={filters.rating || ''}
                  onChange={(e) => handleFilterChange('rating', e.target.value)}
                  className="w-full px-3 py-2 text-sm rounded border border-border bg-background"
                >
                  <option value="">All Ratings</option>
                  <option value="5">5 Stars</option>
                  <option value="4">4 Stars</option>
                  <option value="3">3 Stars</option>
                  <option value="2">2 Stars</option>
                  <option value="1">1 Star</option>
                </select>
              </div>

              {}
              <div className="flex justify-between pt-4 border-t border-border">
                <button
                  onClick={clearAllFilters}
                  className="text-sm text-muted-foreground hover:text-foreground"
                >
                  Clear All
                </button>
                <button
                  onClick={() => setIsOpen(false)}
                  className="px-4 py-2 bg-primary text-primary-foreground rounded hover:bg-primary/90"
                >
                  Apply Filters
                </button>
              </div>
            </div>
          </div>
        </>
      )}

      {}
      {activeFiltersCount > 0 && (
        <div className="flex flex-wrap gap-2 mt-2">
          {Object.entries(filters).map(([key, value]) => (
            <span
              key={key}
              className="inline-flex items-center gap-1 px-2 py-1 text-xs bg-primary/10 text-primary rounded-full"
            >
              {key}: {value}
              <button
                onClick={() => removeFilter(key)}
                className="hover:bg-primary/20 rounded-full p-0.5"
              >
                <X className="w-3 h-3" />
              </button>
            </span>
          ))}
        </div>
      )}
    </div>
  )
}
