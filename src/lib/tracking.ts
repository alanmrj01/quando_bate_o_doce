import { getActiveSiteConfig, getTrackingMode, siteConfig, type QbdMode } from '../config'
import { getAnalyticsAttribution } from './commerce'

type Fbq = ((...args: unknown[]) => void) & {
  callMethod?: (...args: unknown[]) => void
  loaded: boolean
  push: (...args: unknown[]) => void
  queue: unknown[][]
  version: string
}

type TrackerStatus = 'idle' | 'initializing' | 'initialized'

type TrackerRuntime = {
  status: TrackerStatus
  initialization?: Promise<void>
}

type TrackingRuntime = {
  mode: QbdMode
  meta: TrackerRuntime
  ga4: TrackerRuntime
  behavioralListenersInitialized: boolean
  checkoutListenerInitialized: boolean
  qaDiagnosticsLogged: boolean
}

declare global {
  interface Window {
    __qbdTrackingInitialized?: boolean
    __qbdTrackingState?: TrackingRuntime
    _fbq?: Fbq
    dataLayer?: unknown[]
    fbq?: Fbq
    gtag?: (...args: unknown[]) => void
  }
}

const SCRIPT_LOAD_TIMEOUT_MS = 15_000
const trackedOnce = new Set<string>()
const pendingGa4Events = new Map<string, () => void>()
const externalScriptLoads = new Map<string, Promise<void>>()

function trackOnce(key: string, callback: () => void): boolean {
  if (trackedOnce.has(key)) return false
  callback()
  trackedOnce.add(key)
  return true
}

function logQaEvent(mode: QbdMode, eventName: string): void {
  if (mode === 'qa') console.info(`[QBD QA] event=${eventName}`)
}

function isProductionLanding(): boolean {
  try {
    return window.location.origin === new URL(siteConfig.landingProdUrl).origin
  } catch {
    return false
  }
}

function loadExternalScript(id: string, source: string): Promise<void> {
  const pendingLoad = externalScriptLoads.get(id)
  if (pendingLoad) return pendingLoad

  const existingScript = document.getElementById(id) as HTMLScriptElement | null
  if (existingScript?.dataset.qbdLoaded === 'true') return Promise.resolve()

  const script = existingScript ?? document.createElement('script')
  if (!existingScript) {
    script.id = id
    script.async = true
    script.src = source
  }

  const loadPromise = new Promise<void>((resolve, reject) => {
    let timeout: number | undefined

    function cleanup(): void {
      if (timeout !== undefined) window.clearTimeout(timeout)
      timeout = undefined
      script.removeEventListener('load', handleLoad)
      script.removeEventListener('error', handleError)
      externalScriptLoads.delete(id)
    }

    function handleLoad(): void {
      script.dataset.qbdLoaded = 'true'
      cleanup()
      resolve()
    }

    function failLoad(): void {
      cleanup()
      script.remove()
      reject(new Error(`Unable to load tracking resource: ${id}`))
    }

    function handleError(): void {
      failLoad()
    }

    script.addEventListener('load', handleLoad, { once: true })
    script.addEventListener('error', handleError, { once: true })
    timeout = window.setTimeout(failLoad, SCRIPT_LOAD_TIMEOUT_MS)

  })

  externalScriptLoads.set(id, loadPromise)
  if (!existingScript) document.head.appendChild(script)
  return loadPromise
}

function ensureMetaPixelStub(): Fbq {
  if (!window.fbq) {
    const fbq = ((...args: unknown[]) => {
      if (fbq.callMethod) fbq.callMethod(...args)
      else fbq.queue.push(args)
    }) as Fbq

    fbq.loaded = true
    fbq.version = '2.0'
    fbq.queue = []
    fbq.push = fbq
    window.fbq = fbq
    window._fbq = fbq
  }

  return window.fbq
}

function ensureGa4Stub(): (...args: unknown[]) => void {
  window.dataLayer = window.dataLayer ?? []
  window.gtag =
    window.gtag ??
    function gtag() {
      window.dataLayer?.push(arguments)
    }

  return window.gtag
}

function trackMetaProductView(mode: QbdMode): void {
  const { productId, price, currency } = siteConfig.analytics
  const fbq = window.fbq
  if (!fbq) throw new Error('Meta Pixel is unavailable after script load')

  trackOnce('meta:ViewContent', () => {
    fbq('track', 'ViewContent', {
      content_ids: [productId],
      content_name: siteConfig.productName,
      content_type: 'product',
      value: price,
      currency,
    })
    logQaEvent(mode, 'ViewContent')
  })
}

