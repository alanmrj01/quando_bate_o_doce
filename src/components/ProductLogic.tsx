const logicBlocks = [
  ['01', 'Começa pela situação', 'Você não precisa saber qual receita procurar.'],
  ['02', 'Filtra pela realidade', 'Tempo, ingrediente disponível e tipo de vontade fazem parte da decisão.'],
  ['03', 'Termina numa escolha possível', 'A finalidade não é inspirar. É ajudar você a escolher.'],
] as const

export function ProductLogic() {
  return (
    <section className="logic-section section-block" data-reveal>
      <div className="section-heading section-heading--center">
        <span className="section-index">06 / prova do mecanismo</span>
        <h2>Não é uma biblioteca para percorrer. São 37 situações que já começam pela dúvida que você realmente tem.</h2>
      </div>
      <div className="logic-steps">
        {logicBlocks.map(([number, title, copy]) => (
          <article key={number}>
            <span>{number}</span>
            <h3>{title}</h3>
            <p>{copy}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
