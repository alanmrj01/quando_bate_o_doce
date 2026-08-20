---
name: mobile-motion-design
description: Orienta auditorias e implementações visuais autorizadas do Quando Bate o Doce com design mobile-first, motion funcional, microinterações, scroll, profundidade, componentes premium, responsividade, acessibilidade e performance. Use em tarefas de landing page que peçam direção visual, animação, interação ou validação responsiva; não use a skill como autorização para alterar arquivos.
---

# Mobile Motion Design

## Finalidade

Use esta skill como repertório especializado para analisar, planejar, implementar e validar experiências visuais mobile-first do Quando Bate o Doce quando a tarefa atual autorizar esse trabalho.

O objetivo não é encher a página de efeitos. O objetivo é produzir uma experiência que pareça dirigida e executada por uma equipe profissional de direção de arte, motion design e frontend.

Busque uma landing:

- premium;
- humana;
- leve;
- organizada;
- concreta;
- desejável;
- rápida para compreender e usar.

Evite aparência de template genérico, landing produzida por IA, estética gamer, cyberpunk, neon, sci-fi ou tecnologia exagerada.

## Autoridade e limites

Esta skill fornece repertório. Ela não concede autorização para editar o projeto, instalar bibliotecas, mudar a oferta ou ampliar o escopo.

Obedeça, nesta ordem:

1. pedido explícito do usuário;
2. alterações autorizadas da tarefa atual;
3. `AGENTS.md`, MODO CIRÚRGICO e regras de segurança;
4. dados reais do projeto;
5. repertório comercial e de marketing;
6. esta skill;
7. hipóteses e sugestões.

Ausência de pedido significa proibição de alteração.

Antes de qualquer edição, cumpra o fluxo:

`CONTRATO → AUTORIZADO → IMPLEMENTAÇÃO → DIFF → TESTES`

Se a tarefa for somente de análise, permaneça em leitura. Se a oportunidade estiver fora do escopo, informe-a separadamente como sugestão futura.

Não instale automaticamente Three.js, Tailwind CSS, Animate.css, Storybook, shadcn/ui, Material UI ou qualquer outra dependência. Extraia princípios aplicáveis à base existente e preserve a stack atual, salvo autorização explícita.

## Quando usar

Use esta skill quando a solicitação envolver um ou mais destes temas:

- direção visual da landing;
- experiência mobile;
- motion design;
- microinterações;
- hover, press, tap ou estados de foco;
- scroll reveal ou animação conduzida por scroll;
- parallax, profundidade ou camadas;
- movimento e composição de imagens;
- hierarquia visual;
- refinamento de componentes;
- responsividade;
- performance de animação;
- acessibilidade de movimento;
- redução de jank;
- validação visual responsiva.

Não a invoque para justificar mudanças de copy, tracking, checkout, dependências ou configuração quando esses itens não estiverem explicitamente autorizados.

## Processo obrigatório

### 1. Fixar o escopo

Leia integralmente o `AGENTS.md` aplicável. Registre o arquivo e a região autorizados, o que deve permanecer intacto e quais testes são permitidos.

Não confunda uma tarefa visual com autorização para:

- reescrever copy;
- alterar oferta ou preço;
- substituir imagens;
- mudar tracking;
- trocar checkout;
- instalar framework;
- reconstruir componentes fora do escopo.

### 2. Auditar antes de propor

Inspecione a implementação atual e identifique:

- hierarquia da seção;
- ordem do conteúdo no DOM;
- comportamento entre 320px e 1440px;
- componentes e tokens existentes;
- estados interativos existentes;
- imagens, proporções e crops;
- regras de movimento já presentes;
- custos de renderização e possíveis fontes de jank;
- comportamento com `prefers-reduced-motion`;
- relação da seção com a narrativa comercial.

Preserve padrões saudáveis. Não redesenhe por preferência pessoal.

### 3. Formular a função do movimento

