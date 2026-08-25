import { CheckoutButton } from './CheckoutButton'

type SectionCheckoutCtaProps = {
  label: string
  source: string
}

export function SectionCheckoutCta({ label, source }: SectionCheckoutCtaProps) {
  return (
    <div className="section-checkout-cta section-shell" data-reveal>
      <CheckoutButton label={label} source={source} />
    </div>
  )
}
