import { BowlIcon } from './Icons'

export function Brand({ compact = false }: { compact?: boolean }) {
  return (
    <span className={`brand${compact ? ' brand--compact' : ''}`}>
      <span className="brand__symbol"><BowlIcon /></span>
      <span className="brand__copy">
        <span className="brand__name">PRATO <em>10X</em></span>
        {!compact && <small>Refeições menores. Escolhas mais inteligentes.</small>}
      </span>
    </span>
  )
}