function trackGa4ProductView(mode: QbdMode): void {
  const { productId, price, currency } = siteConfig.analytics
  const gtag = window.gtag
  if (!gtag) throw new Error('GA4 is unavailable after script load')

  trackOnce('ga4:view_item', () => {
    gtag('event', 'view_item', {
      ...getAnalyticsAttribution(),
      currency,
      value: price,
      items: [
        {
          item_id: productId,
          item_name: siteConfig.productName,
          price,
          quantity: 1,
        },
      ],
    })
    logQaEvent(mode, 'view_item')
  })
}

async function initializeMetaPixel(metaPixelId: string, mode: QbdMode): Promise<void> {
  const fbq = ensureMetaPixelStub()
  await loadExternalScript('qbd-meta-pixel', 'https://connect.facebook.net/en_US/fbevents.js')

  trackOnce(`meta:init:${metaPixelId}`, () => fbq('init', metaPixelId))
  trackOnce('meta:PageView', () => {
    fbq('track', 'PageView')
    logQaEvent(mode, 'PageView')
  })
  trackMetaProductView(mode)
}

async function initializeGa4(ga4MeasurementId: string, mode: QbdMode): Promise<void> {
  const gtag = ensureGa4Stub()
  await loadExternalScript(
    'qbd-ga4',
    `https://www.googletagmanager.com/gtag/js?id=${ga4MeasurementId}`,
  )

  trackOnce(`ga4:config:${ga4MeasurementId}`, () => {
    gtag('js', new Date())
    gtag('config', ga4MeasurementId, getAnalyticsAttribution())
  })
  trackGa4ProductView(mode)
}

function getScrollProgress(): number {
  const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight
  if (scrollableHeight <= 0) return 1
  return Math.min(1, Math.max(0, window.scrollY / scrollableHeight))
}

function setupLandingEngagement(mode: QbdMode): void {
  const requiredVisibleTime = 10_000
  let accumulatedVisibleTime = 0
  let visibleSince = document.visibilityState === 'visible' ? Date.now() : undefined
  let maxScrollProgress = getScrollProgress()
  let timer: number | undefined
  let cleanedUp = false

  function getVisibleTime(now = Date.now()): number {
    if (visibleSince === undefined) return accumulatedVisibleTime
    return accumulatedVisibleTime + Math.max(0, now - visibleSince)
  }

  function clearTimer(): void {
    if (timer !== undefined) window.clearTimeout(timer)
    timer = undefined
  }

  function cleanup(): void {
    if (cleanedUp) return
    cleanedUp = true
    clearTimer()
    window.removeEventListener('scroll', handleScroll)
    window.removeEventListener('pagehide', cleanup)
    document.removeEventListener('visibilitychange', handleVisibilityChange)
  }

  function scheduleVisibleTimeCheck(): void {
    clearTimer()
    if (cleanedUp || visibleSince === undefined) return

    const remainingTime = requiredVisibleTime - getVisibleTime()
    if (remainingTime <= 0) return
    timer = window.setTimeout(() => {
      timer = undefined
      evaluate()
    }, remainingTime)
  }

  function evaluate(): void {
    maxScrollProgress = Math.max(maxScrollProgress, getScrollProgress())
    if (getVisibleTime() < requiredVisibleTime) {
      scheduleVisibleTimeCheck()
      return
    }
    if (maxScrollProgress < 0.25) return

    const tracked = queueOrTrackGa4Once('ga4:landing_engaged', () => {
      window.gtag?.('event', 'landing_engaged', {
        ...getAnalyticsAttribution(),
        product_id: siteConfig.analytics.productId,
        landing_version: siteConfig.analytics.landingVersion,
      })
      logQaEvent(mode, 'landing_engaged')
    })
    if (tracked) cleanup()
  }

  function handleScroll(): void {
    evaluate()
  }

  function handleVisibilityChange(): void {
    const now = Date.now()
    if (document.visibilityState === 'visible') {
      if (visibleSince === undefined) visibleSince = now
      evaluate()
      return
    }

    if (visibleSince !== undefined) {
      accumulatedVisibleTime += Math.max(0, now - visibleSince)
      visibleSince = undefined
    }
    clearTimer()
  }

  scheduleVisibleTimeCheck()
  window.addEventListener('scroll', handleScroll, { passive: true })
  document.addEventListener('visibilitychange', handleVisibilityChange)
  window.addEventListener('pagehide', cleanup, { once: true })
}

