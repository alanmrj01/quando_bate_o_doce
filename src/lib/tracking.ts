import { siteConfig } from '../config'
import { isInternalTest } from './commerce'

type Fbq = ((...args: unknown[]) => void) & {
  callMethod?: (...args: unknown[]) => void
  loaded: boolean
  push: (...args: unknown[]) => void
  queue: unknown[][]
  version: string
}

declare global {
  interface Window {
    __qbdTrackingInitialized?: boolean
    _fbq?: Fbq
    dataLayer?: unknown[]
    fbq?: Fbq
    gtag?: (...args: unknown[]) => void
  }
}

function isProductionLanding(): boolean {
  try {
    return window.location.origin === new URL(siteConfig.landingProdUrl).origin
  } catch {
    return false
  }
}

function loadExternalScript(id: string, source: string): void {
  if (document.getElementById(id)) return

  const script = document.createElement('script')
  script.id = id
  script.async = true
  script.src = source
  document.head.appendChild(script)
}

function initializeMetaPixel(): void {
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

  loadExternalScript('qbd-meta-pixel', 'https://connect.facebook.net/en_US/fbevents.js')
  window.fbq('init', siteConfig.tracking.metaPixelId)
  window.fbq('track', 'PageView')
}

function initializeGa4(): void {
  window.dataLayer = window.dataLayer ?? []
  window.gtag =
    window.gtag ??
    function gtag() {
      window.dataLayer?.push(arguments)
    }

  loadExternalScript(
    'qbd-ga4',
    `https://www.googletagmanager.com/gtag/js?id=${siteConfig.tracking.ga4MeasurementId}`,
  )
  window.gtag('js', new Date())
  window.gtag('config', siteConfig.tracking.ga4MeasurementId)
}

function trackCheckoutClick(event: Event): void {
  const detail = (event as CustomEvent<{ source?: string }>).detail
  window.gtag?.('event', 'checkout_click', {
    event_category: 'commerce',
    source: detail?.source ?? 'unknown',
  })
}

export function initializeTracking(): void {
  if (window.__qbdTrackingInitialized || isInternalTest() || !isProductionLanding()) return

  window.__qbdTrackingInitialized = true
  initializeMetaPixel()
  initializeGa4()
  window.addEventListener('qbd:checkout_click', trackCheckoutClick)
}
