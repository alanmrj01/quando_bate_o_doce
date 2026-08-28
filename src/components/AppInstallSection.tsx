import { CategoryAppPhone, HomeScreenPhone, SituationAppPhone } from './TopGuideMockups'

const installSteps = [
  {
    number: '1',
    title: 'Instale na tela inicial',
    copy: 'Adicione o app na sua tela inicial e deixe sempre à mão.',
    visual: <HomeScreenPhone className="app-phone--step" />,
  },
  {
    number: '2',
    title: 'Abra pela situação',
    copy: 'Escolha o momento que combina com a sua vontade de doce.',
    visual: <SituationAppPhone className="app-phone--step" />,
  },
  {
    number: '3',
    title: 'Escolha a opção',
    copy: 'Veja as opções fit e escolha a que combina com você agora.',
    visual: <CategoryAppPhone className="app-phone--step" />,
  },
] as const

export function AppInstallSection() {
  return (
    <section className="app-fold app-fold--install section-shell" data-reveal>
      <div className="app-install-copy">
        <h2>
          Você instala<br />
          uma vez e usa<br />
          como app no<br />
          <span>seu celular.</span>
        </h2>
        <p>É rápido, prático e sempre<br />à mão quando a vontade<br />aparecer.</p>
      </div>

      <div className="app-install-steps" aria-label="Como usar o Quando Bate o Doce">
        {installSteps.map(({ number, title, copy, visual }) => (
          <article key={number}>
            <span className="app-step-number">{number}</span>
            <div className="app-install-step-visual">{visual}</div>
            <h3>{number}. {title}</h3>
            <p>{copy}</p>
          </article>
        ))}
      </div>

      <div className="app-install-summary">
        <span aria-hidden="true">↻</span>
        <p><strong>Você não procura receitas aleatórias.</strong><br />Você abre, escolhe a situação e vai direto para uma opção.</p>
      </div>

      <img className="app-install-chocolate" src="/guide-food-icons/zero-sugar-chocolate.png" alt="" width="192" height="192" loading="lazy" decoding="async" aria-hidden="true" />
    </section>
  )
}
