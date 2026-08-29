const storageAreas = [
  ['geladeira', 'o que já está fresco e acessível'],
  ['armário', 'bases simples que você costuma ter'],
  ['freezer', 'possibilidades para ter uma opção à mão'],
  ['itens rápidos', 'opções que cabem em poucos minutos'],
] as const

export function BaseIngredients() {
  return (
    <section className="ingredients-section section-block" data-reveal>
      <div className="section-heading section-heading--split">
        <div>
          <span className="section-index">11 / despensa fit essencial</span>
          <h2>O que vale a pena ter sempre por perto para não ficar sem opção quando a vontade aparecer</h2>
        </div>
        <p>Uma lista prática de ingredientes coringa para facilitar opções fit e proteicas, sem prescrição nutricional ou lista rígida.</p>
      </div>

      <div className="pantry-board">
        {storageAreas.map(([area, copy], index) => (
          <article key={area}>
            <span className={`pantry-icon pantry-icon--${index + 1}`} aria-hidden="true" />
            <div>
              <small>organizar por</small>
              <h3>{area}</h3>
              <p>{copy}</p>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}
