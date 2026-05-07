import { cn } from '../../lib/utils'

export function Card({
  children,
  className,
  ...props
}) {
  return (
    <section
      className={cn(
        'glass-panel hero-glow rounded-[32px] border border-white/10 text-card-foreground shadow-xl animate-fade-in',
        'relative overflow-hidden',
        'before:absolute before:inset-0 before:pointer-events-none before:opacity-100',
        'before:bg-[radial-gradient(520px_circle_at_top_left,hsl(var(--ring)/0.14),transparent_35%)]',
        'after:absolute after:inset-x-8 after:top-0 after:h-px after:bg-white/10 after:content-[""]',
        'transition-[box-shadow,transform,border-color] duration-300 hover:-translate-y-1 hover:border-white/20',
        className
      )}
      {...props}
    >
      <div className="relative z-10">{children}</div>
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
