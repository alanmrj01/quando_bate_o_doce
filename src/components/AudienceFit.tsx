import { audienceFit } from '../content'

export function AudienceFit() {
  return (
    <section className="audience-fit section-block" data-reveal>
      <div className="audience-copy">
        <span className="section-index">12 / para quem</span>
        <h2>Faz mais sentido para quem reconhece pelo menos uma dessas situações</h2>
        <p>Não é preciso se identificar com todas. Uma situação recorrente já ajuda a entender o papel do guia.</p>
      </div>
      <ul className="audience-list">
        {audienceFit.map((item, index) => (
          <li key={item}>
            <span>{String(index + 1).padStart(2, '0')}</span>
            <p>{item}</p>
          </li>
        ))}
      </ul>
    </section>
  )
}

