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
  ['01', 'Guia Quando Bate o Doce'],
  ['02', '37 situações organizadas'],
  ['03', 'Mapa “O que está acontecendo agora?”'],
  ['04', 'Índice clicável para consulta rápida'],
  ['05', 'Opções fit e proteicas por situação'],
  ['06', 'Categorias low carb, sem açúcar e chocolate zero'],
  ['07', 'Receitas saudáveis e alternativas rápidas'],
  ['08', 'Página “não quero cozinhar”'],
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
    question: 'É um livro de receitas?',
    answer:
      'Não. Receitas e opções fit fazem parte do material, mas tudo é organizado por situações — não como uma coleção genérica de sobremesas.',
  },
  {
    question: 'São realmente 37 situações?',
    answer:
      'Sim. O guia organiza 37 situações relacionadas aos momentos em que a vontade de doce aparece e reúne opções fit e proteicas adequadas a cada contexto.',
  },
  {
    question: 'Preciso seguir alguma ordem?',
    answer:
      'Não. É um material de consulta. Você pode ir diretamente para a situação que mais se parece com o momento atual.',
  },
  {
    question: 'Posso acessar pelo celular?',
    answer: 'Sim. O conteúdo é pensado para consulta prática em dispositivos móveis.',
  },
  {
    question: 'Isso elimina a vontade de doce?',
    answer: 'Não existe essa promessa. A proposta é facilitar sua decisão quando a vontade aparecer.',
  },
  {
    question: 'Preciso comprar ingredientes especiais?',
    answer:
      'A proposta é reunir alternativas fit, proteicas e simples, incluindo possibilidades compatíveis com ingredientes e produtos de uma rotina comum.',
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
