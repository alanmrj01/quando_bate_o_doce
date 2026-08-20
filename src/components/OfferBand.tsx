import { siteConfig } from '../config'
import { CheckoutButton } from './CheckoutButton'

export function OfferBand() {
  return (
    <section className="offer-band section-block" id="oferta" data-reveal>
      <div className="offer-band__copy">
        <span>14 / uma resposta pronta para consultar</span>
        <h2>Quando algumas respostas já estão prontas, a vontade não precisa começar uma nova pesquisa.</h2>
      </div>
      <div className="offer-band__action">
        <div className="offer-price">
          <strong>{siteConfig.price}</strong>
          <span>{siteConfig.paymentLabel}</span>
        </div>
        <CheckoutButton label="Quero ter minhas opções prontas" source="offer-band" />
      </div>
    </section>
  )
}