Toda animação precisa cumprir pelo menos uma função:

1. direcionar atenção;
2. demonstrar hierarquia;
3. explicar relação espacial;
4. mostrar mudança de estado;
5. dar feedback de interação;
6. aumentar percepção de qualidade;
7. tangibilizar o produto;
8. conduzir a narrativa;
9. revelar conteúdo no momento correto.

Se não houver função clara, prefira não animar.

Para cada movimento, registre mentalmente ou no diagnóstico:

- gatilho;
- elemento;
- propriedade animada;
- função;
- duração e curva;
- comportamento mobile;
- comportamento com movimento reduzido;
- risco de distração ou custo de renderização.

### 4. Implementar a menor solução autorizada

Reutilize componentes, tokens e padrões da base. Faça o menor patch capaz de testar a hipótese visual. Não introduza uma biblioteca para resolver uma transição que CSS e a stack atual já resolvem.

### 5. Validar e revisar o diff

Teste todos os viewports obrigatórios, estados interativos, redução de movimento e performance. Revise o diff integralmente e confirme que nenhuma área protegida foi alterada.

## Mobile-first absoluto

Comece sempre por:

- 320px;
- 360px;
- 390px;
- 430px.

Somente depois expanda para:

- 768px;
- 1024px;
- 1440px.

Desktop nunca deve ser criado primeiro para depois ser espremido no celular. Mobile é a interface primária.

Em cada largura mobile, verifique:

- conteúdo prioritário visível cedo;
- leitura confortável sem zoom;
- largura de linha apropriada;
- headline sem palavras cortadas;
- CTA acessível por toque;
- ausência de scroll horizontal;
- imagens sem deformação;
- produto legível;
- espaço suficiente entre alvos interativos;
- nenhuma informação dependente de hover;
- animação sem travar ou atrasar a rolagem.

Expanda o layout apenas quando o conteúdo pedir, não por breakpoints arbitrários. Preserve a ordem semântica e adapte composição, spacing, sizing e densidade progressivamente.

## Direção de arte e composição

Cada seção deve possuir uma hierarquia inequívoca. Use, quando necessários:

1. elemento de orientação ou kicker;
2. headline;
3. argumento;
4. representação visual;
5. ação.

Não dê o mesmo peso visual a todos os elementos. Crie contraste por:

- escala;
- espaço;
- peso tipográfico;
- cor;
- posição;
- superfície;
- imagem;
- ritmo;
- entrada no tempo.

Prefira uma ideia visual dominante por seção. Elementos secundários devem apoiar essa ideia, não competir com ela.

Use assimetria de forma controlada quando ela melhorar ritmo ou foco. Não sacrifique leitura, alinhamento ou previsibilidade de interação apenas para parecer diferente.

## Sistema visual e componentes premium

Trate componentes como peças consistentes de um sistema, inspirando-se nos princípios de composição, estados e isolamento presentes em shadcn/ui, Material UI e Storybook.

Para cada componente interativo, defina os estados relevantes:

- default;
- hover, quando houver ponteiro compatível;
- focus-visible;
- active ou pressed;
- selected, quando aplicável;
- expanded ou collapsed, quando aplicável;
- loading, quando aplicável;
- disabled, quando aplicável;
- erro e sucesso, quando aplicáveis.

Mantenha consistência de:

- raio;
- borda;
- sombra;
- superfície;
- tipografia;
- spacing;
- ícones;
- transições;
- semântica de estados.

Não use uma variante visual diferente sem uma razão de hierarquia ou função.

Quando o projeto já possuir Storybook ou ambiente equivalente, valide componentes em isolamento antes da integração. Quando não possuir, não instale nada automaticamente: confira os estados na infraestrutura existente ou em inspeção local autorizada.

## Microinterações

Microinterações devem comunicar causa e efeito rapidamente. Elas não devem competir com conteúdo ou parecer brinquedos independentes.

