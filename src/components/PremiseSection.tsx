const scenes = [
  { time: '12:42', title: 'Acabou o almoço', support: 'Deu vontade de um doce.', illustration: 'lunch' },
  { time: '16:18', title: 'Abriu a geladeira', support: 'Queria alguma coisa rápida.', illustration: 'fridge' },
  { time: '21:07', title: 'Chegou a noite', support: 'Bateu vontade de chocolate.', illustration: 'night' },
  { time: 'agora', title: 'E veio a dúvida', support: 'Isso vai me fazer sair da dieta?', illustration: 'thought' },
] as const

type SceneIllustrationProps = {
  scene: Exclude<(typeof scenes)[number]['illustration'], null>
}

function SceneIllustration({ scene }: SceneIllustrationProps) {
  if (scene === 'lunch') {
    return (
      <svg className="scene-illustration" viewBox="0 0 160 76" aria-hidden="true">
        <path className="scene-art-surface" d="M13 57h134v9H13z" />
        <ellipse className="scene-art-soft" cx="80" cy="42" rx="35" ry="16" />
        <ellipse className="scene-art-line" cx="80" cy="40" rx="28" ry="12" />
        <path className="scene-art-line" d="M29 25v33M24 25v14c0 5 10 5 10 0V25M132 25v33M127 25h10" />
        <path className="scene-art-accent" d="M68 39c7 5 17 5 24 0" />
      </svg>
    )
  }

  if (scene === 'fridge') {
    return (
      <svg className="scene-illustration" viewBox="0 0 160 76" aria-hidden="true">
        <path className="scene-art-soft" d="M55 8h48v58H55z" />
        <path className="scene-art-line" d="M55 8h48v58H55zM55 35h48M94 19v9M94 43v9" />
        <path className="scene-art-surface" d="m55 8-22 8v45l22 5z" />
        <path className="scene-art-line" d="m55 8-22 8v45l22 5M43 34v8" />
        <circle className="scene-art-accent-fill" cx="124" cy="25" r="7" />
        <path className="scene-art-line" d="M124 33c-9 1-13 10-12 25M124 35c8 5 10 13 9 23" />
      </svg>
    )
  }

  if (scene === 'night') {
    return (
      <svg className="scene-illustration" viewBox="0 0 160 76" aria-hidden="true">
        <path className="scene-art-soft" d="M17 14h57v43H17z" />
        <path className="scene-art-line" d="M17 14h57v43H17zM45.5 14v43M17 35.5h57" />
        <path className="scene-art-accent-fill" d="M59 20a10 10 0 1 0 8 14 12 12 0 0 1-8-14Z" />
        <path className="scene-art-surface" d="M88 48h52v15H88z" />
        <path className="scene-art-line" d="M88 48c3-9 10-14 20-14h12c10 0 17 5 20 14v15H88zM98 63v5M130 63v5" />
        <path className="scene-art-accent" d="M108 39h12" />
      </svg>
    )
  }

  return (
    <svg className="scene-illustration" viewBox="0 0 160 76" aria-hidden="true">
      <circle className="scene-art-soft" cx="52" cy="29" r="14" />
      <path className="scene-art-surface" d="M25 67c2-17 12-26 27-26s25 9 27 26Z" />
      <path className="scene-art-line" d="M38 29c0-8 6-14 14-14s14 6 14 14-6 14-14 14M25 67c2-17 12-26 27-26s25 9 27 26" />
      <circle className="scene-art-accent-fill" cx="85" cy="41" r="3" />
      <circle className="scene-art-accent-fill" cx="94" cy="31" r="4" />
      <path className="scene-art-soft" d="M101 10h40v24h-40a12 12 0 0 1 0-24Z" />
      <path className="scene-art-line" d="M101 10h40v24h-40a12 12 0 0 1 0-24Z" />
      <path className="scene-art-accent" d="M114 18h14l3 4-10 7-10-7Z" />
    </svg>
  )
}

export function PremiseSection() {
  return (
    <section className="premise-section section-block" data-reveal>
      <div className="section-heading section-heading--center">
        <h2>A vontade de doce aparece. E junto vem aquela dúvida de sair ou não da dieta.</h2>
      </div>

      <div className="scene-timeline">
        {scenes.map(({ time, title, support, illustration }) => (
          <article className={illustration ? 'has-illustration' : ''} key={title}>
            <span>{time}</span>
            {illustration && <SceneIllustration scene={illustration} />}
            <div className="scene-copy">
              <strong>{title}</strong>
              <p>{support}</p>
            </div>
          </article>
        ))}
      </div>

      <div className="thought-card">
        <span>pergunta interna</span>
        <blockquote>“O que eu posso escolher agora?”</blockquote>
        <p>Quando toda vontade de doce vira uma escolha entre matar a vontade e continuar na dieta, ter opções fit já organizadas deixa a decisão muito mais simples.</p>
      </div>
    </section>
  )
}
