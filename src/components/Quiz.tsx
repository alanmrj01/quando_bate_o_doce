import { useState } from 'react'
import { quizQuestions } from '../content'
import { CheckoutButton } from './CheckoutButton'

type QuizAnswer = 'sim' | 'nao'

export function Quiz() {
  const [answers, setAnswers] = useState<QuizAnswer[]>([])
  const completed = answers.length === quizQuestions.length
  const currentIndex = Math.min(answers.length, quizQuestions.length - 1)
  const visibleStep = completed ? quizQuestions.length : currentIndex + 1
  const progress = visibleStep / quizQuestions.length

  function answer(value: QuizAnswer) {
    if (completed) return
    setAnswers((current) => [...current, value])
  }

  function restart() {
    setAnswers([])
  }

  return (
    <section className="quiz-section section-block" id="quiz" data-reveal>
      <div className="quiz-copy">
        <span className="section-index">01 / reconhecimento</span>
        <h2>Veja em <span className="quiz-time-highlight">menos de 1 minuto</span> se esse é o tipo de situação que acontece com você</h2>
      </div>

      <div className="quiz-panel">
        <div className="quiz-progress-copy">
          <span>Pergunta {visibleStep} de {quizQuestions.length}</span>
          <small>{Math.round(progress * 100)}%</small>
        </div>
        <div
          className="quiz-progress"
          role="progressbar"
          aria-valuemin={1}
          aria-valuemax={quizQuestions.length}
          aria-valuenow={visibleStep}
          aria-label={`Pergunta ${visibleStep} de ${quizQuestions.length}`}
        >
          <span style={{ transform: `scaleX(${progress})` }} />
        </div>

        {!completed ? (
          <div className="quiz-stage" key={currentIndex}>
            <span className="quiz-number">0{visibleStep}</span>
            <p>{quizQuestions[currentIndex]}</p>
            <div className="quiz-actions" aria-label="Opções de resposta">
              <button type="button" onClick={() => answer('sim')}>Sim</button>
              <button type="button" onClick={() => answer('nao')}>Não</button>
            </div>
          </div>
        ) : (
          <div className="quiz-result" aria-live="polite">
            <span className="result-mark" aria-hidden="true">✓</span>
            <div>
              <h3>O Quando Bate o Doce foi pensado exatamente para situações como essas.</h3>
              <p>Independentemente das respostas, você chegou ao fim sem receber um diagnóstico inventado.</p>
              <CheckoutButton label="Quero ter minhas opções prontas" source="quiz-result" />
              <button className="text-button" type="button" onClick={restart}>Refazer perguntas</button>
            </div>
          </div>
        )}
      </div>
    </section>
  )
}
