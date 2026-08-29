import { AppFeatureIcon, CategoryAppPhone } from './TopGuideMockups'

const valueCards = [
  ['phone', 'CONSULTA NO CELULAR', 'Abra pela situação quando a vontade aparecer.'],
  ['grid', '37 SITUAÇÕES REAIS', 'Depois do almoço, fim da tarde, à noite e outros momentos.'],
  ['bowl', 'OPÇÕES FIT ORGANIZADAS', 'Receitas low carb, proteicas e saudáveis para cada momento.'],
  ['search', 'SEM OUTRA BUSCA', 'Você abre pela situação e vai direto às opções.'],
] as const

const proofItems = [
  ['grid', 'Momentos reais', 'almoço, tarde, noite e mais'],
  ['bolt', 'Consulta rápida', 'encontre o que combina no momento'],
  ['lock', 'Pagamento único', 'acesso vitalício no seu celular'],
  ['phone', 'No celular', 'sempre com você, onde estiver'],
  ['download', 'Instalação rápida', 'e acesso imediato após o pagamento'],
] as const

export function AppValueSection() {
  return (
    <section className="app-fold app-fold--value section-shell" data-reveal>
      <div className="app-value-main">
        <div className="app-value-copy">
          <h2>
            Não é mais uma busca.<br />
            É um <span>app de consulta rápida</span><br />
            para <span>37 situações reais do dia.</span>
          </h2>
          <p>Tudo organizado para você abrir no celular,<br />escolher sua situação e ver opções fit que<br />combinam com o seu momento.</p>

          <div className="app-value-cards">
            {valueCards.map(([icon, title, copy]) => (
              <article key={title}>
                <i aria-hidden="true"><AppFeatureIcon kind={icon} /></i>
                <div><h3>{title}</h3><p>{copy}</p></div>
              </article>
            ))}
          </div>
        </div>

        <div className="app-value-phone-wrap">
          <CategoryAppPhone className="app-phone--value" />
        </div>
      </div>

      <div className="app-bonus-panel">
        <span className="app-bonus-label">BÔNUS EXCLUSIVOS</span>
        <article>
          <div className="app-notepad" aria-hidden="true">
            <i>✓ Aveia</i><i>✓ Cacau 100%</i><i>✓ Leite vegetal</i><i>✓ Pasta de amendoim</i><i>✓ Eritritol ou xilitol</i>
          </div>
          <div><span>BÔNUS 1</span><h3>Despensa Fit Essencial</h3><p>Uma lista prática do que vale a pena ter em casa para não ficar sem opção quando a vontade aparecer.</p></div>
        </article>
        <article>
          <div><span>BÔNUS 2</span><h3>Modo Emergência — até 2 minutos</h3><p>Atalhos para quando a vontade aparece e você quer escolher rápido, sem começar outra busca.</p></div>
          <div className="app-stopwatch" aria-hidden="true"><span /><i /></div>
        </article>
      </div>

      <div className="app-proof-strip" aria-label="Benefícios do aplicativo">
        {proofItems.map(([icon, title, copy]) => (
          <span key={title}><i aria-hidden="true"><AppFeatureIcon kind={icon} /></i><b>{title}</b><small>{copy}</small></span>
        ))}
      </div>
    </section>
  )
}
