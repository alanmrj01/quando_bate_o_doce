import { useEffect, useRef, useState } from 'react'
import { emitCheckoutClick, getCheckoutUrl } from '../lib/commerce'
import { trackCtaView } from '../lib/tracking'

type CheckoutButtonProps = {
  label: string
  source: string
  className?: string
}

export function CheckoutButton({ label, source, className = '' }: CheckoutButtonProps) {
  const [message, setMessage] = useState('')
  const checkoutRef = useRef<HTMLAnchorElement>(null)
  const checkoutHref = getCheckoutUrl()

  function handleClick() {
    if (!emitCheckoutClick(source, checkoutHref)) {
      setMessage('Checkout ainda não configurado.')
    }
  }

  useEffect(() => {
    const checkoutElement = checkoutRef.current
    if (!checkoutElement || !('IntersectionObserver' in window)) return

    let continuouslyVisible = false
    let timer: number | undefined

    function clearVisibilityTimer(): void {
      if (timer !== undefined) window.clearTimeout(timer)
      timer = undefined
    }

    const observer = new IntersectionObserver(
      (entries) => {
        const entry = entries.find((candidate) => candidate.target === checkoutElement)
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
          trackCtaView(source)
          observer.disconnect()
        }, 500)
      },
      { threshold: 0.5 },
    )

    observer.observe(checkoutElement)
    return () => {
      clearVisibilityTimer()
      observer.disconnect()
    }
  }, [source])

  return (
    <div className={`checkout-action ${className}`.trim()}>
      <a ref={checkoutRef} className="primary-button" href={checkoutHref ?? undefined} onClick={handleClick}>
        <span>{label}</span>
        <span className="button-arrow" aria-hidden="true">→</span>
      </a>
      <p className="checkout-message" role="status" aria-live="polite">
        {message}
      </p>
    </div>
  )
}
