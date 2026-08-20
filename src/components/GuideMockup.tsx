type GuideMockupProps = {
  compact?: boolean
}

const menuItems = ['Depois do almoço', 'Fim da tarde', 'À noite', 'Quero chocolate', 'Tenho 5 minutos']

export function GuideMockup({ compact = false }: GuideMockupProps) {
  return (
    <div className={`guide-composition${compact ? ' guide-composition--compact' : ''}`} aria-label="Prévia do guia digital aberto em um celular">
      {compact && (
        <>
          <div className="paper-layer paper-layer--back" aria-hidden="true">
            <span>SITUAÇÃO 11</span>
            <strong>Quero chocolate</strong>
          </div>
          <div className="paper-layer paper-layer--middle" aria-hidden="true">
            <span>DOCE EM 5</span>
            <strong>Tempo também decide</strong>
          </div>
        </>
      )}
      <div className="phone-shell">
        <div className="phone-speaker" aria-hidden="true" />
        <div className="phone-screen">
          <div className="phone-brand">
            <span className="brand-dot" />
            QUANDO BATE O DOCE
          </div>
          <p>O que está acontecendo agora?</p>
          <div className="phone-menu">
            {menuItems.map((item, index) => (
              <span key={item} className={index === 3 ? 'is-accent' : ''}>
                {item}
                <b aria-hidden="true">›</b>
              </span>
            ))}
          </div>
          <small>37 situações para consultar</small>
        </div>
      </div>
      {compact && (
        <>
          <span className="floating-tag floating-tag--one">consulta rápida</span>
          <span className="floating-tag floating-tag--two">37 situações</span>
          <span className="cocoa-shape cocoa-shape--one" aria-hidden="true" />
          <span className="cocoa-shape cocoa-shape--two" aria-hidden="true" />
        </>
      )}
    </div>
  )
}
