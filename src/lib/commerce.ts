import { getActiveSiteConfig, getTrackingMode } from '../config'

const storagePrefix = 'qbd_'
const attributionKeys = [
  'src',
  'utm_source',
  'utm_medium',
  'utm_campaign',
  'utm_term',
  'utm_content',
  's1',
  's2',
  's3',
  'fbclid',
] as const
const attributionKeySet = new Set<string>(attributionKeys)
const metaSourceValues = new Set(['meta', 'facebook', 'instagram', 'fb', 'ig'])

type AttributionKey = (typeof attributionKeys)[number]

export type AnalyticsAttribution = Partial<{
  utm_source: string
  utm_medium: string
  utm_campaign: string
  utm_term: string
  utm_content: string
  campaign_id: string
  adset_id: string
  ad_id: string
  journey_id: string
}>

function isAttributionKey(key: string): key is AttributionKey {
  return attributionKeySet.has(key)
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

function safeSessionRemove(key: string): void {
  try {
    window.sessionStorage.removeItem(`${storagePrefix}${key}`)
  } catch {
    // O modo continua sendo definido somente pela URL quando o storage está indisponível.
  }
}

function createJourneyId(): string {
  if ('randomUUID' in crypto) return crypto.randomUUID()
  return `qbd-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`
}

function isInternalJourneyId(value: string): boolean {
  return (
    /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value) ||
    /^qbd-\d+-[a-z0-9]+$/i.test(value)
  )
}

function migrateLegacyJourneyId(): void {
  const legacyS1 = safeSessionGet('s1')
  if (!legacyS1 || !isInternalJourneyId(legacyS1)) return

  if (!safeSessionGet('journey_id')) safeSessionSet('journey_id', legacyS1)
  safeSessionRemove('s1')
}

function getCurrentMetaSource(query: URLSearchParams): string | null {
  const source = query.get('utm_source') ?? query.get('site_source_name')
  return source && metaSourceValues.has(source.trim().toLowerCase()) ? 'meta' : null
}

export function initializeCommerceContext(): void {
  const query = new URLSearchParams(window.location.search)
  safeSessionRemove('internal_test')
  safeSessionRemove('fbp')
  safeSessionRemove('fbc')
  migrateLegacyJourneyId()

  query.forEach((value, key) => {
    if (!value || !isAttributionKey(key)) return

    if (key === 's1' && isInternalJourneyId(value)) {
      if (!safeSessionGet('journey_id')) safeSessionSet('journey_id', value)
      safeSessionRemove('s1')
      return
    }

    safeSessionSet(key, value)
  })

  const explicitSrc = query.get('src')
  if (!explicitSrc) {
    const normalizedMetaSource = getCurrentMetaSource(query)
    if (normalizedMetaSource) safeSessionSet('src', normalizedMetaSource)
  }

  if (!safeSessionGet('journey_id')) {
    safeSessionSet('journey_id', createJourneyId())
  }
}

function getStoredAttribution(): Array<[AttributionKey, string]> {
  return attributionKeys.flatMap((key) => {
    const value = safeSessionGet(key)
    if (!value || (key === 's1' && isInternalJourneyId(value))) return []
    return [[key, value]]
  })
}

export function getAnalyticsAttribution(): AnalyticsAttribution {
  const storedAttribution = new Map(getStoredAttribution())
  const attribution: AnalyticsAttribution = {}
  const directKeys = [
    'utm_source',
    'utm_medium',
    'utm_campaign',
    'utm_term',
    'utm_content',
  ] as const

  directKeys.forEach((key) => {
    const value = storedAttribution.get(key)
    if (value) attribution[key] = value
  })

  const campaignId = storedAttribution.get('s1')
  const adsetId = storedAttribution.get('s2')
  const adId = storedAttribution.get('s3')
  const journeyId = safeSessionGet('journey_id')
  if (campaignId) attribution.campaign_id = campaignId
  if (adsetId) attribution.adset_id = adsetId
  if (adId) attribution.ad_id = adId
  if (journeyId) attribution.journey_id = journeyId

  return attribution
}

export function getCheckoutUrl(): string | null {
  const checkoutBaseUrl = getActiveSiteConfig(getTrackingMode()).checkoutUrl

  try {
    const url = new URL(checkoutBaseUrl)
    getStoredAttribution().forEach(([key, value]) => {
      if (value && !url.searchParams.has(key)) url.searchParams.set(key, value)
    })

    const journeyId = safeSessionGet('journey_id')
    if (journeyId && !url.searchParams.has('sck')) {
      url.searchParams.set('sck', journeyId)
    }

    return url.toString()
  } catch {
    return null
  }
}

export function emitCheckoutClick(source: string, configured: boolean): void {
  window.dispatchEvent(
    new CustomEvent('qbd:checkout_click', {
      detail: {
        source,
        configured,
        internalTest: getTrackingMode() === 'qa',
      },
    }),
  )
}
