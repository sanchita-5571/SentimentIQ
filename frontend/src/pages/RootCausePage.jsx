import { useEffect, useMemo, useState } from 'react'
import { Card, SectionTitle } from '../components/UI/Card'
import { Badge } from '../components/UI/badge'
import { Button } from '../components/UI/button'
import { Skeleton } from '../components/UI/Skeleton'
import { useDataStore } from '../stores/dataStore'

export default function RootCausePage() {
  const rootCauses = useDataStore((state) => state.rootCauses)
  const loading = useDataStore((state) => state.loading.rootCauses)
  const fetchRootCauses = useDataStore((state) => state.fetchRootCauses)
  const rebuildRootCauses = useDataStore((state) => state.rebuildRootCauses)
  const [selectedId, setSelectedId] = useState(null)

  useEffect(() => {
    fetchRootCauses()
  }, [fetchRootCauses])

  const selectedEvent = useMemo(() => {
    if (!rootCauses.length) {
      return null
    }

    return rootCauses.find((event) => event.id === selectedId) || rootCauses[0]
  }, [rootCauses, selectedId])

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="text-3xl font-bold">Root Cause Analysis</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Review the latest sentiment-drop events, the affected aspect, and the supporting evidence.
          </p>
        </div>
        <Button onClick={rebuildRootCauses}>Rebuild root-cause engine</Button>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.1fr,0.9fr]">
        <Card className="p-6">
          <SectionTitle
            eyebrow="Events"
            title="Detected sentiment drops"
            body="Events are generated from dated reviews. Pick one to inspect the degradation chain."
          />
          <div className="space-y-4">
            {loading ? (
              <>
                <Skeleton className="h-24 rounded-2xl" />
                <Skeleton className="h-24 rounded-2xl" />
                <Skeleton className="h-24 rounded-2xl" />
              </>
            ) : rootCauses.length ? (
              rootCauses.map((event) => (
                <button
                  key={event.id}
                  type="button"
                  onClick={() => setSelectedId(event.id)}
                  className={`w-full rounded-2xl border p-5 text-left transition ${
                    selectedEvent?.id === event.id
                      ? 'border-primary bg-primary/5'
                      : 'border-border hover:bg-accent'
                  }`}
                >
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <h3 className="font-semibold">
                        {event.earliest_degrading_aspect || 'General sentiment shift'}
                      </h3>
                      <p className="mt-1 text-sm text-muted-foreground">
                        {event.sentiment_delta?.toFixed(2)} sentiment delta across {event.review_volume} reviews
                      </p>
                    </div>
                    <Badge variant={event.sentiment_delta <= -0.35 ? 'destructive' : 'secondary'}>
                      {event.event_date ? new Date(event.event_date).toLocaleDateString() : 'Undated'}
                    </Badge>
                  </div>
                  {!!event.amplification_chain?.length && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      {event.amplification_chain.map((aspect) => (
                        <span
                          key={aspect}
                          className="rounded-full border border-border px-3 py-1 text-xs text-muted-foreground"
                        >
                          {aspect}
                        </span>
                      ))}
                    </div>
                  )}
                </button>
              ))
            ) : (
              <div className="rounded-2xl border border-dashed border-border p-8 text-sm text-muted-foreground">
                No root causes have been detected yet. Upload dated reviews and run a rebuild to populate this view.
              </div>
            )}
          </div>
        </Card>

        <Card className="p-6">
          <SectionTitle
            eyebrow="Details"
            title={selectedEvent?.earliest_degrading_aspect || 'Select an event'}
            body="The selected event shows the baseline change, evidence snippets, and recommended remediation steps."
          />
          {selectedEvent ? (
            <div className="space-y-6">
              <div className="grid gap-4 md:grid-cols-2">
                <Metric label="Baseline sentiment" value={selectedEvent.baseline_sentiment?.toFixed(2)} />
                <Metric label="Current sentiment" value={selectedEvent.current_sentiment?.toFixed(2)} />
                <Metric label="Sentiment delta" value={selectedEvent.sentiment_delta?.toFixed(2)} />
                <Metric label="Review volume" value={String(selectedEvent.review_volume ?? 0)} />
              </div>

              <div>
                <h3 className="font-semibold">Amplification chain</h3>
                <div className="mt-3 flex flex-wrap gap-2">
                  {(selectedEvent.amplification_chain?.length
                    ? selectedEvent.amplification_chain
                    : ['No secondary aspects identified']
                  ).map((aspect) => (
                    <span
                      key={aspect}
                      className="rounded-full bg-muted px-3 py-1 text-xs text-muted-foreground"
                    >
                      {aspect}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="font-semibold">Evidence</h3>
                <div className="mt-3 space-y-3">
                  {(selectedEvent.evidence || []).length ? (
                    selectedEvent.evidence.map((item) => (
                      <div key={item.review_id} className="rounded-2xl border border-border p-4">
                        <p className="text-sm text-foreground">{item.snippet}</p>
                        <div className="mt-3 flex flex-wrap gap-2 text-xs text-muted-foreground">
                          <span>Sentiment: {item.sentiment_score?.toFixed?.(2) ?? item.sentiment_score}</span>
                          {(item.aspects || []).map((aspect) => (
                            <span key={aspect} className="rounded-full bg-muted px-2 py-1">
                              {aspect}
                            </span>
                          ))}
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="mt-3 text-sm text-muted-foreground">No evidence snippets are available for this event.</p>
                  )}
                </div>
              </div>

              <div>
                <h3 className="font-semibold">Recommendations</h3>
                <div className="mt-3 space-y-3">
                  {(selectedEvent.recommendations || []).length ? (
                    selectedEvent.recommendations.map((item) => (
                      <div key={item.title} className="rounded-2xl border border-border p-4">
                        <div className="flex items-center justify-between gap-3">
                          <p className="font-medium">{item.title}</p>
                          <Badge variant={item.priority === 'high' ? 'destructive' : 'secondary'}>
                            {item.priority}
                          </Badge>
                        </div>
                        <p className="mt-2 text-sm text-muted-foreground">{item.action}</p>
                      </div>
                    ))
                  ) : (
                    <p className="mt-3 text-sm text-muted-foreground">No recommendations are available for this event yet.</p>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="rounded-2xl border border-dashed border-border p-8 text-sm text-muted-foreground">
              Choose an event from the list to inspect the cause chain and remediation steps.
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}

function Metric({ label, value }) {
  return (
    <div className="rounded-2xl border border-border p-4">
      <p className="text-sm text-muted-foreground">{label}</p>
      <p className="mt-2 text-2xl font-semibold">{value ?? '0.00'}</p>
    </div>
  )
}
