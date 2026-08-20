import { useState } from 'react'
import { openCheckout } from '../lib/commerce'

type CheckoutButtonProps = {
  label: string
  source: string
  className?: string
}

export function CheckoutButton({ label, source, className = '' }: CheckoutButtonProps) {
  const [message, setMessage] = useState('')

  function handleClick() {
    const opened = openCheckout(source)
    if (!opened) setMessage('Checkout ainda não configurado.')
  }

  return (
    <div className={`checkout-action ${className}`.trim()}>
      <button className="primary-button" type="button" onClick={handleClick}>
        <span>{label}</span>
        <span className="button-arrow" aria-hidden="true">→</span>
      </button>
      <p className="checkout-message" role="status" aria-live="polite">
        {message}
      </p>
    </div>
  )
}

