import {
  isCheckoutConfigured,
  isTestCheckoutConfigured,
  siteConfig,
} from './config'

type AnalyticsValue = string | number | boolean | null | undefined
export type AnalyticsPayload = Record<string, AnalyticsValue>

type SectionState = {
  name: string
  enteredAt: number | null
  viewed: boolean
}

declare global {
  interface Window {
    dataLayer?: Array<Record<string, unknown>>
    fbq?: (...args: unknown[]) => void
    __PRATO10X_INTERNAL_TEST__?: boolean
  }
}

const UTM_KEYS = [
  'utm_source',
  'utm_medium',
  'utm_campaign',
  'utm_content',
  'utm_term',
  'utm_id',
] as const

const META_ATTRIBUTION_KEYS = ['fbclid', 'fbp', 'fbc'] as const
const EXTRA_ATTRIBUTION_KEYS = [
  'src',
  'placement',
  'campaign_id',
  'adset_id',
  'ad_id',
] as const

const ATTRIBUTION_KEYS = [
  ...UTM_KEYS,
  ...META_ATTRIBUTION_KEYS,
  ...EXTRA_ATTRIBUTION_KEYS,
] as const

const ATTRIBUTION_STORAGE_KEY = 'prato10x_attribution_v2'
const JOURNEY_STORAGE_KEY = 'prato10x_journey_id'

function readCookie(name: string): string {
  const prefix = `${name}=`
  const entry = document.cookie
    .split(';')
    .map((value) => value.trim())
    .find((value) => value.startsWith(prefix))

  return entry ? decodeURIComponent(entry.slice(prefix.length)) : ''
}

function readStoredAttribution(): Record<string, string> {
  try {
    const raw = window.sessionStorage.getItem(ATTRIBUTION_STORAGE_KEY)
    if (!raw) return {}

    const parsed = JSON.parse(raw) as Record<string, unknown>
    return Object.fromEntries(
      ATTRIBUTION_KEYS.map((key) => [
        key,
        typeof parsed[key] === 'string' ? String(parsed[key]) : '',
      ]),
    )
  } catch {
    return {}
  }
}

function persistAttribution(values: Record<string, string>): void {
  try {
    window.sessionStorage.setItem(
      ATTRIBUTION_STORAGE_KEY,
      JSON.stringify(values),
    )
  } catch {
    // Rastreamento nunca deve bloquear a experiência da landing page.
  }
}

export function isInternalTestMode(): boolean {
  if (typeof window.__PRATO10X_INTERNAL_TEST__ === 'boolean') {
    return window.__PRATO10X_INTERNAL_TEST__
  }

  return new URLSearchParams(window.location.search).get('internal_test') === '1'
}

export function getJourneyId(): string {
  try {
    const existing = window.sessionStorage.getItem(JOURNEY_STORAGE_KEY)
    if (existing) return existing

    const generated = typeof crypto.randomUUID === 'function'
      ? `j_${crypto.randomUUID()}`
      : `j_${Date.now()}_${Math.random().toString(36).slice(2, 12)}`

    window.sessionStorage.setItem(JOURNEY_STORAGE_KEY, generated)
    return generated
  } catch {
    return `j_${Date.now()}_${Math.random().toString(36).slice(2, 12)}`
  }
}

export function getAttributionParameters(): Record<string, string> {
  const params = new URLSearchParams(window.location.search)
  const stored = readStoredAttribution()
  const cookieFbp = readCookie('_fbp')
  const cookieFbc = readCookie('_fbc')

  const values = Object.fromEntries(
    ATTRIBUTION_KEYS.map((key) => {
      const currentValue = params.get(key)?.trim() ?? ''

      if (key === 'fbp') {
        return [key, currentValue || cookieFbp || stored[key] || '']
      }

      if (key === 'fbc') {
        return [key, currentValue || cookieFbc || stored[key] || '']
      }

      return [key, currentValue || stored[key] || '']
    }),
  )

  if (Object.values(values).some(Boolean)) persistAttribution(values)
  return values
}

export function getUtmParameters(): Record<string, string> {
  const attribution = getAttributionParameters()
  return Object.fromEntries(UTM_KEYS.map((key) => [key, attribution[key] || '']))
}

export function trackEvent(
  event: string,
  payload: AnalyticsPayload = {},
): void {
  const internalTest = isInternalTestMode()

  window.dataLayer = window.dataLayer ?? []
  window.dataLayer.push({
    event,
    page_version: siteConfig.pageVersion,
    page_path: window.location.pathname,
    journey_id: getJourneyId(),
    internal_test: internalTest ? '1' : '0',
    ...(internalTest ? { debug_mode: true } : {}),
    ...getAttributionParameters(),
    ...payload,
  })
}

