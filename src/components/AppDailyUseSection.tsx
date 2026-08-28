import { siteConfig } from '../config'
import { CheckoutButton } from './CheckoutButton'
import { AppFeatureIcon, BrandAppPhone, SituationAppPhone } from './TopGuideMockups'

const dailySteps = [
  ['1', 'tap', 'Abre pela situação'],
  ['2', 'grid', 'Escolhe a categoria'],
  ['3', 'check', 'Vê a opção ideal para o momento'],
] as const

export function AppDailyUseSection() {
  return (
    <section className="app-fold app-fold--daily section-shell" data-reveal>
      <div className="app-daily-main">
        <div className="app-daily-copy">
          <h2>Para o dia a dia.<br /><span>Feito para usar de verdade.</span></h2>
          <p>Quando bate a vontade de doce,<br />você não precisa fugir da dieta.<br />Abre o app, escolhe sua situação<br />e encontra opções práticas,<br />deliciosas e que funcionam.</p>
          <div className="app-daily-steps" aria-label="Fluxo de uso do aplicativo">
            {dailySteps.map(([number, icon, label]) => (
              <article key={number}>
                <span>{number}</span>
                <i aria-hidden="true"><AppFeatureIcon kind={icon} /></i>
                <b>{label}</b>
              </article>
            ))}
          </div>
          <div className="app-daily-note"><span aria-hidden="true"><AppFeatureIcon kind="refresh" /></span><p><strong>Rápido, prático e na palma da mão.</strong><br />Para você seguir firme, sem abrir mão do doce.</p></div>
        </div>

        <div className="app-daily-phones">
          <SituationAppPhone className="app-phone--daily-situations" />
          <BrandAppPhone className="app-phone--daily-brand" />
        </div>
      </div>

      <div className="app-daily-offer">
        <div><span>◉</span><strong>{siteConfig.price}</strong><small>• {siteConfig.paymentLabel}</small></div>
        <CheckoutButton label="Quero ter isso no meu celular" source="app-daily-use" />
        <p><span aria-hidden="true">▢</span> Acesso imediato após a confirmação do pagamento.</p>
      </div>
    </section>
  )
}
