import { cn } from '../../lib/utils'

export function Card({
  children,
  className,
  ...props
}) {
  return (
    <section
      className={cn(
        'rounded-3xl border bg-card text-card-foreground shadow-xl animate-fade-in',
        className
      )}
      {...props}
    >
      {children}
    </section>
  )
}

export function SectionTitle({ eyebrow, title, body }) {
  return (
    <div className="mb-5">
      {eyebrow ? <p className="text-xs uppercase tracking-[0.25em] text-primary">{eyebrow}</p> : null}
      <h3 className="mt-2 text-xl font-semibold text-foreground">{title}</h3>
      {body ? <p className="mt-2 text-sm text-muted-foreground">{body}</p> : null}
    </div>
  )
}