### Hover no desktop

Use hover apenas como reforço, nunca como único meio de descobrir informação.

Opções discretas:

- pequeno `translate` direcional;
- `scale` leve;
- alteração coerente de sombra;
- alteração de borda ou superfície;
- destaque de ícone;
- deslocamento curto que reforce a direção da ação.

Evite:

- escala exagerada;
- bounce barato;
- glow excessivo;
- elemento pulando;
- layout deslocando;
- movimento que dificulte leitura;
- hover aplicado em dispositivos que não o suportam de modo confiável.

Restrinja estilos de hover a capacidades reais de ponteiro quando isso evitar estados presos ou enganosos no touch.

### Press e tap no mobile

Substitua dependência de hover por feedback tátil visual imediato:

- pequena redução de escala;
- mudança curta de superfície;
- contraste de borda;
- destaque de estado;
- expansão por toque quando necessária.

O feedback deve começar rápido, terminar sem atraso perceptível e não impedir a navegação. Preserve área de toque confortável e estabilidade do layout.

### Focus-visible

Forneça foco perceptível e coerente com o sistema visual. Não remova outline sem substituto equivalente. O foco não pode depender somente de cor sutil, sombra invisível ou movimento.

### Disabled e loading

Estados desabilitados devem continuar reconhecíveis. Estados de carregamento não podem sugerir que uma ação concluída ainda precisa de outro toque. Evite animação contínua pesada e preserve o rótulo ou contexto da ação quando possível.

## Motion tokens e ritmo

Centralize durações, curvas e amplitudes quando a base permitir. Um sistema pequeno e coerente é preferível a valores únicos espalhados.

Use categorias funcionais:

- instantâneo: confirmação de press ou mudança mínima;
- rápido: hover, foco, ícone e feedback de controle;
- moderado: entrada de componente ou mudança de superfície;
- narrativo: reveal de seção, demonstração ou transição espacial relevante.

Movimentos maiores normalmente pedem mais tempo que microfeedbacks, mas nunca transforme leitura em espera. Saídas podem ser ligeiramente mais rápidas que entradas quando isso preservar fluidez.

Escolha curvas de aceleração que comuniquem intenção:

- entrada desacelera de forma natural;
- saída libera espaço com agilidade;
- mudança contínua evita solavancos;
- elemento físico não deve inverter direção sem motivo.

Evite combinar muitas curvas, durações e amplitudes na mesma seção.

## Scroll reveal

Use reveal para construir ritmo e ordem, não para esconder toda a página.

Prefira:

- `opacity` com `transform`;
- fade com `translateY` curto;
- cards em pequeno stagger;
- imagem revelada levemente depois do texto quando isso reforçar hierarquia;
- linhas, indicadores ou etapas crescendo em sequência;
- acionamento uma vez quando repetição não acrescentar informação.

Evite:

- animar cada frase ou palavra;
- atrasar conteúdo essencial;
- revelar tudo com a mesma receita;
- grandes deslocamentos em mobile;
- conteúdo invisível caso JavaScript falhe;
- reiniciar animações continuamente ao oscilar na borda da viewport.

Conteúdo e CTA devem continuar acessíveis imediatamente com movimento reduzido ou falha de script.

## Scroll-driven animation

Use progresso de scroll quando a posição da rolagem realmente explicar progressão, transformação ou relação espacial.

Boas aplicações:

- demonstrar evolução do produto;
- acompanhar uma sequência curta;
- mover camadas de mockup de forma proporcional;
- destacar a etapa atual de um processo;
- revelar uma comparação espacial clara.

Não prenda a rolagem sem necessidade. Não altere a velocidade natural do scroll. Não use uma sequência longa que obrigue o usuário a esperar para acessar conteúdo.

Quando houver cálculo em JavaScript:

- agrupe leituras e escritas de layout;
- sincronize atualizações visuais com o frame de renderização;
- evite criar múltiplos listeners equivalentes;
- remova listeners e observers ao desmontar;
- pause trabalho fora da viewport;
- limite a frequência de cálculo;
- não force reflow a cada evento de scroll.

Prefira recursos nativos e a stack existente quando atendem à necessidade. Fallback deve preservar conteúdo e ação, mesmo sem o efeito.

## Parallax

Parallax é uma ferramenta de profundidade, não um efeito padrão para toda seção.

Use principalmente em:

- hero;
- mockups;
- produto;
- elementos decorativos;
- camadas de fundo.

No mobile:

- reduza significativamente a amplitude;
- limite o número de camadas;
- preserve a velocidade natural da rolagem;
- confirme que nada escapa do viewport;
- desative quando o custo ou desconforto superar a função.

Nunca produza scroll pesado, atraso de resposta, movimento desconfortável, texto difícil de acompanhar ou elementos saindo da composição.

Remova parallax em `prefers-reduced-motion: reduce`.

## Profundidade e movimento espacial

Extraia de Three.js princípios de cena, câmera, camadas, transformação e custo de renderização sem presumir a instalação da biblioteca.

Construa profundidade com:

- sobreposição controlada;
- diferença de escala;
- foreground e background;
- sombras coerentes com uma direção de luz;
- camadas;
- blur de fundo quando necessário;
- movimento relativo sutil;
- perspectiva apenas quando melhora a leitura espacial.

Mantenha uma lógica consistente de profundidade. Elementos visualmente próximos devem reagir de maneira compatível; camadas distantes devem mover-se menos quando essa relação for usada.

Não transforme a landing em uma interface 3D sem necessidade. WebGL, canvas contínuo ou cenas pesadas exigem justificativa, autorização e orçamento de performance explícitos.

## Imagens e produto

Nunca deforme assets. Preserve aspect ratio e use `object-fit` e `object-position` conscientemente.

O crop deve parecer intencional em cada breakpoint. Em imagens de pessoas, evite cortar acidentalmente:

- olhos;
- metade do rosto;
- topo da cabeça quando prejudicar a composição;
- mãos relevantes;
- a interação com o produto.

Quando a imagem contém o produto, ele precisa continuar legível o suficiente para tangibilizar a oferta.

Ao mover imagens:

- preserve o ponto focal;
- não exponha áreas vazias fora do asset;
- mantenha a composição dentro do viewport;
- não cubra texto ou CTA;
- use máscaras e overflow com intenção;
- teste o primeiro e o último frame;
- confirme que a imagem estável continua boa sem animação.

Não sacrifique nitidez ou tempo de carregamento por uma camada decorativa dispensável.

## Tipografia responsiva

Evite valores rígidos excessivos. Use `clamp()` quando ele produzir escala controlada entre limites legíveis.

Nenhum título pode:

- sair do viewport;
- cortar palavras;
- invadir imagem sem intenção;
- exigir fonte minúscula;
- encostar nas bordas;
- criar órfãs visuais evitáveis;
- perder contraste durante a animação.

Avalie line-height, tracking e largura no dispositivo estreito real. A escala tipográfica deve indicar prioridade sem esmagar a representação do produto ou empurrar o CTA para uma distância injustificada.

Não anime propriedades tipográficas de modo que o texto salte de linha, provoque layout shift ou prejudique seleção e leitura.

## Cards

Cards devem organizar relações, não apenas colocar tudo dentro de caixas.

Evite repetição genérica. Introduza variação controlada por:

- escala;
- composição;
- posição da imagem;
- hierarquia interna;
- destaque funcional;
- relação entre cards.

Preserve consistência de design system. Não use altura fixa quando o texto puder variar. Garanta que estados animados não cortem conteúdo, alterem o fluxo de forma brusca ou criem alvos sobrepostos.

Stagger curto pode explicar sequência; não deve obrigar o usuário a esperar cada card aparecer.

