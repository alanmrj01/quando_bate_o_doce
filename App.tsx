import { useEffect } from 'react'
import {
  BowlIcon,
  CheckIcon,
  ClockIcon,
  GridIcon,
  LeafIcon,
  LockIcon,
  TargetIcon,
} from './Icons'
import { Quiz } from './Quiz'
import {
  initializeBehaviorTracking,
  isInternalTestMode,
  openCheckout,
} from './analytics'
import './styles.css'

const toolCards = [
  {
    image: '/tool-plan.jpg',
    title: 'Planejamento prático',
    copy: 'Referências prontas para a rotina, sem transformar cada refeição em um novo problema.',
    icon: GridIcon,
  },
  {
    image: '/tool-direction.jpg',
    title: 'Direção sem esforço',
    copy: 'Uma lógica visual para consultar e adaptar ao que faz sentido no seu dia.',
    icon: TargetIcon,
  },
  {
    image: '/tool-light.jpg',
    title: 'Viver com leveza',
    copy: 'Flexibilidade para decidir com mais clareza sem abrir mão da sua rotina.',
    icon: CheckIcon,
  },
]

const progressionDays = [
  { day: 'Dia 1', image: '/tool-plan.jpg', text: 'Comece com leveza e simplicidade.', locked: false },
  { day: 'Dia 2', image: '/tool-direction.jpg', text: 'Aprofunde suas escolhas todos os dias.', locked: false },
  { day: 'Dia 3', text: 'Conteúdo novo todos os dias.', locked: true },
  { day: 'Dia 4', text: 'Mais clareza para decidir melhor.', locked: true },
  { day: 'Dia 5', text: 'Praticidade que cabe na sua rotina.', locked: true },
  { day: '... até o 37', text: 'Constância que gera resultados.', locked: true },
]

const topicItems = [
  'Prioridade no prato',
  'Refeições menores',
  'Combinações possíveis',
  'Trocas inteligentes',
  'Equilíbrio entre os elementos do prato',
  'Variedade sem complicação',
  'Opções para dias corridos',
  'Clareza para decidir',
  'Adaptação à sua rotina',
  'Planejamento leve',
  'Consistência sem rigidez',
  'Autonomia nas próximas refeições',
]

const experiencePhases = [
  {
    days: 'Dias 1–7',
    title: 'Entender a lógica',
    copy: 'Você começa reconhecendo prioridades, funções e combinações para deixar de olhar o prato apenas como uma lista de alimentos.',
  },
  {
    days: 'Dias 8–21',
    title: 'Levar para a rotina',
    copy: 'As referências começam a ser usadas em situações reais: refeições menores, dias corridos e escolhas feitas com o que está disponível.',
  },
  {
    days: 'Dias 22–37',
    title: 'Ganhar autonomia',
    copy: 'A lógica passa a servir como referência para variar, adaptar e decidir sem precisar começar do zero a cada refeição.',
  },
]

const audienceItems = [
  'está comendo menos e percebeu que escolher ficou mais importante;',
  'ainda improvisa parte das refeições;',
  'quer uma referência prática sem seguir um cardápio engessado;',
  'quer adaptar escolhas ao que já existe em casa;',
  'prefere clareza a uma lista interminável de regras;',
  'quer consultar algo rapidamente no celular.',
]

const faqItems = [
  {
    question: 'O que é o Prato 10x?',
    answer: 'É uma ferramenta digital de decisão para organizar refeições menores com referências, combinações e uma experiência prática de 37 dias.',
  },
  {
    question: 'É um livro de receitas?',
    answer: 'Não. Receitas podem aparecer como referência, mas o centro do Prato 10x é ensinar uma lógica para escolher, combinar e adaptar.',
  },
  {
    question: 'O que eu recebo ao comprar?',
    answer: 'Você recebe acesso digital aos materiais, referências visuais, ferramentas práticas e ao plano de progressão de 37 dias.',
  },
  {
    question: 'Preciso seguir os 37 dias de forma rígida?',
    answer: 'Não. Existe uma progressão para facilitar a aplicação, mas a proposta é servir à sua rotina, não transformar sua alimentação em um calendário engessado.',
  },
  {
    question: 'Serve para quem está comendo menos?',
    answer: 'Foi pensado especialmente para situações em que existe menos espaço no prato e, por isso, escolher o que colocar nele ganhou mais importância.',
  },
  {
    question: 'Consigo usar pelo celular?',
    answer: 'Sim. A experiência foi pensada para consulta prática em dispositivos móveis.',
  },
  {
    question: 'O acesso é imediato?',
    answer: 'Sim. Após a confirmação da compra, o acesso ao produto digital é liberado conforme o fluxo do checkout.',
  },
  {
    question: 'Isso substitui nutricionista ou acompanhamento profissional?',
    answer: 'Não. O Prato 10x é um material educativo e de organização prática. Não substitui avaliação, diagnóstico, prescrição ou acompanhamento profissional.',
  },
]

