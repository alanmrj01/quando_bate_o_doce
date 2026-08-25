import { siteConfig } from '../config'
import { CheckoutButton } from './CheckoutButton'

export function FinalCTA() {
  return (
    <section className="final-cta section-block" data-reveal>
      <span className="final-orbit final-orbit--one" aria-hidden="true" />
      <span className="final-orbit final-orbit--two" aria-hidden="true" />
      <div className="final-cta__content">
        <span className="section-index section-index--light">16 / pronto para consultar</span>
        <h2>Na próxima vez que bater vontade de doce, você pode começar pela situação — e encontrar opções fit já organizadas.</h2>
        <p>Tenha o Quando Bate o Doce salvo no celular e consulte opções fit e proteicas em uma das 37 situações sempre que precisar.</p>
        <div className="final-offer">
          <div>
            <strong>{siteConfig.price}</strong>
            <span>{siteConfig.paymentLabel}</span>
          </div>
          <CheckoutButton label="Quero o Quando Bate o Doce" source="final-cta" />
        </div>
      </div>
    </section>
  )
}
