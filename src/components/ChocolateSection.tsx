const chocolateModes = [
  ['cremoso', 'textura macia'],
  ['crocante', 'contraste de textura'],
  ['gelado', 'temperatura também importa'],
  ['rápido', 'para poucos minutos'],
] as const

export function ChocolateSection() {
  return (
    <section className="chocolate-section section-block" data-reveal>
      <div className="chocolate-visual" aria-hidden="true">
        <span className="chocolate-disc chocolate-disc--one" />
        <span className="chocolate-disc chocolate-disc--two" />
        <span className="chocolate-disc chocolate-disc--three" />
        <div className="chocolate-label">
          <small>situação 11</small>
          <strong>É chocolate mesmo.</strong>
        </div>
      </div>

      <div className="chocolate-copy">
        <span className="section-index section-index--light">09 / vontade específica</span>
        <h2>Porque às vezes “coma uma fruta” simplesmente não responde ao que você está querendo</h2>
        <p>O guia não tenta fingir que toda vontade é igual. Se a vontade é de chocolate, a consulta começa reconhecendo isso.</p>
        <div className="chocolate-modes">
          {chocolateModes.map(([mode, note]) => (
            <article key={mode}>
              <span>chocolate +</span>
              <strong>{mode}</strong>
              <small>{note}</small>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}

