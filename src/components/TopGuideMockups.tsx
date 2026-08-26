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

const categoryIconByKind: Record<CategoryKind, string> = {
  'low-carb': '/guide-food-icons/low-carb-bowl.png',
  brigadeiro: '/guide-food-icons/brigadeiro-fit.png',
  'sem-acucar': '/guide-food-icons/sugar-free-dessert.png',
  'chocolate-zero': '/guide-food-icons/zero-sugar-chocolate.png',
  proteicas: '/guide-food-icons/protein-option.png',
  saudaveis: '/guide-food-icons/healthy-strawberry.png',
}

function CategoryIcon({ kind }: { kind: CategoryKind }) {
  return (
    <img
      src={categoryIconByKind[kind]}
      alt=""
      width="40"
      height="40"
      loading="lazy"
      decoding="async"
    />
  )
}

export function HeroGuideMockup() {
  return (
    <div className="top-phone-scene" role="img" aria-label="Guia Quando Bate o Doce aberto no celular sobre uma composição de chocolate">
      <div className="top-phone-scene__chocolate" aria-hidden="true">
        <picture>
          <source media="(max-width: 599px)" srcSet="/hero-chocolate-reference-v2.jpg" />
          <img
            src="/hero-chocolate-splash-v1.webp"
            alt=""
            width="1254"
            height="1254"
            loading="eager"
            decoding="async"
            fetchPriority="high"
          />
        </picture>
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
