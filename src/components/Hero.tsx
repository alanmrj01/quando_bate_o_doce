import { siteConfig } from '../config'
import { CheckoutButton } from './CheckoutButton'
import { HeroAppComposition } from './TopGuideMockups'

const valueItems = [
  { icon: '◉', title: siteConfig.price, copy: siteConfig.paymentLabel },
  { icon: 'ϟ', title: 'Acesso imediato', copy: '' },
  { icon: '▣', title: '100% digital', copy: 'sem frete' },
  { icon: '▯', title: 'Uso no celular', copy: 'sempre com você' },
] as const

export function Hero() {
  return (
    <section className="app-fold app-fold--hero section-shell" id="inicio">
      <div className="app-hero-layout">
        <div className="app-hero-copy" data-reveal>
          <h1>
            Quando bate<br />
            a vontade de doce,<br />
            <span>você abre o app e</span><br />
            <span>encontra opções fit</span><br />
            <span>para aquele momento.</span>
          </h1>
          <p>
            Instale no seu celular e tenha 37 situações<br className="app-copy-break" />
            reais do dia para não procurar do zero.
          </p>
        </div>

        <HeroAppComposition />
      </div>

      <div className="app-value-strip" aria-label={`${siteConfig.price}, ${siteConfig.paymentLabel}`} data-reveal>
        {valueItems.map(({ icon, title, copy }) => (
          <span className="app-value-item" key={title}>
            <i aria-hidden="true">{icon}</i>
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
