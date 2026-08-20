import { deliverables } from '../content'
import { GuideMockup } from './GuideMockup'

export function Deliverables() {
  return (
    <section className="deliverables-section section-block" data-reveal>
      <div className="section-heading section-heading--center">
        <span className="section-index">10 / o que você recebe</span>
        <h2>Tudo organizado para você consultar sem precisar pensar por onde começar</h2>
      </div>

      <div className="deliverables-layout">
        <div className="deliverables-mockup">
          <GuideMockup compact />
          <div className="product-stamp">
            <span>produto digital</span>
            <strong>37 situações</strong>
          </div>
        </div>
        <ol className="deliverables-list">
          {deliverables.map(([number, item]) => (
            <li key={number}>
              <span>{number}</span>
              <strong>{item}</strong>
            </li>
          ))}
        </ol>
      </div>
    </section>
  )
}

