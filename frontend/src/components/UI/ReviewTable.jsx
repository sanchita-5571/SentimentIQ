export default function ReviewTable({ reviews, loading, reviewMeta, onPageChange }) {

  const formatReviewDate = (value) => {
    if (!value) return 'Undated'
    const parsed = new Date(value)
    return Number.isNaN(parsed.getTime()) ? 'Undated' : parsed.toLocaleDateString()
  }

  if (loading) {
    return <div className="rounded-[28px] border border-border bg-card p-6 text-sm text-muted-foreground">Loading reviews...</div>
  }

  if (!reviews.length) {
    return (
      <div className="rounded-[28px] border border-border bg-card p-6 text-sm text-muted-foreground">
        No reviews match the current filters yet.
      </div>
    )
  }

  const currentPage = reviewMeta?.page || 1
  const totalPages = Math.max(Math.ceil((reviewMeta?.total || 0) / (reviewMeta?.page_size || 20)), 1)

  return (
    <div className="overflow-hidden rounded-[28px] border border-border bg-card">
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm text-foreground">
          <thead className="bg-muted/50 text-xs uppercase tracking-[0.2em] text-muted-foreground">
            <tr>
              <th className="px-4 py-3">Date</th>
              <th className="px-4 py-3">Source</th>
              <th className="px-4 py-3">Product</th>
              <th className="px-4 py-3">Sentiment</th>
              <th className="px-4 py-3">Topics</th>
              <th className="px-4 py-3">Review</th>
            </tr>
          </thead>
          <tbody>
            {reviews.map((review) => (
              <tr key={review.id} className="align-top border-t border-border/60">
                <td className="px-4 py-4">{formatReviewDate(review.review_date)}</td>
                <td className="px-4 py-4 capitalize">{review.source}</td>
                <td className="px-4 py-4">{review.product || "-"}</td>
                <td className="px-4 py-4">
                  <span
                    className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${
                      review.sentiment_label === "negative"
                        ? "bg-negative/10 text-negative"
                        : review.sentiment_label === "positive"
                          ? "bg-positive/10 text-positive"
                          : "bg-neutral/10 text-neutral"
                    }`}
                  >
                    {review.sentiment_label} ({review.sentiment_score.toFixed(2)})
                  </span>
                </td>
                <td className="px-4 py-4 text-muted-foreground">{(review.topics || []).join(", ") || "general feedback"}</td>
                <td className="max-w-xl px-4 py-4 text-foreground">{review.content}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex items-center justify-between border-t border-border/60 px-4 py-3 text-sm text-muted-foreground">
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <div className="flex gap-2">
          <button
            type="button"
            disabled={currentPage <= 1}
            onClick={() => onPageChange?.(currentPage - 1)}
            className="rounded-xl border border-border bg-background px-3 py-2 text-foreground disabled:opacity-40"
          >
            Previous
          </button>
          <button
            type="button"
            disabled={currentPage >= totalPages}
            onClick={() => onPageChange?.(currentPage + 1)}
            className="rounded-xl border border-border bg-background px-3 py-2 text-foreground disabled:opacity-40"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  )
}
