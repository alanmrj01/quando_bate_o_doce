import { situationCategories } from '../content'

export function SituationsGrid() {
  return (
    <section className="situations-section section-block" data-reveal>
      <div className="section-heading section-heading--split">
        <div>
          <span className="section-index">07 / repertório organizado</span>
          <h2>37 situações para encontrar opções fit sem começar outra busca toda vez</h2>
        </div>
        <p>Dentro de cada situação, as opções se organizam por tipo de doce, tempo disponível e realidade da cozinha.</p>
      </div>

      <div className="situation-map">
        {situationCategories.map((category, index) => (
          <article
            className={`situation-tile situation-tile--${(index % 4) + 1}`}
            key={category}
          >
            <span>{String(index + 1).padStart(2, '0')}</span>
            <strong>{category}</strong>
          </article>
        ))}
        <div className="situation-map__more">+ outras situações organizadas dentro do guia.</div>
      </div>
    </section>
  )
}
