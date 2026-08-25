export function SearchObjection() {
  return (
    <section className="objection-section section-block" data-reveal>
      <div className="objection-copy">
        <span className="section-index">05 / objeção honesta</span>
        <h2>Você poderia pesquisar isso no Google. O problema é justamente precisar pesquisar toda vez.</h2>
        <p>O Quando Bate o Doce não foi criado porque essas informações são impossíveis de encontrar.</p>
        <p>Foi criado porque, quando a vontade aparece, você provavelmente não quer pesquisar vinte receitas fit, comparar ingredientes e produtos, perguntar para uma IA, salvar cinco opções e depois decidir qual delas realmente cabe naquele momento.</p>
      </div>

      <div className="search-comparison" aria-label="Comparação entre busca e curadoria">
        <article className="search-side">
          <span>BUSCA</span>
          <ol>
            <li>abrir opções</li>
            <li>comparar</li>
            <li>filtrar</li>
            <li>decidir</li>
          </ol>
        </article>
        <span className="comparison-versus">versus</span>
        <article className="curation-side">
          <span>CURADORIA</span>
          <strong>Abrir pela situação</strong>
          <p>A informação já existe. O valor está em encontrar opções fit e proteicas filtradas, organizadas e prontas para consulta.</p>
        </article>
      </div>
    </section>
  )
}
