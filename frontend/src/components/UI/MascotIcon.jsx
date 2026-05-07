import React from 'react'

/**
 * Inline SVG mascot so we don't need external assets.
 * Usage: <MascotIcon className="h-8 w-8" />
 */
export default function MascotIcon({ className = 'h-10 w-10' }) {
  return (
    <svg
      className={className}
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      aria-hidden="true"
    >
      <defs>
        <linearGradient id="g1" x1="8" y1="8" x2="56" y2="56" gradientUnits="userSpaceOnUse">
          <stop stopColor="hsl(215 85% 58%)" />
          <stop offset="1" stopColor="hsl(170 85% 45%)" />
        </linearGradient>
        <linearGradient id="g2" x1="18" y1="4" x2="54" y2="60" gradientUnits="userSpaceOnUse">
          <stop stopColor="hsl(290 90% 68%)" stopOpacity="0.9" />
          <stop offset="1" stopColor="hsl(215 85% 58%)" stopOpacity="1" />
        </linearGradient>
        <filter
          id="softGlow"
          x="-30%"
          y="-30%"
          width="160%"
          height="160%"
          colorInterpolationFilters="sRGB"
        >
          <feGaussianBlur stdDeviation="3" result="blur" />
          <feColorMatrix
            in="blur"
            type="matrix"
            values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 .55 0"
            result="glow"
          />
          <feMerge>
            <feMergeNode in="glow" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {/* outer orb */}
      <circle cx="32" cy="32" r="26" fill="url(#g2)" opacity="0.18" />
      <circle cx="32" cy="32" r="24" fill="none" stroke="url(#g1)" strokeWidth="3" opacity="0.9" filter="url(#softGlow)" />

      {/* face */}
      <path
        d="M19 33c0-9 6-16 13-16s13 7 13 16c0 10-6 18-13 18s-13-8-13-18Z"
        fill="hsl(0 0% 100% / 0.06)"
        stroke="hsl(215 85% 58% / 0.55)"
        strokeWidth="2"
      />

      {/* eyes */}
      <circle cx="26" cy="32" r="4" fill="hsl(215 85% 58%)" />
      <circle cx="38" cy="32" r="4" fill="hsl(215 85% 58%)" />
      <circle cx="24.8" cy="30.7" r="1.2" fill="white" opacity="0.9" />
      <circle cx="36.8" cy="30.7" r="1.2" fill="white" opacity="0.9" />

      {/* smile */}
      <path
        d="M25 40c2.1 3 5.2 4.5 7 4.5S37.9 43 40 40"
        stroke="url(#g1)"
        strokeWidth="3"
        strokeLinecap="round"
        fill="none"
      />

      {/* antenna / signal */}
      <path d="M32 10v10" stroke="url(#g1)" strokeWidth="3" strokeLinecap="round" />
      <path
        d="M23 16c3 2 5.8 3 9 3 3.2 0 6-1 9-3"
        stroke="hsl(170 85% 45% / 0.65)"
        strokeWidth="2"
        strokeLinecap="round"
        fill="none"
      />

      {/* subtle sparkle */}
      <path
        d="M10 28l2 1-2 1-1 2-1-2-2-1 2-1 1-2 1 2Z"
        fill="hsl(290 90% 68% / 0.65)"
      />
      <path
        d="M54 43l2 1-2 1-1 2-1-2-2-1 2-1 1-2 1 2Z"
        fill="hsl(215 85% 58% / 0.65)"
      />
    </svg>
  )
}

