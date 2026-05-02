import { useEffect } from 'react'
import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import FilterBar from '../components/UI/FilterBar'
import { Card, SectionTitle } from '../components/UI/Card'
import { useDataStore } from '../stores/dataStore'
import { useFilterStore } from '../stores/filterStore'

export default function TrendsPage() {
  const filters = useFilterStore((state) => state.filters)
  const snapshot = useDataStore((state) => state.snapshot)
  const fetchSnapshot = useDataStore((state) => state.fetchSnapshot)

  useEffect(() => {
    fetchSnapshot(filters)
  }, [fetchSnapshot, filters])

  const aspectTrends = snapshot?.aspect_trends || []
  const colors = aspectTrends.map((item) => (item.delta < 0 ? '#fb7185' : '#34d399'))

  return (
    <div className="space-y-6">
      <FilterBar options={snapshot?.filter_options} />
      <Card>
        <SectionTitle
          eyebrow="Trend analytics"
          title="Aspect drift and topic pressure"
          body="This view highlights where sentiment is weakening first, which is often the earliest signal before the headline score falls."
        />
        <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
          <div className="h-96">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={aspectTrends}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
                <XAxis dataKey="aspect" tick={{ fill: '#cbd5e1' }} />
                <YAxis tick={{ fill: '#cbd5e1' }} />
                <Tooltip />
                <Bar dataKey="delta">
                  {aspectTrends.map((entry, index) => (
                    <Cell key={entry.aspect} fill={colors[index]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-3">
            {(snapshot?.topics || []).map((topic) => (
              <div key={topic.topic} className="rounded-2xl border border-white/10 bg-slate-900/60 p-4">
                <div className="flex items-center justify-between">
                  <p className="font-medium text-white">{topic.topic}</p>
                  <span className="text-sm text-slate-300">{topic.mentions}</span>
                </div>
                <p className="mt-2 text-sm text-slate-300">Avg sentiment {topic.avg_sentiment.toFixed(2)}</p>
              </div>
            ))}
          </div>
        </div>
      </Card>
    </div>
  )
}