## Landing page e conversão

Motion é subordinado à compreensão e à conversão.

Mapeie o movimento à narrativa:

- hero: atenção e tangibilização;
- seção seguinte: identificação;
- demonstração: funcionamento do produto;
- progressão: evolução ou sequência;
- prova ou esclarecimento: redução de incerteza;
- CTA: feedback de interação e confirmação de ação.

Uma animação está errada se:

- dificulta leitura;
- retarda o CTA;
- distrai da oferta;
- esconde o produto;
- cria jank;
- prejudica mobile;
- muda a ordem mental da narrativa;
- aumenta curiosidade visual sem aumentar compreensão.

No Quando Bate o Doce, o movimento deve transmitir:

- leveza;
- clareza;
- organização;
- facilidade de consulta;
- sensação de guia situacional;
- produto concreto.

Prefira movimento seguro, intencional e editorial a efeitos espetaculares sem função comercial.

## Performance e redução de jank

Priorize animações baseadas em:

- `transform`;
- `opacity`.

Evite animar continuamente, quando transform puder produzir o mesmo resultado:

- `width`;
- `height`;
- `top`;
- `left`;
- `margin`;
- `padding`.

Regras de execução:

- não aplique `will-change` globalmente ou permanentemente sem justificativa;
- evite sombras e filtros grandes animados em múltiplas camadas;
- pause loops quando a página estiver oculta ou o elemento estiver fora da viewport;
- não mantenha animações decorativas contínuas sem necessidade;
- evite leituras de layout intercaladas com escritas no mesmo frame;
- não provoque layout shift para criar efeito;
- teste em viewport mobile e condições de CPU menos favoráveis;
- preserve input, tap e scroll responsivos durante a animação;
- use o menor número de elementos animados capaz de comunicar a ideia;
- remova código, listeners e classes temporárias quando o componente encerrar seu ciclo.

Use Three.js somente se a tarefa autorizar e se profundidade real justificar o custo. Não instale uma solução 3D para simular um deslocamento que CSS pode executar com qualidade.

## Acessibilidade de movimento

Toda implementação relevante deve respeitar:

```css
@media (prefers-reduced-motion: reduce) {
  /* Preserve conteúdo e estados; remova movimento não essencial. */
}
```

Nessa condição:

- remova parallax;
- remova deslocamentos grandes;
- remova animações decorativas contínuas;
- reduza ou elimine durações;
- torne conteúdo imediatamente acessível;
- preserve feedback essencial por mudança clara de estado;
- evite rolagem ou foco animados sem necessidade.

Movimento nunca pode ser o único sinal de estado, progresso, sucesso, erro ou seleção. Combine-o com texto, ícone, forma, contraste ou outra pista persistente.

Evite flashes, oscilações e movimento periférico repetitivo. Não mova o alvo durante a tentativa de toque ou clique.

## Responsive motion

Não copie a mesma animação de desktop para todos os tamanhos.

Ao reduzir a viewport:

- diminua distância e amplitude;
- reduza número de camadas;
- simplifique stagger;
- evite entradas laterais que atravessem a tela inteira;
- preserve o produto e o CTA acima dos efeitos;
- substitua hover por press/tap;
- considere remover efeitos puramente decorativos.

Ao ampliar a viewport:

- use o espaço adicional para relações e camadas mais claras;
- não aumente movimento apenas porque há espaço;
- preserve a mesma prioridade narrativa do mobile;
- evite transformar composição editorial em painel de efeitos.

## Diagnóstico e recomendação

Quando solicitado a avaliar uma experiência visual, responda com:

`DIAGNÓSTICO → EVIDÊNCIA → HIPÓTESE → ALTERAÇÃO PROPOSTA → MÉTRICA ESPERADA → RISCO`

Para motion, acrescente:

- função do movimento;
- gatilho;
- fallback sem movimento;
- impacto mobile;
- impacto de performance.

