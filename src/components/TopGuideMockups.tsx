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
        <ellipse cx="24" cy="38" rx="14" ry="4" fill="#b87a4d" opacity=".32" />
        <path d="M11 32h26l-4 10H15Z" fill="#b97842" />
        <path d="m14 33 4 7 3-7 3 8 3-8 3 7 4-7" fill="none" stroke="#e9bc7a" strokeWidth="1.2" />
        <circle cx="24" cy="22" r="12" fill="#673227" />
        <circle cx="20" cy="18" r="6" fill="#814236" opacity=".7" />
        <g fill="#f3d7b6">
          <rect x="16" y="17" width="4" height="1.4" rx=".7" transform="rotate(24 16 17)" />
          <rect x="24" y="14" width="4" height="1.4" rx=".7" transform="rotate(-18 24 14)" />
          <rect x="29" y="19" width="4" height="1.4" rx=".7" transform="rotate(31 29 19)" />
          <rect x="18" y="25" width="4" height="1.4" rx=".7" transform="rotate(-27 18 25)" />
          <rect x="26" y="27" width="4" height="1.4" rx=".7" transform="rotate(16 26 27)" />
        </g>
      </svg>
    )
  }

  if (kind === 'sem-acucar') {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <ellipse cx="24" cy="39" rx="13" ry="3.5" fill="#c18b52" opacity=".25" />
        <path d="M14 29h20l-2.2 11H16.2Z" fill="#d89a55" />
        <path d="M17 29c.3-5.4 4-7.2 7.2-9.7 2.8-2.2 2.7-5.2.8-7.2 5.9 2.1 9.2 7.2 6.4 11.1 3.5.3 5 3.5 2.6 5.8Z" fill="#edb35f" />
        <path d="M18.5 28c2.3-3.9 8.5-2.8 8-7.9 2.8 2.6 1.4 5.2-.1 7.6" fill="none" stroke="#fff0c7" strokeWidth="1.8" strokeLinecap="round" />
        <path d="M32.5 11c-3.8 0-6.2 2.1-7 5.6 4 .6 7.2-1.1 8.7-4.8Z" fill="#768b51" />
        <path d="M13 16h6M16 13v6" stroke="#b63c50" strokeWidth="1.8" strokeLinecap="round" />
      </svg>
    )
  }

  if (kind === 'chocolate-zero') {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <ellipse cx="24" cy="40" rx="15" ry="3" fill="#7c4938" opacity=".22" />
        <g transform="rotate(-10 23 24)">
          <rect x="11" y="8" width="25" height="32" rx="3" fill="#5b2d24" />
          <rect x="13" y="10" width="9" height="8" rx="1.5" fill="#764033" />
          <rect x="24" y="10" width="9" height="8" rx="1.5" fill="#6a382d" />
          <rect x="13" y="20" width="9" height="8" rx="1.5" fill="#6a382d" />
          <rect x="24" y="20" width="9" height="8" rx="1.5" fill="#81483a" />
          <rect x="13" y="30" width="9" height="8" rx="1.5" fill="#81483a" />
          <rect x="24" y="30" width="9" height="8" rx="1.5" fill="#67352b" />
          <path d="M14.5 11.5h6" stroke="#b47762" strokeWidth="1" strokeLinecap="round" opacity=".65" />
        </g>
        <circle cx="37" cy="34" r="7" fill="#f7eee1" stroke="#b63c50" strokeWidth="1.5" />
        <path d="m33.8 37.2 6.4-6.4" stroke="#b63c50" strokeWidth="1.7" strokeLinecap="round" />
      </svg>
    )
  }

  if (kind === 'proteicas') {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <ellipse cx="24" cy="39" rx="14" ry="3.5" fill="#aa6a61" opacity=".2" />
        <path d="M12 18h24l-2.4 20H14.4Z" fill="#f2e7d6" stroke="#d0b99f" strokeWidth="1.2" />
        <ellipse cx="24" cy="18" rx="12" ry="4.5" fill="#fffaf0" stroke="#d0b99f" strokeWidth="1.2" />
        <path d="M15.5 18c3.6-2.4 13.6-2.4 17 0" fill="none" stroke="#e2c69e" strokeWidth="2" strokeLinecap="round" />
        <circle cx="20" cy="17" r="2.2" fill="#b64259" />
        <circle cx="25" cy="18" r="1.8" fill="#7f9457" />
        <path d="M31 14c3.8-6.2 6.9-7 8.5-5.8-1.2 3.5-3.9 6-8.5 7.4Z" fill="#d9b76f" />
        <path d="M18 26h12" stroke="#b63c50" strokeWidth="2" strokeLinecap="round" />
        <path d="M20 30h8" stroke="#d69aab" strokeWidth="1.8" strokeLinecap="round" />
      </svg>
    )
  }

  if (kind === 'saudaveis') {
    return (
      <svg viewBox="0 0 48 48" aria-hidden="true">
        <ellipse cx="24" cy="40" rx="13" ry="3" fill="#a74a4c" opacity=".18" />
        <path d="M24 13c-8.3 0-13.7 5.4-12.1 13.6C13.8 36.3 24 42 24 42s10.2-5.7 12.1-15.4C37.7 18.4 32.3 13 24 13Z" fill="#d7444f" />
        <path d="M24 14c-5.3.1-9.3 3-9.4 8.5" fill="none" stroke="#f47c7e" strokeWidth="2.4" strokeLinecap="round" opacity=".68" />
        <path d="M24 14c-4.8-.1-7.5-2.3-8.5-5.2 3.9-.8 7.2.1 9.3 3.1C27 8.4 30.5 7 34.5 8c-1.1 3.2-4.3 5.6-10.5 6Z" fill="#70884e" />
        <g fill="#f7c78c">
          <ellipse cx="19" cy="24" rx="1" ry="1.4" /><ellipse cx="28" cy="22" rx="1" ry="1.4" />
          <ellipse cx="23" cy="30" rx="1" ry="1.4" /><ellipse cx="30" cy="29" rx="1" ry="1.4" />
          <ellipse cx="20" cy="35" rx="1" ry="1.4" />
        </g>
      </svg>
    )
  }

  return (
    <svg viewBox="0 0 48 48" aria-hidden="true">
      <ellipse cx="24" cy="39" rx="15" ry="3" fill="#7e654d" opacity=".2" />
      <path d="M9 24h30c-.9 10.4-6.2 16-15 16S9.9 34.4 9 24Z" fill="#d7a46b" />
      <path d="M11 24h26" stroke="#f6d39c" strokeWidth="2" strokeLinecap="round" />
      <ellipse cx="24" cy="23" rx="14" ry="5.5" fill="#f0dfbf" />
      <path d="M13 23c2.4-4 6.3-5.8 11.4-5.8 4.7 0 8.5 1.7 10.8 5" fill="#e4b967" />
      <path d="M17 21c2.4-2.4 8.5-3.3 13.6-.8" fill="none" stroke="#f8e6bd" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M25 17c-.7-5.6 2.4-9.1 8.1-9.8.3 5.6-2.8 8.8-8.1 9.8Z" fill="#758a51" />
      <circle cx="17" cy="20" r="1.2" fill="#a64b4b" /><circle cx="28" cy="21" r="1.1" fill="#a64b4b" />
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
          <p><span>O que está</span><span>acontecendo</span><span>agora?</span></p>
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
