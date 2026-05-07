import { useEffect, useMemo } from 'react'
import { Card, SectionTitle } from '../components/UI/Card'
import FilterBar from '../components/UI/FilterBar'
import { useDataStore } from '../stores/dataStore'
import { useFilterStore } from '../stores/filterStore'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts'

export default function TrendsPage() {
  const filters = useFilterStore((state) => state.filters)
  const snapshot = useDataStore((state) => state.snapshot)
  const fetchSnapshot = useDataStore((state) => state.fetchSnapshot)

  useEffect(() => {
    fetchSnapshot(filters)
  }, [fetchSnapshot, filters])

  const data = useMemo(() => {
    // “General trends” uses the timeline but shows only sentiment.
    return (snapshot?.timeline || []).map((row) => ({
      date: new Date(row.date).toLocaleDateString(),
      average_sentiment: row.average_sentiment,
    }))
  }, [snapshot])

  return (
    <div className="space-y-6">
      <FilterBar options={snapshot?.filter_options} />
      <Card>
        <SectionTitle
          eyebrow="Trends"
          title="Overall sentiment trend"
          body="A simplified trend view (timeline average sentiment only) for quick monitoring."
        />

        <div className="h-96">
          {data.length ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.2)" />
                <XAxis dataKey="date" tick={{ fill: 'currentColor' }} tickLine={false} axisLine={false} />
                <YAxis tick={{ fill: 'currentColor' }} tickLine={false} axisLine={false} />
                <Tooltip />
                <Line type="monotone" dataKey="average_sentiment" stroke="#3b82f6" strokeWidth={3} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full flex items-center justify-center text-sm text-muted-foreground">
              Upload dated reviews to populate the sentiment trend chart.
            </div>
          )}
        </div>
      </Card>
    </div>
  )
}