function appendCheckoutTracking(checkoutUrl: URL): void {
  const attribution = getAttributionParameters()

  for (const [key, value] of Object.entries(attribution)) {
    if (value && !checkoutUrl.searchParams.has(key)) {
      checkoutUrl.searchParams.set(key, value)
    }
  }

  if (!checkoutUrl.searchParams.has('s1')) {
    checkoutUrl.searchParams.set('s1', getJourneyId())
  }
}

export function openCheckout(buttonLocation: string): void {
  const internalTest = isInternalTestMode()

  trackEvent('checkout_clicked', {
    button_location: buttonLocation,
    checkout_mode: internalTest ? 'test' : 'production',
  })

  trackEvent('checkout_click', {
    button_location: buttonLocation,
    checkout_provider: 'kiwify',
    checkout_mode: internalTest ? 'test' : 'production',
  })

  /*
   * IMPORTANTE:
   * Não disparamos InitiateCheckout da Meta nesta landing.
   * A Kiwify é a fonte responsável pelo InitiateCheckout quando o checkout
   * realmente carrega. Isso evita contabilizar o clique da landing e a visita
   * ao checkout como dois InitiateCheckout diferentes.
   */

  const checkoutConfigured = internalTest
    ? isTestCheckoutConfigured()
    : isCheckoutConfigured()

  if (!checkoutConfigured) {
    console.warn(
      internalTest
        ? 'Configure o checkout de teste em config.ts.'
        : 'Configure o link definitivo do checkout em config.ts.',
    )
    alert('O checkout ainda não está configurado para esta publicação.')
    return
  }

  const checkoutUrl = new URL(
    internalTest ? siteConfig.testCheckoutUrl : siteConfig.checkoutUrl,
  )

  appendCheckoutTracking(checkoutUrl)

  if (internalTest) {
    checkoutUrl.searchParams.set('src', 'internal_test')
    checkoutUrl.searchParams.set('internal_test', '1')
  }

  window.location.href = checkoutUrl.toString()
}

function secondsSince(startedAt: number): number {
  return Math.max(0, Math.round((performance.now() - startedAt) / 100) / 10)
}

export function initializeBehaviorTracking(): () => void {
  getAttributionParameters()
  getJourneyId()

  if (!('IntersectionObserver' in window)) return () => undefined

  const sectionStates = new Map<HTMLElement, SectionState>()
  const sectionElements = Array.from(
    document.querySelectorAll<HTMLElement>('[data-track-section]'),
  )

  for (const element of sectionElements) {
    sectionStates.set(element, {
      name: element.dataset.trackSection || element.id || 'section',
      enteredAt: null,
      viewed: false,
    })
  }

  function closeSection(element: HTMLElement): void {
    const state = sectionStates.get(element)
    if (!state?.enteredAt) return

    const durationSeconds = secondsSince(state.enteredAt)
    state.enteredAt = null

    if (durationSeconds >= 1) {
      trackEvent('section_time', {
        section_name: state.name,
        duration_seconds: durationSeconds,
      })
    }
  }

  const sectionObserver = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        const element = entry.target as HTMLElement
        const state = sectionStates.get(element)
        if (!state) continue

        if (entry.isIntersecting) {
          if (!state.viewed) {
            state.viewed = true
            trackEvent('section_view', { section_name: state.name })
          }

          if (state.enteredAt === null && document.visibilityState === 'visible') {
            state.enteredAt = performance.now()
          }
        } else {
          closeSection(element)
        }
      }
    },
    { threshold: [0, 0.05, 0.15] },
  )

  sectionElements.forEach((element) => sectionObserver.observe(element))

  const oneShotElements = Array.from(
    document.querySelectorAll<HTMLElement>('[data-track-once]'),
  )
  const firedOneShotEvents = new Set<string>()

  const oneShotObserver = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue

        const element = entry.target as HTMLElement
        const eventName = element.dataset.trackOnce?.trim()
        if (!eventName || firedOneShotEvents.has(eventName)) continue

        firedOneShotEvents.add(eventName)
        trackEvent(eventName)
        oneShotObserver.unobserve(element)
      }
    },
    { threshold: [0.35] },
  )

  oneShotElements.forEach((element) => oneShotObserver.observe(element))

  function handleVisibilityChange(): void {
    if (document.visibilityState === 'hidden') {
      sectionElements.forEach(closeSection)
      return
    }

    for (const [element, state] of sectionStates) {
      const bounds = element.getBoundingClientRect()
      const visible = bounds.bottom > 0 && bounds.top < window.innerHeight
      if (visible && state.enteredAt === null) state.enteredAt = performance.now()
    }
  }

  function flushTracking(): void {
    sectionElements.forEach(closeSection)
  }

  document.addEventListener('visibilitychange', handleVisibilityChange)
  window.addEventListener('pagehide', flushTracking)

  return () => {
    flushTracking()
    sectionObserver.disconnect()
    oneShotObserver.disconnect()
    document.removeEventListener('visibilitychange', handleVisibilityChange)
    window.removeEventListener('pagehide', flushTracking)
  }
}