export default function App() {
  useEffect(() => initializeBehaviorTracking(), [])
  const internalTest = isInternalTestMode()

  return (
    <div className="page-shell">
      {internalTest && (
        <div className="internal-test-banner" role="status">
          MODO TESTE • Meta Pixel bloqueado • checkout de teste ativo
        </div>
      )}

      <main>
        <section className="hero-ref" id="top" data-track-section="hero">
          <div className="hero-ref__copy">
            <h1>
              <span className="hero-ref__highlight">Se você</span> está comendo menos,{' '}
              <span className="hero-ref__highlight">saber</span> o que colocar no prato se tornou ainda mais importante.
            </h1>

            <p className="hero-ref__subheadline">37 Dias de experiência sem escolher no improviso</p>

            <div className="hero-ref__offer" id="preco" data-track-once="price_view">
              <strong>R$37</strong>
              <span>em até 12x de R$ 4,17<br />ou à vista no pix</span>
              <button type="button" onClick={() => openCheckout('hero')}>
                Quero começar por R$1 ao dia <LeafIcon />
              </button>
            </div>
          </div>

          <div className="hero-ref__visual" aria-label="Prato 10x em uso durante uma refeição">
            <img
              src="/hero-person.webp"
              alt="Mulher consultando o Prato 10x em uma refeição menor, com tablet e material visual ao lado"
              width="900"
              height="1108"
              fetchPriority="high"
            />
          </div>
        </section>

        <Quiz />

        <section className="compact-section tools-section" id="ferramenta" data-track-section="ferramenta">
          <div className="compact-card">
            <h2>Ferramenta para usar e<br />consultar no dia a dia</h2>
            <div className="tools-grid">
              {toolCards.map((item) => {
                const Icon = item.icon
                return (
                  <article className="tool-card" key={item.title}>
                    <div className="tool-card__image">
                      <img src={item.image} alt="" />
                      <span className="tool-card__icon"><Icon /></span>
                    </div>
                    <h3>{item.title}</h3>
                    <p>{item.copy}</p>
                  </article>
                )
              })}
            </div>
          </div>
        </section>

        <section className="compact-section logic-section" id="logica" data-track-section="logica">
          <div className="compact-card">
            <h2>Não é um Cardápio pronto.<br /><span>É uma ferramenta prática com plano de progressão</span></h2>

            <div className="logic-grid">
              <article className="logic-column">
                <strong>Não entrega pratos para copiar</strong>
                <p>Você aprende critérios para entender o que priorizar e adaptar as combinações ao que já existe na sua rotina.</p>
              </article>

              <article className="logic-column">
                <strong>Não depende de novas receitas</strong>
                <p>As referências organizam funções, combinações e possibilidades para que cada refeição não precise começar do improviso.</p>
              </article>

              <article className="logic-column">
                <strong>A lógica continua depois do exemplo</strong>
                <p>O plano de progressão transforma a referência em uso prático ao longo dos 37 dias, até que decidir fique mais simples de repetir.</p>
              </article>
            </div>
          </div>
        </section>

        <section className="compact-section progression-section" id="progressao" data-track-section="progressao">
          <div className="compact-card">
            <h2>Mais do que ideias no cardápio.<br /><span>É uma experiência de 37 dias que se adapta a você.</span></h2>

            <div className="days-grid">
              {progressionDays.map((item) => (
                <article className={`day-card${item.locked ? ' day-card--locked' : ''}`} key={item.day}>
                  <strong>{item.day}</strong>
                  <div className="day-card__visual">
                    {item.image && <img src={item.image} alt="" />}
                    {item.locked && <span className="day-card__lock"><LockIcon /></span>}
                  </div>
                  <p>{item.text}</p>
                </article>
              ))}
            </div>

            <div className="progress-lines" aria-hidden="true">
              <span className="progress-lines__start" />
              <span className="progress-lines__rest" />
            </div>
            <div className="progress-labels">
              <small>Semana 1 • Base do método</small>
              <small>Semanas 2 a 5 • Aprofundamento e personalização</small>
            </div>
          </div>
        </section>

        <section className="compact-section quick-section" id="conteudo-rapido" data-track-section="conteudo_rapido">
          <div className="compact-card">
            <h2>Conteúdo rápido, decisões mais simples</h2>
            <div className="quick-grid">
              <article>
                <strong>Bases completas de trocas e composições inteligentes</strong>
                <p>Para o dia a dia com clareza e variedade.</p>
                <span className="mini-foods">🥕 🥔 🥦 🌽</span>
              </article>
              <article>
                <strong>Cardápios estratégicos para diferentes objetivos</strong>
                <p>Referências para momentos diferentes do dia.</p>
                <span className="mini-foods">🍠 🥚 🍚 🥬</span>
              </article>
              <article>
                <strong>Dicas práticas para rotina real.</strong>
                <p>Menos dúvida, mais ação.</p>
                <span className="quick-check"><CheckIcon /></span>
              </article>
            </div>
          </div>
        </section>

        <section className="offer-band" id="oferta" data-track-section="oferta" data-track-once="offer_view">
          <div className="offer-band__copy">
            <h2>Quando você tem uma referência, a próxima refeição não começa do zero.</h2>
            <p>Prato 10x é clareza, liberdade e consistência para transformar sua alimentação de dentro para fora.</p>
            <ul>
              <li><CheckIcon /> 37 dias de conteúdo completo</li>
              <li><CheckIcon /> Nova ideia todos os dias</li>
              <li><CheckIcon /> Flexibilidade para a sua rotina</li>
              <li><CheckIcon /> Resultados reais na sua rotina</li>
            </ul>
          </div>

          <div className="offer-band__price">
            <strong>R$37</strong>
            <span>em até 12x de R$ 4,17<br />ou à vista no pix</span>
            <button type="button" onClick={() => openCheckout('offer-band')}>
              Quero comprar por R$1 por dia <LeafIcon />
            </button>
          </div>
        </section>

        <div className="trust-row" aria-label="Informações do acesso">
          <span><LockIcon /> Pagamento seguro</span>
          <span><ClockIcon /> Acesso imediato</span>
          <span><GridIcon /> Use na prática</span>
          <span><TargetIcon /> 100% online</span>
        </div>

        <section className="compact-section topics-section" id="assuntos" data-track-section="assuntos">
          <div className="compact-card">
            <h2>12 assuntos abordados e vividos na prática.</h2>
            <ol className="topics-grid">
              {topicItems.map((item, index) => (
                <li key={item}>
                  <span>{String(index + 1).padStart(2, '0')}</span>
                  <strong>{item}</strong>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section className="compact-section experience-section" id="experiencia" data-track-section="experiencia">
          <div className="compact-card">
            <h2>Experiência prática, decisões reais, impacto.</h2>
            <div className="experience-grid">
              <article><BowlIcon /><strong>Experiência prática, não teórica.</strong><p>Use no dia a dia, sem complicação.</p></article>
              <article><TargetIcon /><strong>Conteúdo pensado para sua autonomia.</strong><p>Você aprende, você escolhe.</p></article>
              <article><ClockIcon /><strong>Atualizações que mantêm o conteúdo sempre relevante.</strong><p>Você nunca fica sozinho.</p></article>
            </div>
          </div>
        </section>

        <section className="compact-section journey-section">
          <div className="compact-card">
            <h2>Como a experiência evolui ao longo dos 37 dias</h2>
            <div className="journey-grid">
              {experiencePhases.map((phase) => (
                <article key={phase.days}>
                  <span>{phase.days}</span>
                  <h3>{phase.title}</h3>
                  <p>{phase.copy}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="compact-section audience-section">
          <div className="compact-card">
            <h2>Essa experiência faz mais sentido para quem...</h2>
            <div className="audience-layout">
              <ul>
                {audienceItems.map((item) => (
                  <li key={item}><CheckIcon /> <span>{item}</span></li>
                ))}
              </ul>
              <p className="audience-note">O Prato 10x não é uma prescrição alimentar, não substitui acompanhamento profissional e não foi criado para oferecer resultados milagrosos.</p>
            </div>
          </div>
        </section>

        <section className="compact-section faq-section">
          <div className="compact-card">
            <h2>Perguntas frequentes</h2>
            <div className="faq-list">
              {faqItems.map((item) => (
                <details key={item.question}>
                  <summary>{item.question}</summary>
                  <p>{item.answer}</p>
                </details>
              ))}
            </div>
          </div>
        </section>
      </main>

      <footer className="mini-footer">
        <a href="/privacidade.html">Política de Privacidade</a>
        <a href="/termos.html">Termos de Uso</a>
        <span>© {new Date().getFullYear()} Prato 10x</span>
      </footer>
    </div>
  )
}