Não apresente preferência estética como fato. Quando não houver evidência suficiente, marque a conclusão como hipótese.

## Validação obrigatória

Para qualquer implementação visual futura autorizada em que esta skill for usada, valide:

- 320px;
- 360px;
- 390px;
- 430px;
- 768px;
- 1024px;
- 1440px.

Em todas as larguras, confira:

- overflow;
- clipping;
- scroll horizontal;
- ordem e legibilidade do texto;
- imagens, crop e proporção;
- produto visível;
- CTA;
- áreas de toque;
- estados de hover compatíveis;
- press/tap;
- focus-visible;
- active e disabled quando aplicáveis;
- scroll reveal;
- scroll-driven animation;
- parallax;
- primeiro e último frame;
- conteúdo com JavaScript indisponível, quando pertinente;
- `prefers-reduced-motion`;
- fluidez do scroll;
- resposta ao input;
- jank e layout shift;
- estabilidade após resize e mudança de orientação.

Valide também que:

- a animação possui função declarada;
- a experiência permanece compreensível sem animação;
- nenhum conteúdo exige espera desnecessária;
- nenhum efeito bloqueia compra ou navegação;
- o diff contém somente alterações autorizadas;
- nenhuma dependência foi adicionada sem autorização.

## Critérios de aceite

Considere o trabalho visual pronto somente quando:

1. funciona primeiro nos quatro viewports mobile;
2. expande de modo coerente para tablet e desktop;
3. mantém texto, produto e CTA legíveis;
4. oferece feedback equivalente para touch, teclado e ponteiro;
5. respeita redução de movimento;
6. não produz scroll horizontal, clipping ou layout shift evitável;
7. não introduz jank perceptível;
8. cada animação possui função concreta;
9. a composição parece intencional sem parecer genérica;
10. o motion reforça a narrativa comercial;
11. nenhuma biblioteca ou área protegida foi alterada fora do contrato;
12. testes e diff foram apresentados conforme o `AGENTS.md`.

## Fontes normativas autorizadas

O repertório desta skill usa exclusivamente estes repositórios GitHub como referências nomeadas. Todos possuíam mais de 70.000 estrelas na verificação de 19 de agosto de 2026:

1. [shadcn-ui/ui](https://github.com/shadcn-ui/ui) — composição de componentes, estados, hierarquia, consistência e interfaces refinadas.
2. [mui/material-ui](https://github.com/mui/material-ui) — design systems, estados, interação, responsividade, temas e consistência.
3. [mrdoob/three.js](https://github.com/mrdoob/three.js) — profundidade, transformações, camadas, parallax, composição espacial e consciência de renderização.
4. [tailwindlabs/tailwindcss](https://github.com/tailwindlabs/tailwindcss) — mobile-first, breakpoints, spacing, sizing, composição e adaptação responsiva.
5. [animate-css/animate.css](https://github.com/animate-css/animate.css) — entradas, saídas, timing, transform, opacity e padrões reutilizáveis de animação CSS.
6. [storybookjs/storybook](https://github.com/storybookjs/storybook) — componentes em isolamento, estados visuais, conferência e regressão antes da integração.

Não acrescente como fonte normativa qualquer repositório com menos de 70.000 estrelas. Antes de atualizar esta lista, verifique novamente o limite. Conhecimento geral de navegador e CSS pode apoiar a implementação, mas não deve introduzir outro repositório GitHub como autoridade desta skill.

## Regra final

A existência desta skill nunca autoriza uma alteração.

Se o usuário solicitar somente movimento, não altere copy. Se solicitar somente layout, não altere tracking. Se solicitar somente um componente, não redesenhe a landing inteira. Se identificar uma oportunidade fora do escopo, informe-a sem implementar.

O resultado correto é o menor trabalho visual autorizado que melhora clareza, qualidade, interação e experiência mobile sem comprometer conversão, acessibilidade, performance ou estabilidade.
