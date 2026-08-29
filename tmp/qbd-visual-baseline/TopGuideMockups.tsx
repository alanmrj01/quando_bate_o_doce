const situationOptions = [
  { label: 'Depois do almoço', icon: '☕' },
  { label: 'Fim da tarde', icon: '♨' },
  { label: 'Quero chocolate', icon: '▥' },
  { label: 'Noite', icon: '☾' },
  { label: 'Final de semana', icon: '▦' },
] as const

export type AppFeatureIconKind =
  | 'bolt'
  | 'bowl'
  | 'camera'
  | 'chat'
  | 'check'
  | 'coin'
  | 'download'
  | 'grid'
  | 'lock'
  | 'phone'
  | 'refresh'
  | 'search'
  | 'screen'
  | 'tap'

export function AppFeatureIcon({ kind }: { kind: AppFeatureIconKind }) {
  return (
    <svg className="app-feature-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
      {kind === 'bolt' && <path d="M13.2 2.8 5.8 13h5.4l-.5 8.2 7.5-11h-5.5l.5-7.4Z" />}
      {kind === 'bowl' && <><path d="M4 11.3h16c-.6 4.8-3.6 7.5-8 7.5s-7.4-2.7-8-7.5Z" /><path d="M7.2 8.2c1-1 2.1-1.5 3.2-1.5 1.2 0 2 .5 2.9 1.5.8.9 1.8 1.3 3.1 1.3" /></>}
      {kind === 'camera' && <><rect x="3.5" y="3.5" width="17" height="17" rx="4" /><circle cx="12" cy="12" r="3.6" /><circle cx="17.4" cy="6.7" r=".8" fill="currentColor" stroke="none" /></>}
      {kind === 'chat' && <><path d="M5.2 18.5 3.8 21l3.3-1A9 9 0 1 0 4 16.9" /><path d="M8.7 8.2c.8 3.1 2.2 4.6 5.2 6l1.5-1.5 2.2 1.1c-.3 1.7-1.4 2.6-3.1 2.6-4.3-.8-7.3-3.7-8-8 0-1.7.9-2.8 2.6-3.1l1.1 2.2-1.5.7Z" /></>}
      {kind === 'check' && <path d="m4.5 12.3 4.4 4.4L19.7 6.4" />}
      {kind === 'coin' && <><circle cx="12" cy="12" r="9" /><path d="M12 6.5v11M15.2 8.8a4.9 4.9 0 0 0-2.9-.8c-1.7 0-2.9.8-2.9 2s1 1.8 2.9 2.1c1.8.3 2.9 1 2.9 2.2 0 1.3-1.3 2.2-3.2 2.2a5 5 0 0 1-3.2-1" /></>}
      {kind === 'download' && <><rect x="4" y="3" width="16" height="18" rx="2.5" /><path d="M12 6v8m-3-3 3 3 3-3M9 18h6" /></>}
      {kind === 'grid' && <><rect x="3.5" y="3.5" width="7" height="7" rx="1.2" /><rect x="13.5" y="3.5" width="7" height="7" rx="1.2" /><rect x="3.5" y="13.5" width="7" height="7" rx="1.2" /><rect x="13.5" y="13.5" width="7" height="7" rx="1.2" /></>}
      {kind === 'lock' && <><rect x="4.5" y="10" width="15" height="10.5" rx="2" /><path d="M8 10V7a4 4 0 0 1 8 0v3m-4 4v2.5" /></>}
      {kind === 'phone' && <><rect x="7" y="2" width="10" height="20" rx="2.3" /><path d="M10.2 18.5h3.6" /></>}
      {kind === 'refresh' && <><path d="M19.2 8.4A8 8 0 0 0 5 7l-1.2 2" /><path d="M3.8 4.5V9h4.5M4.8 15.6A8 8 0 0 0 19 17l1.2-2" /><path d="M20.2 19.5V15h-4.5" /></>}
      {kind === 'search' && <><circle cx="10.5" cy="10.5" r="6.5" /><path d="m15.5 15.5 4.5 4.5" /></>}
      {kind === 'screen' && <><rect x="3" y="4" width="18" height="15" rx="2" /><path d="M8 22h8M12 19v3M7 8h10M7 11h7" /></>}
      {kind === 'tap' && <><path d="M9 11V7.5a1.7 1.7 0 0 1 3.4 0v5.2-2.1a1.6 1.6 0 0 1 3.2 0v2-1a1.6 1.6 0 0 1 3.2 0v3.8c0 3.5-2.4 5.8-6.2 5.8-2.3 0-3.8-.8-5.2-2.7L4.8 15a1.7 1.7 0 0 1 2.6-2.1L9 14.2V11Z" /><path d="M5.5 8.5A5 5 0 0 1 8 4.3" /></>}
    </svg>
  )
}

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
        <h3><span>O que está</span><span>acontecendo agora?</span></h3>
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
          <span className="app-icon app-icon--whatsapp"><b><AppFeatureIcon kind="chat" /></b><small>WhatsApp</small></span>
          <span className="app-icon app-icon--instagram"><b><AppFeatureIcon kind="camera" /></b><small>Instagram</small></span>
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

    </div>
  )
}
