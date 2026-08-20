import { siteConfig } from '../config'

const storagePrefix = 'qbd_'
const preservedClickKeys = new Set(['fbclid', 'fbp', 'fbc'])

function isAttributionKey(key: string): boolean {
  return key.startsWith('utm_') || preservedClickKeys.has(key)
}

function safeSessionGet(key: string): string | null {
  try {
    return window.sessionStorage.getItem(`${storagePrefix}${key}`)
  } catch {
    return null
  }
}

function safeSessionSet(key: string, value: string): void {
  try {
    window.sessionStorage.setItem(`${storagePrefix}${key}`, value)
  } catch {
    // A landing continua funcional mesmo quando o storage está indisponível.
  }
}

function createJourneyId(): string {
  if ('randomUUID' in crypto) return crypto.randomUUID()
  return `qbd-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`
}

export function initializeCommerceContext(): void {
  const query = new URLSearchParams(window.location.search)

  if (query.get('internal_test') === '1') {
    safeSessionSet('internal_test', '1')
  }

  query.forEach((value, key) => {
    if (value && isAttributionKey(key)) safeSessionSet(key, value)
  })

  if (!safeSessionGet('journey_id')) {
    safeSessionSet('journey_id', createJourneyId())
  }
}

export function isInternalTest(): boolean {
  return safeSessionGet('internal_test') === '1'
}

function getStoredAttribution(): Array<[string, string]> {
  const entries: Array<[string, string]> = []

  try {
    for (let index = 0; index < window.sessionStorage.length; index += 1) {
      const storageKey = window.sessionStorage.key(index)
      if (!storageKey?.startsWith(storagePrefix)) continue

      const key = storageKey.slice(storagePrefix.length)
      if (!isAttributionKey(key)) continue

      const value = window.sessionStorage.getItem(storageKey)
      if (value) entries.push([key, value])
    }
  } catch {
    // Parâmetros continuam opcionais quando o storage está indisponível.
  }

  return entries
}

export function getCheckoutUrl(): string | null {
  const checkoutBaseUrl = isInternalTest()
    ? siteConfig.checkout.testUrl
    : siteConfig.checkout.productionUrl

  try {
    const url = new URL(checkoutBaseUrl)
    getStoredAttribution().forEach(([key, value]) => {
      if (value && !url.searchParams.has(key)) url.searchParams.set(key, value)
    })

    const journeyId = safeSessionGet('journey_id')
    if (journeyId && !url.searchParams.has('s1')) {
      url.searchParams.set('s1', journeyId)
    }

    if (isInternalTest()) url.searchParams.set('internal_test', '1')
    return url.toString()
  } catch {
    return null
  }
}

export function openCheckout(source: string): boolean {
  const checkoutUrl = getCheckoutUrl()
  window.dispatchEvent(
    new CustomEvent('qbd:checkout_click', {
      detail: { source, configured: Boolean(checkoutUrl), internalTest: isInternalTest() },
    }),
  )

  if (!checkoutUrl) return false
  window.location.assign(checkoutUrl)
  return true
}
