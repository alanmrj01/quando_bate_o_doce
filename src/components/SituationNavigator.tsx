import { useState } from 'react'
import { situations } from '../content'

export function SituationNavigator() {
  const [selected, setSelected] = useState<(typeof situations)[number]>('Acabei de almoçar')

  return (
    <section className="navigator-section section-block" id="como-funciona" data-reveal>
      <div className="section-heading section-heading--split">
        <div>
          <span className="section-index">03 / mecanismo</span>
          <h2>Em vez de começar uma pesquisa, comece pela situação.</h2>
        </div>
        <p>O ponto de entrada não é uma receita. É o momento que já está acontecendo.</p>
      </div>

      <div className="navigator-card">
        <div className="navigator-options">
          <span className="navigator-label">O que está acontecendo agora?</span>
          <div className="situation-buttons" aria-label="Escolha uma situação para visualizar o fluxo">
            {situations.map((situation) => (
              <button
                type="button"
                key={situation}
                className={selected === situation ? 'is-selected' : ''}
                aria-pressed={selected === situation}
                onClick={() => setSelected(situation)}
              >
                {situation}
              </button>
            ))}
          </div>
        </div>

        <div className="navigator-result" aria-live="polite">
          <span className="result-kicker">situação selecionada</span>
          <h3>{selected}</h3>
          <p>O guia abre o contexto correspondente e organiza os caminhos que fazem sentido para esse momento.</p>
          <ol className="mechanism-flow" aria-label="Fluxo de consulta">
            <li><span>01</span><b>Situação</b></li>
            <li><span>02</span><b>Contexto</b></li>
            <li><span>03</span><b>Opções</b></li>
            <li><span>04</span><b>Escolha</b></li>
          </ol>
        </div>
      </div>
    </section>
  )
}

