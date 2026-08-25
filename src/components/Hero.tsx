import { siteConfig } from '../config'
import { CheckoutButton } from './CheckoutButton'
import { HeroGuideMockup, SituationGuideMockup } from './TopGuideMockups'

const benefits = [
  {
    label: '37 situações organizadas',
    icon: (
      <svg viewBox="0 0 32 32" aria-hidden="true">
        <path d="M8 6h16v20H8zM12 11h8M12 16h8M12 21h5" />
      </svg>
    ),
  },
  {
    label: 'Consulta rápida no celular',
    icon: (
      <svg viewBox="0 0 32 32" aria-hidden="true">
        <rect x="9" y="4" width="14" height="24" rx="4" />
        <path d="M13 8h6M14 24h4" />
      </svg>
    ),
  },
  {
    label: 'Sem começar outra busca toda vez',
    icon: (
      <svg viewBox="0 0 32 32" aria-hidden="true">
        <circle cx="14" cy="14" r="8" />
        <path d="m20 20 6 6M7 25 25 7" />
      </svg>
    ),
  },
] as const

export function Hero() {
  return (
    <section className="hero hero-editorial section-shell" id="inicio">
      <div className="hero-first-fold">
        <div className="hero-intro" data-reveal>
          <span className="hero-preheadline">CHEGA DE FUGIR DA DIETA</span>
          <h1>
            Quando bate a <span className="hero-accent hero-accent--short">vontade</span> de doce, você tem um{' '}
            <span className="hero-accent hero-accent--long">guia de opções fit</span> para aquele momento.
          </h1>
        </div>

        <div className="hero-product-stage" data-reveal>
          <HeroGuideMockup />
        </div>

        <p className="hero-editorial-subheadline" data-reveal>
          37 situações do dia com opções de <strong>doces proteicos e fit</strong> organizadas para você consultar no celular sem precisar começar outra busca toda vez.
        </p>
      </div>

      <div className="hero-commerce" aria-label={`${siteConfig.price}, ${siteConfig.paymentLabel}`} data-reveal>
        <div className="hero-commerce__price">
          <span>ACESSO COMPLETO</span>
          <div>
            <strong>{siteConfig.price}</strong>
            <small>{siteConfig.paymentLabel}</small>
          </div>
          <em>37 situações organizadas por menos de R$1 cada</em>
        </div>
        <div className="hero-commerce__action">
          <CheckoutButton label="Quero ter esse guia no celular" source="hero" />
          <p>
            <span>Acesso imediato</span>
            <i aria-hidden="true">•</i>
            <span>100% digital</span>
            <i aria-hidden="true">•</i>
            <span>Seguro</span>
          </p>
        </div>
      </div>

      <div className="hero-second-fold">
        <div className="hero-benefits" aria-label="Características do guia" data-reveal>
          {benefits.map(({ label, icon }) => (
            <span className="hero-benefit" key={label}>
              <i>{icon}</i>
              <b>{label}</b>
            </span>
          ))}
        </div>

        <article className="situation-guide-card" data-reveal>
          <div className="situation-guide-card__copy">
            <span className="situation-guide-card__label">GUIA SITUACIONAL DE CONSULTA</span>
            <h2>
              Você <span>abre pela situação</span> e encontra opções fit para aquele momento.
            </h2>
            <p>
              Em vez de procurar do zero, o guia organiza doces proteicos e opções fit para situações reais do dia — como depois do almoço, no fim da tarde, à noite ou quando bate vontade de chocolate.
            </p>
            <span className="editorial-note editorial-note--open">abra pela situação</span>
          </div>

          <div className="situation-guide-card__visual">
            <span className="editorial-note editorial-note--save">salve no celular</span>
            <SituationGuideMockup />
            <span className="editorial-note editorial-note--fit">opções fit e proteicas</span>
          </div>
        </article>
      </div>
    </section>
  )
}
