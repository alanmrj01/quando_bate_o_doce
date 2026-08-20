const times = [
  ['2', 'minutos', 'uma decisão quase imediata'],
  ['5', 'minutos', 'pouco tempo, ainda com escolha'],
  ['10', 'minutos', 'uma janela curta para preparar'],
] as const

export function QuickTimeSection() {
  return (
    <section className="quick-time-section section-block" data-reveal>
      <div className="quick-time-copy">
        <span className="section-index">08 / doce em 5</span>
        <h2>Porque uma opção de 40 minutos não compete com aquilo que já está pronto</h2>
        <p>O tempo disponível também faz parte da organização da decisão. A opção precisa caber no momento — não apenas parecer boa em outra realidade.</p>
      </div>

      <div className="time-dial" aria-label="Opções organizadas por tempo disponível">
        {times.map(([number, unit, copy], index) => (
          <article key={number} className={index === 1 ? 'is-featured' : ''}>
            <span>tenho</span>
            <strong>{number}</strong>
            <b>{unit}</b>
            <p>{copy}</p>
          </article>
        ))}
      </div>
    </section>
  )
}

