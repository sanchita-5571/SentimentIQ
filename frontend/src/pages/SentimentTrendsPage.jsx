import { useEffect } from 'react'
import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { AlertCircle } from 'lucide-react'
import FilterBar from '../components/UI/FilterBar'
import { Card, SectionTitle } from '../components/UI/Card'
import { useDataStore } from '../stores/dataStore'
import { useFilterStore } from '../stores/filterStore'

export default function SentimentTrendsPage() {
  const filters = useFilterStore((state) => state.filters)
  const snapshot = useDataStore((state) => state.snapshot)
  const fetchSnapshot = useDataStore((state) => state.fetchSnapshot)

  useEffect(() => {
    fetchSnapshot(filters)
  }, [fetchSnapshot, filters])

  const sentimentTrends = (snapshot?.timeline || []).map((item) => ({
    period: new Date(item.date).toLocaleDateString(),
    average_sentiment: item.average_sentiment,
    negative_reviews: item.negative_reviews,
    review_count: item.review_count,
  }))

  const deltaData = snapshot?.aspect_trends || []

  const colors = deltaData.map((item) => (item.delta < 0 ? '#fb7185' : '#34d399'))

  return (
    <div className="space-y-6">
      <FilterBar options={snapshot?.filter_options} />
      <Card>
        <SectionTitle
          eyebrow="Sentiment Trends"
          title="Sentiment Evolution Over Time"
          body="Track daily sentiment movement and compare aspect-level delta signals from the current filtered dataset."
        />
        <div className="grid gap-6 lg:grid-cols-2">
          <div className="h-80">
            {sentimentTrends.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={sentimentTrends}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.2)" />
                  <XAxis dataKey="period" tick={{ fill: 'currentColor' }} />
                  <YAxis tick={{ fill: 'currentColor' }} />
                  <Tooltip />
                  <Bar dataKey="average_sentiment" fill="#3b82f6" name="Average sentiment" />
                  <Bar dataKey="negative_reviews" fill="#ef4444" name="Negative reviews" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <EmptyChart message="Upload dated reviews to populate the sentiment trend chart." />
            )}
          </div>

          <div className="h-80">
            {deltaData.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={deltaData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.2)" />
                  <XAxis dataKey="aspect" tick={{ fill: 'currentColor' }} />
                  <YAxis tick={{ fill: 'currentColor' }} />
                  <Tooltip />
                  <Bar dataKey="delta" name="Aspect delta">
                    {deltaData.map((entry, index) => (
                      <Cell key={`cell-${entry.aspect}-${index}`} fill={colors[index]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <EmptyChart message="Aspect delta bars appear once the snapshot contains aspect trends." />
            )}
          </div>
        </div>

        {snapshot?.topics?.length ? (
          <div className="mt-8">
            <h3 className="text-lg font-semibold mb-4 text-foreground">Emerging Sentiment Topics</h3>
            <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
              {snapshot.topics.slice(0, 6).map((topic, idx) => (
                <div key={idx} className="rounded-xl border border-border/50 p-4 hover:bg-accent/50 transition-colors">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-foreground truncate">{topic.topic}</span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      topic.avg_sentiment > 0.1 ? 'bg-emerald-500/10 text-emerald-500' :
                      topic.avg_sentiment < -0.1 ? 'bg-red-500/10 text-red-500' :
                      'bg-amber-500/10 text-amber-500'
                    }`}>
                      {topic.avg_sentiment > 0 ? '+' : ''}{topic.avg_sentiment.toFixed(2)}
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">{topic.mentions} mentions</p>
                </div>
              ))}
            </div>
          </div>
        ) : null}
      </Card>
    </div>
  )
}

function EmptyChart({ message }) {
  return (
    <div className="flex h-full flex-col items-center justify-center rounded-2xl border border-dashed border-border text-center">
      <AlertCircle className="mb-3 h-10 w-10 text-muted-foreground" />
      <p className="max-w-sm text-sm text-muted-foreground">{message}</p>
    </div>
  )
}
