export default function ReviewTable({ reviews, loading, reviewMeta, onPageChange }) {
  if (loading) {
    return <div className="rounded-[28px] border border-white/10 bg-white/5 p-6 text-sm text-slate-300">Loading reviews...</div>
  }

  if (!reviews.length) {
    return (
      <div className="rounded-[28px] border border-white/10 bg-white/5 p-6 text-sm text-slate-300">
        No reviews match the current filters yet.
      </div>
    )
  }

  const currentPage = reviewMeta?.page || 1
  const totalPages = Math.max(Math.ceil((reviewMeta?.total || 0) / (reviewMeta?.page_size || 20)), 1)

  return (
    <div className="overflow-hidden rounded-[28px] border border-white/10 bg-white/5">
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm text-slate-200">
          <thead className="bg-white/5 text-xs uppercase tracking-[0.2em] text-slate-400">
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
              <tr key={review.id} className="border-t border-white/5 align-top">
                <td className="px-4 py-4">{new Date(review.review_date).toLocaleDateString()}</td>
                <td className="px-4 py-4 capitalize">{review.source}</td>
                <td className="px-4 py-4">{review.product || "-"}</td>
                <td className="px-4 py-4">
                  <span
                    className={`rounded-full px-3 py-1 text-xs font-semibold ${
                      review.sentiment_label === "negative"
                        ? "bg-rose-400/15 text-rose-100"
                        : review.sentiment_label === "positive"
                          ? "bg-emerald-400/15 text-emerald-100"
                          : "bg-slate-500/15 text-slate-200"
                    }`}
                  >
                    {review.sentiment_label} ({review.sentiment_score.toFixed(2)})
                  </span>
                </td>
                <td className="px-4 py-4">{(review.topics || []).join(", ") || "general feedback"}</td>
                <td className="max-w-xl px-4 py-4 text-slate-100">{review.content}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex items-center justify-between border-t border-white/5 px-4 py-3 text-sm text-slate-300">
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <div className="flex gap-2">
          <button
            type="button"
            disabled={currentPage <= 1}
            onClick={() => onPageChange?.(currentPage - 1)}
            className="rounded-xl border border-white/10 px-3 py-2 disabled:opacity-40"
          >
            Previous
          </button>
          <button
            type="button"
            disabled={currentPage >= totalPages}
            onClick={() => onPageChange?.(currentPage + 1)}
            className="rounded-xl border border-white/10 px-3 py-2 disabled:opacity-40"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  )
}
