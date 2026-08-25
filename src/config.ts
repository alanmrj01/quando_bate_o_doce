export type QbdMode = 'production' | 'qa'

const environmentConfig = {
  production: {
    metaPixelId: '2073559566628743',
    ga4MeasurementId: 'G-QK9KJ7VF0D',
    checkoutUrl: 'https://pay.kiwify.com.br/C6MsR21',
  },
  qa: {
    metaPixelId: '905563608877431',
    ga4MeasurementId: 'G-S4GL15S2H9',
    checkoutUrl: 'https://pay.kiwify.com.br/4B5VArF',
  },
} as const

export const siteConfig = {
  productName: 'Quando Bate o Doce',
  price: 'R$27',
  paymentLabel: 'pagamento único',
  landingProdUrl: 'https://quando-bate-o-doce.netlify.app/',
  analytics: {
    productId: 'qbd',
    offerId: 'qbd_27',
    price: 27,
    currency: 'BRL',
    landingVersion: 'qbd_tracking_v2',
  },
  environments: environmentConfig,
} as const

export function getTrackingMode(search = window.location.search): QbdMode {
  const query = new URLSearchParams(search)
  // Compatibilidade legada: internal_test=1 é alias temporário do modo QA.
  return query.get('qa') === '1' || query.get('internal_test') === '1' ? 'qa' : 'production'
}

export function getActiveSiteConfig(mode = getTrackingMode()) {
  return siteConfig.environments[mode]
}