function queueOrTrackGa4Once(key: string, callback: () => void): boolean {
  if (trackedOnce.has(key) || pendingGa4Events.has(key)) return true

  const runtime = window.__qbdTrackingState
  if (runtime?.ga4.status === 'initialized' && window.gtag) {
    return trackOnce(key, callback)
  }

  if (!runtime) return false
  pendingGa4Events.set(key, callback)
  return true
}

function flushPendingGa4Events(): void {
  for (const [key, callback] of pendingGa4Events) {
    if (trackOnce(key, callback)) pendingGa4Events.delete(key)
  }
}

function createTrackingRuntime(mode: QbdMode): TrackingRuntime {
  return {
    mode,
    meta: { status: 'idle' },
    ga4: { status: 'idle' },
    behavioralListenersInitialized: false,
    checkoutListenerInitialized: false,
    qaDiagnosticsLogged: false,
  }
}

function updateInitializedFlag(runtime: TrackingRuntime): void {
  window.__qbdTrackingInitialized =
    runtime.meta.status === 'initialized' && runtime.ga4.status === 'initialized'
}

function startTrackerInitialization(
  runtime: TrackingRuntime,
  trackerName: 'Meta' | 'GA4',
  tracker: TrackerRuntime,
  initialize: () => Promise<void>,
  onInitialized?: () => void,
): Promise<void> {
  if (tracker.status === 'initialized') return Promise.resolve()
  if (tracker.status === 'initializing' && tracker.initialization) {
    return tracker.initialization
  }

  tracker.status = 'initializing'
  updateInitializedFlag(runtime)

  const initialization = initialize()
    .then(() => {
      tracker.status = 'initialized'
      onInitialized?.()
    })
    .catch((error: unknown) => {
      tracker.status = 'idle'
      console.warn(`[QBD tracking] ${trackerName} initialization failed; retry is available.`, error)
      throw error
    })
    .finally(() => {
      tracker.initialization = undefined
      updateInitializedFlag(runtime)
    })

  tracker.initialization = initialization
  return initialization
}

function initializeBehavioralListeners(runtime: TrackingRuntime): void {
  if (runtime.behavioralListenersInitialized) return
  runtime.behavioralListenersInitialized = true
  setupLandingEngagement(runtime.mode)
  setupOfferView(runtime.mode)
}

function initializeCheckoutListener(runtime: TrackingRuntime): void {
  if (runtime.checkoutListenerInitialized) return
  runtime.checkoutListenerInitialized = true
  window.addEventListener('qbd:checkout_click', trackCheckoutClick)
}

function logQaConfiguration(runtime: TrackingRuntime): void {
  if (runtime.mode !== 'qa' || runtime.qaDiagnosticsLogged) return
  runtime.qaDiagnosticsLogged = true
  const activeConfig = getActiveSiteConfig(runtime.mode)
  console.info('[QBD QA] mode=qa')
  console.info(`[QBD QA] meta=${activeConfig.metaPixelId}`)
  console.info(`[QBD QA] ga4=${activeConfig.ga4MeasurementId}`)
  console.info(`[QBD QA] checkout=${activeConfig.checkoutUrl}`)
}

function getOrCreateTrackingRuntime(mode: QbdMode): TrackingRuntime | undefined {
  const existingRuntime = window.__qbdTrackingState
  if (existingRuntime) {
    if (existingRuntime.mode !== mode) {
      console.warn('[QBD tracking] Tracking mode cannot change without a page load.')
      return undefined
    }
    return existingRuntime
  }

  const runtime = createTrackingRuntime(mode)
  window.__qbdTrackingState = runtime
  window.__qbdTrackingInitialized = false
  return runtime
}

function retryableTrackingInitialization(runtime: TrackingRuntime): Promise<void> {
  const activeConfig = getActiveSiteConfig(runtime.mode)
  const metaInitialization = startTrackerInitialization(
    runtime,
    'Meta',
    runtime.meta,
    () => initializeMetaPixel(activeConfig.metaPixelId, runtime.mode),
  )
  const ga4Initialization = startTrackerInitialization(
    runtime,
    'GA4',
    runtime.ga4,
    () => initializeGa4(activeConfig.ga4MeasurementId, runtime.mode),
    () => flushPendingGa4Events(),
  )

  return Promise.allSettled([metaInitialization, ga4Initialization]).then(() => undefined)
}

