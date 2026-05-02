import { useEffect } from 'react'
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { useDataStore } from '../stores/dataStore'
import { useFilterStore } from '../stores/filterStore'
import FilterBar from '../components/UI/FilterBar'
import UploadPanel from '../components/UI/UploadPanel'
import StatGrid from '../components/UI/StatGrid'
import { Card, SectionTitle } from '../components/UI/Card'

export default function DashboardPage() {
  const filters = useFilterStore((state) => state.filters)
  const snapshot = useDataStore((state) => state.snapshot)
  const loading = useDataStore((state) => state.loading.snapshot)
  const rootCauses = useDataStore((state) => state.rootCauses)
  const fetchSnapshot = useDataStore((state) => state.fetchSnapshot)
  const fetchRootCauses = useDataStore((state) => state.fetchRootCauses)

  useEffect(() => {
    fetchSnapshot(filters)
    const interval = window.setInterval(() => fetchSnapshot(filters), 15000)
    return () => window.clearInterval(interval)
  }, [fetchSnapshot, filters])

  useEffect(() => {
    fetchRootCauses()
  }, [fetchRootCauses])

  const timeline = snapshot?.timeline || []

  return (
    <div className="space-y-6">
      <FilterBar options={snapshot?.filter_options} />
      <UploadPanel />
      <StatGrid overview={snapshot?.overview || {}} />
      <div className="grid gap-6 xl:grid-cols-[1.6fr_1fr]">
        <Card>
          <SectionTitle
            eyebrow="Overview page"
            title="Sentiment trend and review volume"
            body="The dashboard refreshes automatically so chart state and shared filters stay synchronized across views."
          />
          <div className="h-80">
            {loading ? (
              <div className="flex h-full items-center justify-center text-sm text-slate-300">Refreshing live chart...</div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={timeline}>
                  <defs>
                    <linearGradient id="sentimentArea" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.45} />
                      <stop offset="95%" stopColor="#22d3ee" stopOpacity={0.02} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
                  <XAxis dataKey="date" tick={{ fill: '#cbd5e1' }} tickFormatter={(value) => new Date(value).toLocaleDateString()} />
                  <YAxis tick={{ fill: '#cbd5e1' }} />
                  <Tooltip />
                  <Area type="monotone" dataKey="average_sentiment" stroke="#22d3ee" fill="url(#sentimentArea)" />
                  <Area type="monotone" dataKey="review_count" stroke="#fb923c" fillOpacity={0} />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        </Card>
        <Card>
          <SectionTitle eyebrow="Hot topics" title="Current conversation clusters" />
          <div className="space-y-4">
            {(snapshot?.topics || []).map((topic) => (
              <div key={topic.topic} className="rounded-2xl border border-white/10 bg-slate-900/50 p-4">
                <div className="flex items-center justify-between">
                  <p className="font-medium text-white">{topic.topic}</p>
                  <span className="text-sm text-slate-300">{topic.mentions} mentions</span>
                </div>
                <p className="mt-2 text-sm text-slate-300">Average sentiment: {topic.avg_sentiment.toFixed(2)}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>
      <Card>
        <SectionTitle
          eyebrow="Live diagnostics"
          title="Most recent root-cause signals"
          body="These are the latest sentiment-drop events detected from the review timeline."
        />
        <div className="grid gap-4 lg:grid-cols-2">
          {(rootCauses || []).slice(0, 4).map((event) => (
            <div key={event.id} className="rounded-2xl border border-white/10 bg-slate-900/60 p-4">
              <p className="text-xs uppercase tracking-[0.25em] text-rose-200">
                {new Date(event.event_date).toLocaleDateString()}
              </p>
              <p className="mt-2 text-lg font-semibold text-white">
                {event.earliest_degrading_aspect || "general"} triggered the first drop
              </p>
              <p className="mt-2 text-sm text-slate-300">
                Delta {event.sentiment_delta.toFixed(2)} across {event.review_volume} reviews.
              </p>
            </div>
          ))}
          {!rootCauses?.length ? (
            <div className="rounded-2xl border border-white/10 bg-slate-900/40 p-4 text-sm text-slate-300">
              No sentiment-drop events have been detected yet.
            </div>
          ) : null}
        </div>
      </Card>
    </div>
  )
}
