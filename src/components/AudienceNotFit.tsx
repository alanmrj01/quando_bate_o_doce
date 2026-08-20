import { audienceNotFit } from '../content'

export function AudienceNotFit() {
  return (
    <section className="audience-not-fit section-block" data-reveal>
      <div className="not-fit-title">
        <span className="section-index">13 / limites claros</span>
        <h2>Não foi criado para transformar alimentação em mais uma lista de proibições</h2>
      </div>
      <div className="not-fit-content">
        <ul>
          {audienceNotFit.map((item) => (
            <li key={item}><span aria-hidden="true">—</span>{item}</li>
          ))}
        </ul>
        <blockquote>“É uma referência prática para ajudar na decisão quando essa vontade aparece.”</blockquote>
      </div>
    </section>
  )
}

