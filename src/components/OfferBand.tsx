import { siteConfig } from '../config'
import { CheckoutButton } from './CheckoutButton'

export function OfferBand() {
  return (
    <section className="offer-band section-block" id="oferta" data-reveal>
      <div className="offer-band__copy">
        <span>14 / uma resposta pronta para consultar</span>
        <h2>Quando as opções fit já estão organizadas pela situação, a vontade não precisa virar outra busca.</h2>
      </div>
      <div className="offer-band__action">
        <div className="offer-price">
          <strong>{siteConfig.price}</strong>
          <span>{siteConfig.paymentLabel}</span>
        </div>
        <CheckoutButton label="Quero ter minhas opções organizadas" source="offer-band" />
      </div>
    </section>
  )
}
