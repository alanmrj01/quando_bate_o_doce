import type { SVGProps } from 'react'

type IconProps = SVGProps<SVGSVGElement>

const base = {
  width: 24,
  height: 24,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 1.8,
  strokeLinecap: 'round' as const,
  strokeLinejoin: 'round' as const,
  'aria-hidden': true,
}

export function ArrowRightIcon(props: IconProps) {
  return <svg {...base} {...props}><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg>
}

export function CheckIcon(props: IconProps) {
  return <svg {...base} {...props}><path d="m5 12 4 4L19 6"/></svg>
}

export function ClockIcon(props: IconProps) {
  return <svg {...base} {...props}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>
}

export function BowlIcon(props: IconProps) {
  return <svg {...base} {...props}><path d="M4 10h16c0 5-3.6 9-8 9s-8-4-8-9Z"/><path d="M7 7c1-2 3-3 5-3M12 8c1.1-2 2.8-3 5-3M9 19h6"/></svg>
}

export function TargetIcon(props: IconProps) {
  return <svg {...base} {...props}><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/><path d="M15 9l5-5M16 4h4v4"/></svg>
}

export function GridIcon(props: IconProps) {
  return <svg {...base} {...props}><rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="3" width="8" height="8" rx="2"/><rect x="3" y="13" width="8" height="8" rx="2"/><rect x="13" y="13" width="8" height="8" rx="2"/></svg>
}

export function BagIcon(props: IconProps) {
  return <svg {...base} {...props}><path d="M5 8h14l1 12H4L5 8Z"/><path d="M9 9V6a3 3 0 0 1 6 0v3"/></svg>
}

export function CalendarIcon(props: IconProps) {
  return <svg {...base} {...props}><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/></svg>
}

export function BookIcon(props: IconProps) {
  return <svg {...base} {...props}><path d="M4 5.5A3.5 3.5 0 0 1 7.5 2H11v17H7.5A3.5 3.5 0 0 0 4 22V5.5Z"/><path d="M20 5.5A3.5 3.5 0 0 0 16.5 2H13v17h3.5A3.5 3.5 0 0 1 20 22V5.5Z"/></svg>
}

export function ShieldIcon(props: IconProps) {
  return <svg {...base} {...props}><path d="M12 3 4.5 6v5.2c0 4.7 3.2 8.1 7.5 9.8 4.3-1.7 7.5-5.1 7.5-9.8V6L12 3Z"/><path d="m8.8 12 2.1 2.1 4.5-4.5"/></svg>
}

export function QuestionIcon(props: IconProps) {
  return <svg {...base} {...props}><circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.7 2.7 0 1 1 4.6 1.9c-.9.8-2.1 1.3-2.1 3.1M12 17h.01"/></svg>
}

export function MenuIcon(props: IconProps) {
  return <svg {...base} {...props}><path d="M4 7h16M4 12h16M4 17h16"/></svg>
}

export function CloseIcon(props: IconProps) {
  return <svg {...base} {...props}><path d="m6 6 12 12M18 6 6 18"/></svg>
}

export function LockIcon(props: IconProps) {
  return <svg {...base} {...props}><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>
}

export function LeafIcon(props: IconProps) {
  return <svg {...base} {...props}><path d="M20 4C12 4 6 8 6 14c0 3 2 5 5 5 6 0 9-7 9-15Z"/><path d="M4 21c2-5 6-9 12-12"/></svg>
}
