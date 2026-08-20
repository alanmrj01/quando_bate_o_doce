import { useState } from 'react'
import { faqItems } from '../content'

export function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(0)

  return (
    <section className="faq-section section-block" id="faq" data-reveal>
      <div className="faq-intro">
        <span className="section-index">15 / perguntas frequentes</span>
        <h2>Antes de decidir, talvez você queira saber isso</h2>
        <p>Respostas diretas, sem promessas escondidas.</p>
      </div>
      <div className="faq-list">
        {faqItems.map((item, index) => {
          const isOpen = openIndex === index
          const panelId = `faq-panel-${index}`
          const buttonId = `faq-button-${index}`
          return (
            <article className={isOpen ? 'is-open' : ''} key={item.question}>
              <h3>
                <button
                  id={buttonId}
                  type="button"
                  aria-expanded={isOpen}
                  aria-controls={panelId}
                  onClick={() => setOpenIndex(isOpen ? null : index)}
                >
                  <span>{item.question}</span>
                  <b aria-hidden="true">+</b>
                </button>
              </h3>
              <div
                className="faq-answer"
                id={panelId}
                role="region"
                aria-labelledby={buttonId}
                aria-hidden={!isOpen}
              >
                <div>
                  <p>{item.answer}</p>
                </div>
              </div>
            </article>
          )
        })}
      </div>
    </section>
  )
}
