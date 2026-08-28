const situationOptions = [
  { label: 'Depois do almoço', icon: '☕' },
  { label: 'Fim da tarde', icon: '♨' },
  { label: 'Quero chocolate', icon: '▥' },
  { label: 'Noite', icon: '☾' },
  { label: 'Final de semana', icon: '▦' },
] as const

type CategoryKind = 'brigadeiro' | 'chocolate-zero' | 'low-carb' | 'proteicas' | 'saudaveis' | 'sem-acucar'

const fitCategories: Array<{ label: string; kind: CategoryKind }> = [
  { label: 'Brigadeiro fit', kind: 'brigadeiro' },
  { label: 'Chocolate zero açúcar', kind: 'chocolate-zero' },
  { label: 'Receitas low carb', kind: 'low-carb' },
  { label: 'Opções proteicas', kind: 'proteicas' },
  { label: 'Receitas saudáveis', kind: 'saudaveis' },
  { label: 'Doces sem açúcar', kind: 'sem-acucar' },
]

const categoryIconByKind: Record<CategoryKind, string> = {
  brigadeiro: '/guide-food-icons/brigadeiro-fit.png',
  'chocolate-zero': '/guide-food-icons/zero-sugar-chocolate.png',
  'low-carb': '/guide-food-icons/low-carb-bowl.png',
  proteicas: '/guide-food-icons/protein-option.png',
  saudaveis: '/guide-food-icons/healthy-strawberry.png',
  'sem-acucar': '/guide-food-icons/sugar-free-dessert.png',
}

function AppBrand({ compact = false }: { compact?: boolean }) {
  return (
    <span className={`app-screen-brand${compact ? ' is-compact' : ''}`}>
      <img src="/qbd-apple-mark-v1.png" alt="" width="34" height="34" />
      <b>QUANDO BATE O DOCE</b>
    </span>
  )
}

export function SituationAppPhone({ className = '' }: { className?: string }) {
  return (
    <div className={`app-phone app-phone--situations ${className}`.trim()} role="img" aria-label="Aplicativo Quando Bate o Doce aberto na seleção de situações">
      <span className="app-phone__speaker" aria-hidden="true" />
      <div className="app-phone__screen">
        <AppBrand />
        <h3>O que está<br />acontecendo<br />agora?</h3>
        <div className="app-phone__situation-list">
          {situationOptions.map(({ label, icon }) => (
            <span className={label === 'Quero chocolate' ? 'is-selected' : ''} key={label}>
              <i aria-hidden="true">{icon}</i>
              <b>{label}</b>
              <em aria-hidden="true">›</em>
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}

export function CategoryAppPhone({ className = '' }: { className?: string }) {
  return (
    <div className={`app-phone app-phone--categories ${className}`.trim()} role="img" aria-label="Aplicativo mostrando seis categorias de opções fit">
      <span className="app-phone__speaker" aria-hidden="true" />
      <div className="app-phone__screen">
        <AppBrand />
        <h3>Dentro da ferramenta</h3>
        <div className="app-category-grid">
          {fitCategories.map(({ label, kind }) => (
            <span key={label}>
              <img src={categoryIconByKind[kind]} alt="" width="58" height="58" decoding="async" />
              <b>{label}</b>
            </span>
          ))}
        </div>
        <p>Você abre pela situação e vai direto para uma opção que combina com aquele momento.</p>
      </div>
    </div>
  )
}

export function HomeScreenPhone({ className = '' }: { className?: string }) {
  return (
    <div className={`app-phone app-phone--home-screen ${className}`.trim()} role="img" aria-label="Tela inicial do celular com o Quando Bate o Doce instalado ao lado de outros aplicativos">
      <span className="app-phone__speaker" aria-hidden="true" />
      <div className="app-home-screen">
        <span className="app-home-time">9:41</span>
        <div className="app-home-icons">
          <span className="app-icon app-icon--whatsapp"><b>◔</b><small>WhatsApp</small></span>
          <span className="app-icon app-icon--instagram"><b>◎</b><small>Instagram</small></span>
          <span className="app-icon app-icon--qbd"><b><img src="/qbd-apple-mark-v1.png" alt="" /></b><small>Quando Bate<br />o Doce</small></span>
        </div>
        <div className="app-home-dots" aria-hidden="true">••••</div>
        <div className="app-home-dock" aria-hidden="true"><span>▰</span><span>◉</span><span>●</span><span>▣</span></div>
      </div>
    </div>
  )
}

export function BrandAppPhone({ className = '' }: { className?: string }) {
  return (
    <div className={`app-phone app-phone--brand ${className}`.trim()} role="img" aria-label="Tela de abertura do aplicativo Quando Bate o Doce">
      <span className="app-phone__speaker" aria-hidden="true" />
      <div className="app-brand-screen">
        <img src="/qbd-apple-mark-v1.png" alt="" width="118" height="118" />
        <strong>Quando<br />Bate o Doce</strong>
      </div>
    </div>
  )
}

export function HeroAppComposition() {
  return (
    <div className="app-hero-visual" data-reveal>
      <div className="app-hero-chocolate" aria-hidden="true">
        <img src="/hero-chocolate-splash-v1.webp" alt="" width="1254" height="1254" loading="eager" decoding="async" fetchPriority="high" />
      </div>

      <div className="app-hero-phones">
        <SituationAppPhone className="app-phone--hero-situations" />
        <CategoryAppPhone className="app-phone--hero-categories" />
      </div>

      <div className="app-install-proof">
        <HomeScreenPhone />
        <span>Instale e abra<br />sempre que<br />precisar!</span>
      </div>

      <img className="app-food-decor app-food-decor--brigadeiro" src="/guide-food-icons/brigadeiro-fit.png" alt="" width="192" height="192" aria-hidden="true" />
      <img className="app-food-decor app-food-decor--chocolate" src="/guide-food-icons/zero-sugar-chocolate.png" alt="" width="192" height="192" aria-hidden="true" />
    </div>
  )
}
