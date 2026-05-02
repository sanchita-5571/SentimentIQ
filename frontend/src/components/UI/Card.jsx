export function Card({ children, className = '' }) {
  return <section className={`rounded-[28px] border border-white/10 bg-white/5 p-5 shadow-2xl shadow-black/10 ${className}`}>{children}</section>
}

export function SectionTitle({ eyebrow, title, body }) {
  return (
    <div className="mb-5">
      {eyebrow ? <p className="text-xs uppercase tracking-[0.25em] text-cyan-300">{eyebrow}</p> : null}
      <h3 className="mt-2 text-xl font-semibold text-white">{title}</h3>
      {body ? <p className="mt-2 text-sm text-slate-300">{body}</p> : null}
    </div>
  )
}
