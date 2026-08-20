export const siteConfig = {
  productName: 'Quando Bate o Doce',
  price: 'R$27',
  paymentLabel: 'pagamento único',
  landingProdUrl: 'https://quando-bate-o-doce.netlify.app/',
  checkout: {
    productionUrl: 'https://pay.kiwify.com.br/C6MsR21',
    testUrl: 'https://pay.kiwify.com.br/4B5VArF',
  },
  tracking: {
    metaPixelId: '2073559566628743',
    ga4MeasurementId: 'G-QK9KJ7VF0D',
  },
} as const
