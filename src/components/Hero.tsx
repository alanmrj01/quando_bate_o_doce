import { useEffect, useRef } from 'react'
import { siteConfig } from '../config'
import { CheckoutButton } from './CheckoutButton'
import { GuideMockup } from './GuideMockup'

export function Hero() {
  const visualRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const visual = visualRef.current
    if (!visual) return

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)')
    const coarsePointer = window.matchMedia('(pointer: coarse)')
    if (reduceMotion.matches || coarsePointer.matches) return

    function handlePointerMove(event: PointerEvent) {
      if (!visual) return
      const bounds = visual.getBoundingClientRect()
      const x = (event.clientX - bounds.left) / bounds.width - 0.5
      const y = (event.clientY - bounds.top) / bounds.height - 0.5
      visual.style.setProperty('--parallax-x', `${x * 8}px`)
      visual.style.setProperty('--parallax-y', `${y * 7}px`)
    }

    function resetParallax() {
      visual?.style.setProperty('--parallax-x', '0px')
      visual?.style.setProperty('--parallax-y', '0px')
    }

    visual.addEventListener('pointermove', handlePointerMove)
    visual.addEventListener('pointerleave', resetParallax)
    return () => {
      visual.removeEventListener('pointermove', handlePointerMove)
      visual.removeEventListener('pointerleave', resetParallax)
    }
  }, [])

  return (
    <section className="hero section-shell" id="inicio">
      <div className="hero-copy" data-reveal>
        <div className="eyebrow"><span /> Guia situacional de consulta</div>
        <h1><span className="hero-headline-emphasis">Talvez o melhor</span> momento para decidir o que fazer quando bate a vontade de comer doce seja antes dela aparecer</h1>
        <div className="hero-sweet-visual">
          <img
            src="/hero-chocolate-editorial.png"
            alt="Trufa de chocolate aberta ao lado de pedaços de chocolate escuro"
            width="960"
            height="640"
            loading="eager"
            decoding="async"
          />
        </div>
        <p className="hero-subheadline">
          O Quando Bate o Doce organiza 37 situações reais para você consultar quando a vontade aparece — depois do almoço, no fim da tarde, à noite, quando quer chocolate ou quando tem poucos minutos para decidir.
        </p>

        <div className="hero-offer" aria-label={`${siteConfig.price}, ${siteConfig.paymentLabel}`}>
          <div className="price-lockup">
            <span>acesso completo</span>
            <strong>{siteConfig.price}</strong>
            <small>{siteConfig.paymentLabel}</small>
            <em>37 situações organizadas por menos de R$1 cada</em>
          </div>
          <CheckoutButton label="Quero ter essa experiência no meu celular" source="hero" />
        </div>

        <div className="hero-proof" aria-label="Características do produto">
          <span>37 situações organizadas</span>
          <span>Consulta rápida no celular</span>
          <span>Sem começar outra busca toda vez</span>
        </div>
      </div>

      <div className="hero-visual" ref={visualRef} data-reveal>
        <p className="visual-note visual-note--top">salve no celular</p>
        <GuideMockup />
        <p className="visual-note visual-note--bottom">abra pela situação</p>
      </div>
    </section>
  )
}
