const homeOptions = [
  'Depois do almoço',
  'Fim da tarde',
  'À noite',
  'Quero chocolate',
  'Tenho 5 minutos',
] as const

type CategoryKind = 'low-carb' | 'brigadeiro' | 'sem-acucar' | 'chocolate-zero' | 'proteicas' | 'saudaveis'

const fitCategories: Array<{ label: string; kind: CategoryKind }> = [
  { label: 'Receitas low carb', kind: 'low-carb' },
  { label: 'Brigadeiro fit', kind: 'brigadeiro' },
  { label: 'Doces sem açúcar', kind: 'sem-acucar' },
  { label: 'Chocolate zero açúcar', kind: 'chocolate-zero' },
  { label: 'Opções proteicas', kind: 'proteicas' },
  { label: 'Receitas saudáveis', kind: 'saudaveis' },
]

function CategoryIcon({ kind }: { kind: CategoryKind }) {
  if (kind === 'brigadeiro') {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <path d="M13 33c1-9 5-15 11-15s10 6 11 15" />
        <path d="M10 34h28l-3 7H13Z" />
        <path d="m18 14 2 3m6-5-1 4m7 0-3 2" />
      </svg>
    )
  }

  if (kind === 'sem-acucar') {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <path d="m14 19 10-6 10 6v12l-10 6-10-6Z" />
        <path d="m14 19 10 6 10-6M24 25v12M10 39 38 9" />
      </svg>
    )
  }

  if (kind === 'chocolate-zero') {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <path d="M11 12h26v25H11zM11 24h26M20 12v25M29 12v25" />
        <circle cx="34" cy="34" r="8" />
        <path d="m30 38 8-8" />
      </svg>
    )
  }

  if (kind === 'proteicas') {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <path d="M17 10h14l3 7-2 22H16l-2-22Z" />
        <path d="M14 17h20M19 25c3 3 7 3 10 0" />
        <path d="M21 10V7h6v3" />
      </svg>
    )
  }

  if (kind === 'saudaveis') {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <path d="M24 17c-7-5-15 0-15 9 0 8 7 14 15 14s15-6 15-14c0-9-8-14-15-9Z" />
        <path d="M24 17c0-5 3-8 7-10M25 12c5-3 9-2 11 1-4 3-8 3-11-1Z" />
      </svg>
    )
  }

  return (
    <svg viewBox="0 0 48 48" aria-hidden="true">
      <path d="M10 29h28c-1 8-6 12-14 12S11 37 10 29Z" />
      <path d="M14 29c2-7 8-11 18-10" />
      <path d="M25 18c-1-6 2-10 8-11 1 6-2 10-8 11Z" />
    </svg>
  )
}

export function HeroGuideMockup() {
  return (
    <div className="top-phone-scene" role="img" aria-label="Guia Quando Bate o Doce aberto no celular sobre uma composição de chocolate">
      <div className="top-phone-scene__chocolate" aria-hidden="true">
        <img
          src="/hero-chocolate-splash-v1.webp"
          alt=""
          width="1254"
          height="1254"
          loading="eager"
          decoding="async"
          fetchPriority="high"
        />
      </div>

      <div className="top-phone top-phone--home">
        <div className="top-phone__speaker" aria-hidden="true" />
        <div className="top-phone__screen">
          <div className="top-phone__brand">
            <span className="apple-mark apple-mark--phone" aria-hidden="true" />
            <span>QUANDO BATE O DOCE</span>
          </div>
          <p>O que está acontecendo agora?</p>
          <div className="top-phone__menu">
            {homeOptions.map((option) => (
              <span className={option === 'Quero chocolate' ? 'is-featured' : ''} key={option}>
                {option}
                <b aria-hidden="true">›</b>
              </span>
            ))}
          </div>
          <small>37 situações para consultar</small>
        </div>
      </div>
    </div>
  )
}

export function SituationGuideMockup() {
  return (
    <div className="situation-phone" role="img" aria-label="Tela do guia com categorias de opções fit e proteicas para depois do almoço">
      <div className="situation-phone__speaker" aria-hidden="true" />
      <div className="situation-phone__screen">
        <span className="situation-phone__back">← Voltar</span>
        <div className="situation-phone__title">
          <span className="apple-mark apple-mark--phone" aria-hidden="true" />
          <div>
            <small>SITUAÇÃO</small>
            <strong>Depois do almoço</strong>
          </div>
        </div>
        <p>Opções fit e proteicas para esse momento</p>
        <div className="fit-category-grid">
          {fitCategories.map(({ label, kind }) => (
            <span className="fit-category" key={label}>
              <span className={`fit-category__icon fit-category__icon--${kind}`}>
                <CategoryIcon kind={kind} />
              </span>
              <b>{label}</b>
            </span>
          ))}
        </div>
        <small className="situation-phone__footer">Escolha uma categoria para consultar</small>
      </div>
    </div>
  )
}
