export const quizQuestions = [
  {
    question: 'Você sente vontade de comer algo doce no seu dia?',
    options: [
      { label: 'Sim', value: 'sim' },
      { label: 'Às vezes', value: 'nao' },
    ],
  },
  {
    question: 'Quando essa vontade aparece mais?',
    options: [
      { label: 'Depois do almoço', value: 'sim' },
      { label: 'Fim da tarde ou noite', value: 'nao' },
    ],
  },
  {
    question: 'Quando ela aparece, você tenta continuar na dieta?',
    options: [
      { label: 'Sim, quase sempre', value: 'sim' },
      { label: 'Nem sempre', value: 'nao' },
    ],
  },
  {
    question: 'Quando quer doce, você busca uma opção fit ou improvisa?',
    options: [
      { label: 'Busco uma opção fit', value: 'sim' },
      { label: 'Acabo improvisando', value: 'nao' },
    ],
  },
] as const

export const situations = [
  'Acabei de almoçar',
  'Quero chocolate',
  'É fim da tarde',
  'É noite',
  'Tenho 5 minutos',
  'Quero algo cremoso',
  'Quero algo gelado',
  'Quero algo crocante',
  'Quase não tenho nada em casa',
  'Não quero cozinhar',
] as const

export const situationCategories = [
  'Depois das refeições',
  'Fim da tarde',
  'Noite',
  'Chocolate',
  'Cremoso',
  'Crocante',
  'Gelado',
  'Pouco tempo',
  'Poucos ingredientes',
  'Não quero cozinhar',
  'Quero algo simples',
  'Quero variar',
] as const

export const deliverables = [
  ['01', 'App Quando Bate o Doce'],
  ['02', '37 situações organizadas para consulta'],
  ['03', 'Tela “O que está acontecendo agora?”'],
  ['04', 'Navegação rápida pela situação'],
  ['05', 'Opções fit e proteicas por momento'],
  ['06', 'Categorias low carb, sem açúcar e chocolate zero'],
  ['07', 'Lista-base do doce fit'],
  ['08', 'Modo emergência para poucos minutos'],
] as const

export const audienceFit = [
  'depois do almoço procura algo doce sem querer sair da alimentação que planejou;',
  'no fim da tarde a vontade aparece e você procura uma opção fit;',
  'à noite quer uma alternativa doce que faça sentido para esse momento;',
  'chocolate aparece com frequência na cabeça;',
  'salva receitas fit, mas não lembra delas quando precisa;',
  'pesquisa opções proteicas apenas quando a vontade já apareceu;',
  'quer alternativas organizadas em vez de começar outra busca toda vez.',
] as const

export const audienceNotFit = [
  'Não é um plano alimentar.',
  'Não é prescrição nutricional.',
  'Não promete emagrecimento ou resultado corporal.',
  'Não promete eliminar vontade de doce.',
  'Não substitui nutricionista ou acompanhamento profissional.',
  'Não exige abandonar sobremesas.',
] as const

export const faqItems = [
  {
    question: 'O que é o Quando Bate o Doce?',
    answer:
      'É um app de consulta rápida para abrir no celular quando a vontade de doce aparece. Você escolhe a situação e encontra opções fit organizadas para aquele momento.',
  },
  {
    question: 'Como eu recebo o acesso?',
    answer:
      'Após a confirmação do pagamento, você recebe o acesso digital e as orientações para abrir a ferramenta no celular.',
  },
  {
    question: 'Como adiciono à tela inicial?',
    answer:
      'As instruções de instalação mostram como adicionar o Quando Bate o Doce à tela inicial para abrir junto dos outros aplicativos.',
  },
  {
    question: 'Funciona no celular?',
    answer: 'Sim. A experiência é pensada para abrir e consultar diretamente pelo celular.',
  },
  {
    question: 'Preciso baixar pela Play Store ou App Store?',
    answer: 'Não. O acesso é digital e as orientações mostram como adicionar a ferramenta à tela inicial do seu próprio celular.',
  },
  {
    question: 'São realmente 37 situações?',
    answer:
      'Sim. O app organiza 37 situações reais e reúne categorias como brigadeiro fit, chocolate zero açúcar, opções proteicas, low carb, saudáveis e sem açúcar.',
  },
  {
    question: 'O acesso é imediato?',
    answer:
      'Após a confirmação do pagamento, o acesso ao produto digital é liberado conforme o fluxo do checkout.',
  },
  {
    question: 'É assinatura?',
    answer: 'Não. O valor de R$27 é pagamento único.',
  },
] as const
