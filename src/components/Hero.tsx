import { siteConfig } from '../config'
import { CheckoutButton } from './CheckoutButton'
import { AppFeatureIcon, HeroAppComposition } from './TopGuideMockups'

const valueItems = [
  { icon: 'coin', title: siteConfig.price, copy: siteConfig.paymentLabel },
  { icon: 'bolt', title: 'Acesso imediato', copy: '' },
  { icon: 'screen', title: 'Consulta pronta', copy: 'sem nova busca' },
  { icon: 'phone', title: 'Uso no celular', copy: 'sempre com você' },
] as const

export function Hero() {
  return (
    <section className="app-fold app-fold--hero section-shell" id="inicio">
      <div className="app-hero-layout">
        <div className="app-hero-copy" data-reveal>
          <h1>
            Quando bate<br />
            a vontade de doce,<br />
            <span>você tem opções fit</span><br />
            <span>sem improvisar</span><br />
            <span>nem sair da dieta.</span>
          </h1>
          <p>
            O QBD organiza 37 situações no celular<br className="app-copy-break" />
            para você não começar outra busca toda vez.
          </p>
        </div>

        <HeroAppComposition />
      </div>

      <div className="app-value-strip" aria-label={`${siteConfig.price}, ${siteConfig.paymentLabel}`} data-reveal>
        {valueItems.map(({ icon, title, copy }) => (
          <span className="app-value-item" key={title}>
            <i aria-hidden="true"><AppFeatureIcon kind={icon} /></i>
            <span>
              <strong>{title}</strong>
              {copy && <small>{copy}</small>}
            </span>
          </span>
        ))}
      </div>

      <div className="app-hero-action" data-reveal>
        <CheckoutButton label="Quero ter isso no meu celular" source="hero" />
        <p><span aria-hidden="true">▢</span> Acesso imediato após a confirmação do pagamento.</p>
      </div>
    </section>
  )
}
