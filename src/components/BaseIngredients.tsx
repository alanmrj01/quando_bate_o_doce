const storageAreas = [
  ['geladeira', 'o que já está fresco e acessível'],
  ['armário', 'bases simples que você costuma ter'],
  ['freezer', 'possibilidades para não começar do zero'],
  ['itens rápidos', 'opções que cabem em poucos minutos'],
] as const

export function BaseIngredients() {
  return (
    <section className="ingredients-section section-block" data-reveal>
      <div className="section-heading section-heading--split">
        <div>
          <span className="section-index">11 / lista-base</span>
          <h2>Algumas decisões ficam mais fáceis quando algumas opções já estão em casa</h2>
        </div>
        <p>Uma referência organizacional, sem prescrição nutricional e sem transformar a cozinha em uma lista rígida.</p>
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

