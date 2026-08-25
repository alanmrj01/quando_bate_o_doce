import { useEffect } from 'react'
import { AudienceFit } from './components/AudienceFit'
import { AudienceNotFit } from './components/AudienceNotFit'
import { BaseIngredients } from './components/BaseIngredients'
import { ChocolateSection } from './components/ChocolateSection'
import { Deliverables } from './components/Deliverables'
import { FAQ } from './components/FAQ'
import { FinalCTA } from './components/FinalCTA'
import { Hero } from './components/Hero'
import { OfferBand } from './components/OfferBand'
import { PremiseSection } from './components/PremiseSection'
import { ProductLogic } from './components/ProductLogic'
import { ProductPreview } from './components/ProductPreview'
import { QuickTimeSection } from './components/QuickTimeSection'
import { Quiz } from './components/Quiz'
import { SearchObjection } from './components/SearchObjection'
import { SectionCheckoutCta } from './components/SectionCheckoutCta'
import { SituationNavigator } from './components/SituationNavigator'
import { SituationsGrid } from './components/SituationsGrid'
import { useReveal } from './hooks/useReveal'
import { initializeTracking } from './lib/tracking'

export default function App() {
  useReveal()

  useEffect(() => {
    initializeTracking()
  }, [])

  return (
    <div className="site-shell">
      <header className="topbar" aria-label="Cabeçalho">
        <a className="wordmark" href="#inicio" aria-label="Quando Bate o Doce — início">
          <span className="apple-mark" aria-hidden="true" />
          <b>QUANDO BATE<br />O DOCE</b>
        </a>
        <a className="topbar-link" href="#produto">ver o guia <span aria-hidden="true">↓</span></a>
      </header>

      <main>
        <Hero />
        <Quiz />
        <PremiseSection />
        <SituationNavigator />
        <SectionCheckoutCta label="Quero ter minhas opções organizadas" source="after-how-it-works" />
        <ProductPreview />
        <SearchObjection />
        <ProductLogic />
        <SectionCheckoutCta label="Quero acessar as 37 situações" source="after-product-demo" />
        <SituationsGrid />
        <QuickTimeSection />
        <ChocolateSection />
        <SectionCheckoutCta label="Quero ter esse guia no celular" source="after-situations" />
        <Deliverables />
        <BaseIngredients />
        <SectionCheckoutCta label="Quero o Quando Bate o Doce" source="after-ingredients" />
        <AudienceFit />
        <AudienceNotFit />
        <OfferBand />
        <FAQ />
        <FinalCTA />
      </main>

      <footer className="site-footer">
        <div className="wordmark wordmark--footer"><span aria-hidden="true" /><b>QUANDO BATE<br />O DOCE</b></div>
        <p>Material digital educativo, organizacional, culinário e de consulta. Não substitui acompanhamento profissional.</p>
        <span>© {new Date().getFullYear()} Quando Bate o Doce</span>
      </footer>
    </div>
  )
}
