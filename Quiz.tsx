import { useMemo, useRef, useState } from 'react'
import {
  getJourneyId,
  getUtmParameters,
  isInternalTestMode,
  openCheckout,
  trackEvent,
} from './analytics'
import { siteConfig } from './config'
import { ArrowRightIcon, CheckIcon, LockIcon } from './Icons'

type QuizAnswer = 'yes' | 'no'
type SubmitStatus = 'idle' | 'sending' | 'success' | 'error'

type QuizQuestion = {
  id: `q${number}`
  question: string
}

const quizQuestions: QuizQuestion[] = [
  { id: 'q1', question: 'Você busca comer bem, com leveza e de forma prática no dia a dia?' },
  { id: 'q2', question: 'Quando você está comendo menos, decidir o que colocar no prato ainda gera dúvida?' },
  { id: 'q3', question: 'Nos dias corridos, você acaba improvisando mais do que gostaria nas refeições?' },
  { id: 'q4', question: 'Ter uma referência prática para consultar facilitaria suas próximas escolhas?' },
]

export function Quiz() {
  const [answers, setAnswers] = useState<Record<string, QuizAnswer>>({})
  const [status, setStatus] = useState<SubmitStatus>('idle')
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const quizStartedRef = useRef(false)
  const submittedRef = useRef(false)

  const completed = useMemo(
    () => quizQuestions.every((question) => Boolean(answers[question.id])),
    [answers],
  )

  async function submitAnswers(nextAnswers: Record<string, QuizAnswer>) {
    if (submittedRef.current) return
    submittedRef.current = true
    setStatus('sending')

    const nextScore = Object.values(nextAnswers).filter((answer) => answer === 'yes').length
    const internalTest = isInternalTestMode()
    const payload = new URLSearchParams({
      'form-name': siteConfig.quizFormName,
      page_version: siteConfig.pageVersion,
      timestamp: new Date().toISOString(),
      score: String(nextScore),
      internal_test: internalTest ? '1' : '0',
      journey_id: getJourneyId(),
      ...getUtmParameters(),
      ...nextAnswers,
    })

    if (internalTest) {
      setStatus('success')
      trackEvent('quiz_submitted', {
        submit_status: 'test_skipped',
        affirmative_answers: nextScore,
        total_steps: quizQuestions.length,
      })
      return
    }

    try {
      const response = await fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: payload.toString(),
      })

      if (!response.ok) throw new Error(`Netlify form returned ${response.status}`)

      setStatus('success')
      trackEvent('quiz_submitted', {
        submit_status: 'success',
        affirmative_answers: nextScore,
        total_steps: quizQuestions.length,
      })
    } catch (error) {
      console.error('Não foi possível registrar o quiz.', error)
      setStatus('error')
      trackEvent('quiz_submitted', {
        submit_status: 'error',
        affirmative_answers: nextScore,
        total_steps: quizQuestions.length,
      })
    }
  }

  function answerQuestion(id: string, value: QuizAnswer) {
    if (!quizStartedRef.current) {
      quizStartedRef.current = true
      trackEvent('quiz_start', { total_steps: quizQuestions.length })
    }

    const nextAnswers = { ...answers, [id]: value }
    setAnswers(nextAnswers)

    const index = quizQuestions.findIndex((question) => question.id === id)
    trackEvent('quiz_answered', {
      step_number: index + 1,
      total_steps: quizQuestions.length,
      answer_value: value,
    })

    setCurrentQuestionIndex(index < quizQuestions.length - 1 ? index + 1 : quizQuestions.length)

    const nowCompleted = quizQuestions.every((question) => Boolean(nextAnswers[question.id]))
    if (nowCompleted && !submittedRef.current) {
      const score = Object.values(nextAnswers).filter((answer) => answer === 'yes').length
      trackEvent('quiz_complete', {
        total_steps: quizQuestions.length,
        affirmative_answers: score,
      })
      void submitAnswers(nextAnswers)
    }
  }

  const currentQuestion = quizQuestions[currentQuestionIndex]
  const visibleStep = Math.min(currentQuestionIndex + 1, quizQuestions.length)
  const progress = (visibleStep / quizQuestions.length) * 100

  return (
    <section className="quiz-ref" id="quiz" data-track-section="quiz">
      <div className="quiz-ref__panel">
        <h2>Responda e veja se essa experiência é ideal para você viver agora:</h2>

        <div className="quiz-ref__progress">
          <span>Pergunta {visibleStep} de {quizQuestions.length}</span>
          <div
            className="quiz-ref__progress-track"
            role="progressbar"
            aria-valuemin={1}
            aria-valuemax={quizQuestions.length}
            aria-valuenow={visibleStep}
            aria-label={`Pergunta ${visibleStep} de ${quizQuestions.length}`}
          >
            <span style={{ width: `${progress}%` }} />
          </div>
        </div>

        {!completed && currentQuestion && (
          <div className="quiz-ref__stage">
            <article className="quiz-ref__card" key={currentQuestion.id}>
              <span className="quiz-ref__number">{visibleStep}</span>
              <p>{currentQuestion.question}</p>
              <div className="quiz-ref__answers">
                <button type="button" onClick={() => answerQuestion(currentQuestion.id, 'yes')}>
                  Sim
                </button>
                <button type="button" onClick={() => answerQuestion(currentQuestion.id, 'no')}>
                  Não
                </button>
              </div>
            </article>
          </div>
        )}

        {completed && currentQuestionIndex >= quizQuestions.length && (
          <div className="quiz-ref__result" aria-live="polite">
            <span className="quiz-ref__result-icon"><CheckIcon /></span>
            <div>
              <h3>O Prato 10x é a experiência ideal para a sua situação.</h3>
              <button type="button" onClick={() => openCheckout('quiz-result')}>
                Eu quero esta experiência <ArrowRightIcon />
              </button>
              <small className={`quiz-ref__save quiz-ref__save--${status}`}>
                {status === 'sending' && 'Salvando sua resposta anônima…'}
                {status === 'success' && (isInternalTestMode() ? 'Modo teste: resposta não enviada ao formulário comercial.' : 'Resposta anônima registrada.')}
                {status === 'error' && 'Não foi possível registrar agora, mas isso não bloqueia seu acesso.'}
              </small>
            </div>
          </div>
        )}

        <p className="quiz-ref__privacy"><LockIcon /> Respostas anônimas • não é diagnóstico • checkout seguro</p>
      </div>
    </section>
  )
}
