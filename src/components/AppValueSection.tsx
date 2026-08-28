import { CategoryAppPhone } from './TopGuideMockups'

const valueCards = [
  ['▣', 'APP NO CELULAR', 'nada de PDF para baixar. Acesso rápido, sempre que precisar.'],
  ['▦', '37 SITUAÇÕES REAIS', 'do café da manhã à vontade noturna. Para o dia a dia de verdade.'],
  ['♨', 'OPÇÕES FIT ORGANIZADAS', 'Receitas low carb, proteicas e saudáveis para cada momento.'],
  ['ϟ', 'CONSULTA RÁPIDA', 'Encontre o que precisa em poucos toques, sem enrolação.'],
] as const

const proofItems = [
  ['☆', '37 situações', 'para cobrir sempre que precisar'],
  ['ϟ', 'Consulta rápida', 'encontre o que combina no momento'],
  ['▣', 'Pagamento único', 'acesso vitalício no seu celular'],
  ['▯', 'No celular', 'sempre com você, onde estiver'],
  ['⇩', 'Instalação rápida', 'e acesso imediato após o pagamento'],
] as const

export function AppValueSection() {
  return (
    <section className="app-fold app-fold--value section-shell" data-reveal>
      <div className="app-value-main">
        <div className="app-value-copy">
          <h2>
            Não é um PDF solto.<br />
            É um <span>app de consulta rápida</span><br />
            para <span>37 situações reais do dia.</span>
          </h2>
          <p>Tudo organizado para você abrir no celular,<br />escolher sua situação e ver opções fit que<br />combinam com o seu momento.</p>

          <div className="app-value-cards">
            {valueCards.map(([icon, title, copy]) => (
              <article key={title}>
                <i aria-hidden="true">{icon}</i>
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
          <div><span>BÔNUS 1</span><h3>Lista-base do doce fit</h3><p>Ingredientes coringa para você ter sempre por perto e montar opções rápidas sem ficar sem saída.</p></div>
        </article>
        <article>
          <div><span>BÔNUS 2</span><h3>Modo emergência</h3><p>Atalhos para quando a vontade bate forte e você quer resolver em até 2 minutos, sem pensar demais e sem sair da dieta.</p></div>
          <div className="app-stopwatch" aria-hidden="true"><span /><i /></div>
        </article>
      </div>

      <div className="app-proof-strip" aria-label="Benefícios do aplicativo">
        {proofItems.map(([icon, title, copy]) => (
          <span key={title}><i aria-hidden="true">{icon}</i><b>{title}</b><small>{copy}</small></span>
        ))}
      </div>

      <img className="app-value-food app-value-food--left" src="/guide-food-icons/brigadeiro-fit.png" alt="" width="192" height="192" loading="lazy" decoding="async" aria-hidden="true" />
      <img className="app-value-food app-value-food--right" src="/guide-food-icons/brigadeiro-fit.png" alt="" width="192" height="192" loading="lazy" decoding="async" aria-hidden="true" />
    </section>
  )
}
