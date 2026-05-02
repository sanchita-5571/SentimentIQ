import { useEffect } from 'react'
import { Card, SectionTitle } from '../components/UI/Card'
import { useDataStore } from '../stores/dataStore'

export default function RootCausePage() {
  const rootCauses = useDataStore((state) => state.rootCauses)
  const loading = useDataStore((state) => state.loading.rootCauses)
  const fetchRootCauses = useDataStore((state) => state.fetchRootCauses)
  const rebuildRootCauses = useDataStore((state) => state.rebuildRootCauses)

  useEffect(() => {
    fetchRootCauses()
  }, [fetchRootCauses])

  return (
    <div className="space-y-6">
      <Card>
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <SectionTitle
            eyebrow="Root cause drilldown"
            title="Sentiment-drop events ranked by earliest degrading aspect"
            body="Each event compares the current day against the trailing baseline, identifies the first aspect to deteriorate, then traces the amplification chain."
          />
          <button
            type="button"
            onClick={rebuildRootCauses}
            className="rounded-2xl bg-cyan-300 px-4 py-3 text-sm font-semibold text-slate-950"
          >
            Recompute engine
          </button>
        </div>
      </Card>

      {loading ? <Card>Loading root-cause events...</Card> : null}
      {!loading && !rootCauses.length ? (
        <Card>No root-cause events yet. Ingest more dated reviews, then recompute the engine.</Card>
      ) : null}

      <div className="space-y-4">
        {rootCauses.map((event) => (
          <Card key={event.id}>
            <div className="flex flex-col gap-4 xl:flex-row xl:justify-between">
              <div className="max-w-3xl">
                <p className="text-xs uppercase tracking-[0.25em] text-rose-200">
                  {new Date(event.event_date).toLocaleDateString()}
                </p>
                <h3 className="mt-2 text-2xl font-semibold text-white">
                  First degrading aspect: {event.earliest_degrading_aspect || 'general'}
                </h3>
                <p className="mt-3 text-sm text-slate-300">
                  Baseline {event.baseline_sentiment.toFixed(2)} to {event.current_sentiment.toFixed(2)}.
                  Delta {event.sentiment_delta.toFixed(2)} across {event.review_volume} reviews.
                </p>
                <div className="mt-4 flex flex-wrap gap-2">
                  {(event.amplification_chain || []).map((node) => (
                    <span key={node} className="rounded-full bg-white/8 px-3 py-1 text-xs text-slate-100">
                      {node}
                    </span>
                  ))}
                </div>
              </div>
              <div className="space-y-3 xl:max-w-md">
                <p className="text-sm font-medium text-orange-200">Recommended actions</p>
                {(event.recommendations || []).map((recommendation) => (
                  <div key={recommendation.title} className="rounded-2xl border border-white/10 bg-slate-900/60 p-4">
                    <p className="font-medium text-white">{recommendation.title}</p>
                    <p className="mt-2 text-sm text-slate-300">{recommendation.action}</p>
                  </div>
                ))}
              </div>
            </div>
            <div className="mt-5 grid gap-3 md:grid-cols-2">
              {(event.evidence || []).map((evidence) => (
                <div key={evidence.review_id} className="rounded-2xl border border-white/10 bg-slate-900/50 p-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-white">Review #{evidence.review_id}</span>
                    <span className="text-xs text-rose-200">{evidence.sentiment_score.toFixed(2)}</span>
                  </div>
                  <p className="mt-3 text-sm text-slate-300">{evidence.snippet}</p>
                </div>
              ))}
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