function setupOfferView(mode: QbdMode): void {
  const offerElement = document.getElementById('oferta')
  if (!offerElement || !('IntersectionObserver' in window)) return

  let continuouslyVisible = false
  let timer: number | undefined

  function clearVisibilityTimer(): void {
    if (timer !== undefined) window.clearTimeout(timer)
    timer = undefined
  }

  function cleanup(): void {
    clearVisibilityTimer()
    observer.disconnect()
    window.removeEventListener('pagehide', cleanup)
  }

  const observer = new IntersectionObserver(
    (entries) => {
      const entry = entries.find((candidate) => candidate.target === offerElement)
      if (!entry) return

      continuouslyVisible = entry.isIntersecting && entry.intersectionRatio >= 0.5
      if (!continuouslyVisible) {
        clearVisibilityTimer()
        return
      }

      if (timer !== undefined) return
      timer = window.setTimeout(() => {
        timer = undefined
        if (!continuouslyVisible) return

        const tracked = queueOrTrackGa4Once('ga4:offer_view', () => {
          window.gtag?.('event', 'offer_view', {
            ...getAnalyticsAttribution(),
            product_id: siteConfig.analytics.productId,
            offer_id: siteConfig.analytics.offerId,
            price: siteConfig.analytics.price,
            currency: siteConfig.analytics.currency,
            landing_version: siteConfig.analytics.landingVersion,
          })
          logQaEvent(mode, 'offer_view')
        })
        if (tracked) cleanup()
      }, 1_000)
    },
    { threshold: 0.5 },
  )

  observer.observe(offerElement)
  window.addEventListener('pagehide', cleanup, { once: true })
}

export function trackCtaView(ctaPosition: string): void {
  const runtime = window.__qbdTrackingState
  if (!ctaPosition || !runtime) return

  queueOrTrackGa4Once(`ga4:cta_view:${ctaPosition}`, () => {
    window.gtag?.('event', 'cta_view', {
      ...getAnalyticsAttribution(),
      cta_position: ctaPosition,
      product_id: siteConfig.analytics.productId,
      offer_id: siteConfig.analytics.offerId,
      price: siteConfig.analytics.price,
      currency: siteConfig.analytics.currency,
      landing_version: siteConfig.analytics.landingVersion,
    })
    logQaEvent(runtime.mode, 'cta_view')
  })
}

function trackCheckoutClick(event: Event): void {
  const detail = (event as CustomEvent<{ source?: string }>).detail
  const ctaPosition = detail?.source ?? 'unknown'
  const runtime = window.__qbdTrackingState
  if (!runtime) return

  const mode = runtime.mode
  const attribution = getAnalyticsAttribution()

  if (runtime.ga4.status === 'initialized' && window.gtag) {
    window.gtag('event', 'checkout_click', {
      ...attribution,
      event_category: 'commerce',
      source: ctaPosition,
      cta_position: ctaPosition,
      product_id: siteConfig.analytics.productId,
      offer_id: siteConfig.analytics.offerId,
      price: siteConfig.analytics.price,
      value: siteConfig.analytics.price,
      currency: siteConfig.analytics.currency,
      landing_version: siteConfig.analytics.landingVersion,
    })
    logQaEvent(mode, 'checkout_click')
  }

  if (runtime.meta.status === 'initialized' && window.fbq) {
    window.fbq('trackCustom', 'CheckoutClick', {
      ...(attribution.campaign_id ? { campaign_id: attribution.campaign_id } : {}),
      ...(attribution.adset_id ? { adset_id: attribution.adset_id } : {}),
      ...(attribution.ad_id ? { ad_id: attribution.ad_id } : {}),
      product_id: siteConfig.analytics.productId,
      offer_id: siteConfig.analytics.offerId,
      price: siteConfig.analytics.price,
      value: siteConfig.analytics.price,
      currency: siteConfig.analytics.currency,
      cta_position: ctaPosition,
      landing_version: siteConfig.analytics.landingVersion,
    })
    logQaEvent(mode, 'CheckoutClick')
  }
}

export function initializeTracking(): Promise<void> {
  const mode = getTrackingMode()
  document.documentElement.dataset.qbdMode = mode

  if (!isProductionLanding()) return Promise.resolve()

  const runtime = getOrCreateTrackingRuntime(mode)
  if (!runtime) return Promise.resolve()

  logQaConfiguration(runtime)
  initializeBehavioralListeners(runtime)
  initializeCheckoutListener(runtime)
  return retryableTrackingInitialization(runtime)
}
