const previewPages = [
  ['SITUAÇÃO 04', 'Terminei o almoço e quero alguma coisa doce', 'depois da refeição'],
  ['SITUAÇÃO 11', 'Quero chocolate', 'vontade específica'],
  ['SITUAÇÃO 19', 'Tenho menos de 5 minutos', 'tempo disponível'],
  ['SITUAÇÃO 28', 'É noite e quero beliscar', 'momento do dia'],
] as const

export function ProductPreview() {
  return (
    <section className="preview-section section-block" id="produto" data-reveal>
      <div className="section-heading section-heading--split">
        <div>
          <span className="section-index">04 / por dentro do guia</span>
          <h2>Um guia para abrir quando a vontade aparece — não para deixar esquecido numa pasta.</h2>
        </div>
        <p>Páginas simuladas a partir da estrutura real do produto. O conteúdo completo permanece dentro do guia.</p>
      </div>

      <div className="preview-desk">
        {previewPages.map(([number, title, label], index) => (
          <article className={`pdf-page pdf-page--${index + 1}`} key={number}>
            <header>
              <span>{number}</span>
              <i aria-hidden="true" />
            </header>
            <small>{label}</small>
            <h3>{title}</h3>
            <div className="page-divider" />
            <div className="page-context">
              <span>A situação</span>
              <span>O que importa neste momento</span>
              <span>Opções já filtradas</span>
            </div>
            <footer>QUANDO BATE O DOCE</footer>
          </article>
        ))}
      </div>
    </section>
  )
}
