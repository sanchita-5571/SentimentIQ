import { Card } from './Card'

export default function StatGrid({ overview }) {
  const items = [
    ['Total reviews', overview?.total_reviews ?? 0],
    ['Average sentiment', `${Math.round((overview?.average_sentiment ?? 0) * 100)}%`],
    ['Negative ratio', `${Math.round((overview?.negative_ratio ?? 0) * 100)}%`],
    ['Average rating', (overview?.average_rating ?? 0).toFixed(2)],
    ['Active topics', overview?.active_topics ?? 0],
    ['Duplicates removed', overview?.duplicates_removed ?? 0],
  ]

  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {items.map(([label, value]) => (
        <Card key={label} className="bg-gradient-to-br from-white/8 to-white/3">
          <p className="text-sm text-slate-300">{label}</p>
          <p className="mt-3 text-3xl font-semibold text-white">{value}</p>
        </Card>
      ))}
    </div>
  )
}
