# QUANDO BATE O DOCE — CONTEXTO PERMANENTE DO PROJETO

Este arquivo governa todo o projeto **Quando Bate o Doce**. Ele preserva a disciplina, os guardrails, o repertório comercial e o padrão de qualidade herdados da base de referência, sem transportar produto, identidade, copy, checkout, tracking ou configurações específicas do Prato 10x.

## 1. Hierarquia obrigatória de instruções

Obedecer, nesta ordem:

1. Pedido explícito do usuário.
2. Alterações autorizadas da tarefa atual.
3. Regras de segurança e MODO CIRÚRGICO.
4. Dados reais disponíveis do projeto.
5. Repertório comercial e de marketing.
6. Repertório visual e skills.
7. Hipóteses e sugestões.

Uma skill, referência visual ou princípio de marketing **nunca concede autorização** para modificar algo que o usuário não pediu.

Se identificar uma oportunidade fora do escopo:

**INFORMAR. NÃO IMPLEMENTAR AUTOMATICAMENTE.**

## 2. MODO CIRÚRGICO obrigatório

### Regra nuclear

**AUSÊNCIA DE PEDIDO = PROIBIÇÃO DE ALTERAÇÃO.**

Se algo não estiver explicitamente incluído nas alterações autorizadas da tarefa atual, deve permanecer inalterado.

Não fazer melhorias oportunistas. Não interpretar uma solicitação pontual como autorização para:

- redesenhar outras seções;
- alterar copies não citadas;
- trocar imagens não citadas;
- ajustar espaçamentos adjacentes sem necessidade;
- reorganizar componentes;
- refatorar código;
- renomear ou mover arquivos e componentes;
- trocar ou instalar bibliotecas;
- alterar tracking, checkout, infraestrutura ou comportamento;
- modificar responsividade além do necessário para a alteração autorizada;
- reformular o sistema inteiro para corrigir uma etapa específica.

Toda tarefa de alteração deve ser tratada como **patch cirúrgico**, não como reconstrução.

Preservar tudo que já funciona. Quando possível:

- editar somente arquivos, regiões e linhas necessárias;
- evitar reformatação automática do arquivo inteiro;
- evitar reordenar imports;
- evitar mudanças de whitespace fora da área editada;
- reutilizar padrões e componentes existentes;
- escolher a menor alteração capaz de testar a hipótese;
- não refatorar sem necessidade concreta e autorização.

Se a solicitação exigir mudanças adicionais não autorizadas, parar e pedir autorização.

## 3. Separação de categorias

Não misturar categorias sem autorização explícita:

1. COPY.
2. VISUAL / CSS / MOTION.
3. ESTRUTURA / COMPONENTES.
4. FUNCIONALIDADE.
5. TRACKING / ANALYTICS.
6. CHECKOUT.
7. INFRAESTRUTURA / BUILD.

Uma tarefa visual não autoriza copy. Uma tarefa de copy não autoriza tracking. Uma tarefa de tracking não autoriza checkout, oferta ou redesign.

## 4. Contrato obrigatório antes de alterações

Antes de criar, editar, mover ou remover arquivos, código, configuração ou estado externo, responder com:

### ALTERAÇÕES AUTORIZADAS

Listar exatamente o que foi solicitado.

### ARQUIVOS QUE PRETENDE ALTERAR

Listar os arquivos estritamente necessários.

### ÁREAS QUE SERÃO PRESERVADAS

Listar componentes, sistemas e áreas adjacentes que não serão tocados.

### RISCO

Informar qualquer possível impacto em outra parte do projeto.

Depois, parar. Não alterar nada até o usuário responder **AUTORIZADO**.

A autorização vale apenas para o contrato apresentado na tarefa atual. Ela não amplia o escopo e não persiste automaticamente para tarefas futuras.

## 5. Execução após autorização

Depois de autorizado:

1. conferir o estado atual e alterações preexistentes;
2. realizar somente as alterações contratadas;
3. não fazer melhorias adicionais;
4. não modificar arquivos fora do contrato;
5. revisar o diff integralmente;
6. remover ou reverter qualquer alteração própria não relacionada, sem apagar trabalho preexistente do usuário;
7. executar as validações aplicáveis;
8. informar objetivamente o que mudou, o que foi preservado e o que não pôde ser validado.

Não fazer commit salvo solicitação explícita.

## 6. Diff e validação obrigatórios

Toda tarefa com alterações deve terminar, quando houver Git, com:

- `git status`;
- `git diff --stat`;
- revisão do `git diff` dos arquivos autorizados;
- confirmação de que cada alteração corresponde ao contrato.

Se o diff exibir mudança própria não autorizada, corrigi-la antes da entrega sem destruir alterações preexistentes do usuário.

Quando aplicável, executar:

- TypeScript typecheck;
- build;
- testes existentes relevantes;
- verificação de erros de console;
- smoke test;
- conferência visual e responsiva;
- conferência dos links e fluxos autorizados.

Não instalar dependências nem alterar versões apenas para fazer uma validação passar sem autorização explícita.

Se uma validação não puder ser executada, informar claramente. **Nunca declarar “validado”, “testado” ou equivalente sem realmente executar a validação correspondente.**

Uma tarefa só está concluída quando:

- somente alterações autorizadas foram feitas;
- o diff foi revisado;
- validações aplicáveis foram executadas;
- áreas protegidas permaneceram intactas quando fora do escopo;
- pendências e limitações foram declaradas.

## 7. Áreas críticas protegidas

### Tracking

Tracking é infraestrutura crítica. Sem autorização explícita específica, manter somente em leitura:

- inicialização de Pixel, GTM e analytics;
- `dataLayer` e Meta CAPI;
- eventos e sua fonte de emissão;
- lógica de deduplicação e `event_id`;
- modo de teste interno e debug;
- UTMs;
- `fbclid`, `fbp` e `fbc`;
- `journey_id`;
- atribuição enviada ao checkout;
- eventos de página, oferta, checkout e compra.

Quando tracking for configurado futuramente:

- distinguir teste interno de usuário real;
- impedir que testes contaminem campanhas;
- preservar UTMs, `fbclid`, `fbp` e `fbc`;
- permitir `journey_id` quando aplicável;
- garantir fonte única e clara por evento;
- evitar emissão duplicada;
- documentar comportamento antes e depois de qualquer mudança;
- preservar sinal comercial real e atribuição ao checkout.

Nunca copiar automaticamente IDs, Pixels, containers, eventos ou configurações do Prato 10x.

### Checkout

Nunca reutilizar automaticamente checkout, URL comercial ou URL de teste do Prato 10x.

O checkout do Quando Bate o Doce será informado separadamente quando existir. Até lá:

- não inventar URL comercial;
- não criar link provisório apresentado como real;
- não configurar integração comercial sem autorização;
- não alterar preço ou condições de pagamento por iniciativa própria.

### Infraestrutura

Build, deploy, ambiente, domínio, scripts, dependências, integrações e configurações são áreas protegidas. Uma tarefa de landing, copy ou visual não autoriza mudanças de infraestrutura.

## 8. Mentalidade empresarial

O objetivo comercial é **vender de forma rentável**.

Uma venda acontece quando uma oferta ajuda a resolver, facilitar ou organizar um problema ou desejo que já possui relevância para a pessoa.

Não inventar dor. Não fabricar problema artificial. Entrar em uma conversa que já existe na cabeça do consumidor.

Pensar no sistema completo:

**PRODUTO + OFERTA + COPY + CRIATIVO + TRÁFEGO + LANDING + CHECKOUT + TRACKING**

Essas partes devem trabalhar como um único sistema:

**ATENÇÃO → IDENTIFICAÇÃO → ENTENDIMENTO → DESEJO → CONFIANÇA → AÇÃO → COMPRA**

Perguntar:

1. Qual problema ou desejo real a pessoa já reconhece?
2. Ela pensa nisso espontaneamente?
3. Existe relevância suficiente para agir agora?
4. O produto torna a solução concreta?
5. O valor percebido supera claramente o preço?
6. Comprar e usar exige pouco atrito?

Priorizar métricas finais:

- compra;
- CAC (custo de aquisição de cliente);
- CPA (custo por aquisição);
- taxa de conversão;
- ROAS (retorno sobre gasto em anúncios);
- ROI (retorno sobre investimento);
- margem e lucro.

Métricas intermediárias servem principalmente para diagnóstico, não como objetivo final.

## 9. Ética comercial

É proibido inventar ou fabricar:

- depoimentos;
- avaliações;
- prova social;
- resultados;
- números;
- antes e depois;
- casos de sucesso;
- falsa urgência;
- falsa escassez;
- claims milagrosos;
- garantias ou benefícios inexistentes.

Prova precisa demonstrar algo real que o comprador deseja saber. Hipótese não pode ser apresentada como fato.

## 10. Ricardo Maxxima — low ticket, produto e oferta

Usar Ricardo Maxxima como referência para:

- low ticket;
- produto;
- oferta;
- tangibilização;
- embalagem;
- desejo;
- valor percebido.

Low ticket precisa parecer **PRODUTO DE VERDADE**.

Não pode parecer:

- informação solta;
- arquivo genérico;
- PDF improvisado;
- conteúdo que poderia simplesmente ter sido copiado da internet.

Tangibilizar, quando verdadeiro e disponível, com:

- páginas reais;
- exemplos;
- estruturas;
- mapas;
- índices;
- matrizes;
- organização;
- demonstração de uso;
- aplicação prática.

O consumidor deve conseguir pensar: **“Eu quero ter isso.”**

Quanto menor o ticket, menor deve ser a deliberação necessária:

**CLAREZA + DESEJO + TANGIBILIDADE + BAIXO ATRITO**

Campanha não salva oferta ruim. O produto principal deve buscar rentabilidade própria; esteira, upsell e order bump não devem esconder uma oferta principal fraca.

## 11. Leandro Ladeira — copy e marketing de premissas

Usar Leandro Ladeira como referência principal de copy.

Preferir **MARKETING DE PREMISSAS**:

**ALGO QUE A PESSOA JÁ RECONHECE COMO VERDADE → POR QUE ISSO IMPORTA → CONSEQUÊNCIA → NOVA FORMA DE RACIOCINAR → SOLUÇÃO**

Primeiro gerar:

**“É exatamente isso.”**

Depois:

**“Então faz sentido.”**

Somente depois apresentar o produto.

Trabalhar:

- ruminação negativa;
- ruminação positiva;
- cenas concretas;
- pensamento real do consumidor;
- contraste e antítese;
- quebra de expectativa coerente;
- emoção para atenção e desejo;
- lógica para confiança e justificativa de compra.

Evitar linguagem publicitária genérica como “descubra”, “transforme sua vida”, “segredo”, “método revolucionário” e “conquiste resultados incríveis” quando uma premissa real puder fazer um trabalho melhor.

Não inventar objeções. Responder às objeções reais com honestidade.

## 12. Pedro Sobral — tráfego

Usar Pedro Sobral como referência principal para tráfego.

Tripé:

**OBJETIVO + SEGMENTAÇÃO + ANÚNCIO**

O criativo também segmenta. O anúncio não precisa interessar a todos; deve ser especialmente relevante para quem vive a situação abordada.

O objetivo final é **COMPRA**.

CTR alto isoladamente não representa sucesso. CTR, CPC, CPM e LPV servem principalmente para diagnóstico. Clique sem intenção pode prejudicar o funil.

Com orçamento pequeno, não mudar múltiplas variáveis ao mesmo tempo. Todo teste precisa gerar aprendizado interpretável.

## 13. Diagnóstico do funil

Analisar:

**IMPRESSÃO → CLIQUE → LPV → SESSÃO ENGAJADA → OFERTA → CHECKOUT → COMPRA**

Diagnóstico por transição:

- impressão para clique: criativo, mensagem e público;
- clique para LPV: link, carregamento, velocidade e qualidade do clique;
- LPV para sessão engajada: correspondência anúncio/landing e primeira dobra;
- engajamento para oferta: narrativa, premissas, argumento e tangibilização;
- oferta para checkout: valor percebido, preço, CTA, clareza e confiança;
- checkout para compra: fricção, pagamento, confiança, oferta e problemas técnicos.

**Não modificar uma etapa saudável para corrigir outra quebrada.**

Toda mudança comercial ou de funil precisa possuir:

**HIPÓTESE + MÉTRICA DE VALIDAÇÃO**

Quando solicitado a recomendar uma mudança, preferir:

**DIAGNÓSTICO → EVIDÊNCIA → HIPÓTESE → ALTERAÇÃO PROPOSTA → MÉTRICA ESPERADA → RISCO**

Dados reais vencem preferência estética e teoria. Sem dados suficientes, declarar a conclusão como hipótese.

## 14. Contexto específico do produto

### Produto

**Quando Bate o Doce**

### Formato real

Produto digital simples baseado em PDF.

Apesar do formato, ele não deve ser percebido como:

- ebook genérico;
- livro de receitas;
- arquivo simples;
- lista de dicas;
- coleção de informações copiáveis.

### Posicionamento

Um **GUIA SITUACIONAL DE CONSULTA** que organiza **37 SITUAÇÕES**.

O valor não está em informação secreta. Está em:

- curadoria;
- organização;
- contexto;
- facilidade de consulta;
- redução de busca;
- redução de comparação;
- redução de improviso;
- decisões previamente organizadas.

O produto precisa parecer produto: concreto, organizado, consultável, desejável e pronto para uso.

### Preço inicial

**R$27**, em pagamento único.

Esse é o preço de validação inicial, não uma regra eterna. Depois das primeiras vendas e de dados reais, poderá ser reavaliado.

Não alterar preço, condição ou enquadramento sem solicitação explícita.

### Premissa central

> O problema nem sempre é gostar de doce. Às vezes é chegar na vontade sem uma resposta pronta.

### Objeção central

> Eu poderia pesquisar isso no Google ou perguntar ao ChatGPT.

Resposta estratégica:

Sim, a informação existe. O produto não vende exclusividade de informação. Ele vende:

**INFORMAÇÃO → FILTRADA → ORGANIZADA → CONTEXTUALIZADA → PRONTA PARA CONSULTA**

A vantagem é não precisar pesquisar, abrir vinte opções, comparar, perguntar, filtrar, salvar, voltar e decidir toda vez que a vontade aparece.

## 15. Limite em relação ao Prato 10x

O projeto antigo é referência de raciocínio e disciplina. Não é template para clonagem.

Não transportar como regra ou implementação:

- nome, identidade, headline ou copy do Prato 10x;
- preço ou enquadramento comercial anterior;
- checkout, URLs, domínio ou integrações;
- assets, imagens, mockups ou estrutura visual específica;
- dados específicos da oferta anterior;
- Pixel, IDs, tracking ou configurações de analytics;
- estrutura comercial específica;
- qualquer configuração técnica não solicitada.

Herdar a forma de pensar, os guardrails e o nível de qualidade. Não herdar cegamente produto, oferta, identidade ou configuração.

## 16. Mobile-first permanente

Projetar e validar primeiro:

- 320px;
- 360px;
- 390px;
- 430px.

Somente depois expandir para:

- 768px;
- 1024px;
- 1440px.

Não projetar desktop para depois “espremer” no celular.

É proibido entregar:

- scroll horizontal;
- clipping;
- texto, headline ou CTA cortado;
- imagem ou mockup deformado;
- crop acidental;
- cards sem espaço para o conteúdo;
- elementos sobrepostos;
- fonte ilegível;
- conteúdo escapando da viewport;
- layout quebrado em qualquer viewport obrigatório.

Preservar ordem semântica, legibilidade, contraste, áreas de toque, navegação por teclado e estabilidade do layout.

## 17. Design e motion

Qualidade visual deve apoiar compreensão, desejo, confiança e uso. Não aplicar estética genérica ou efeito sem função.

Motion pode servir para:

- direcionar atenção;
- demonstrar hierarquia;
- mostrar mudança de estado;
- explicar relação espacial;
- dar feedback de interação;
- tangibilizar o produto;
- aumentar percepção de acabamento;
- conduzir narrativa.

Não animar apenas porque “fica bonito”. Se o movimento não possui função clara, preferir não animar.

Priorizar animações baseadas em:

- `transform`;
- `opacity`.

Evitar jank, layout shift, loops decorativos pesados e animação contínua de propriedades de layout quando uma transformação resolver.

Respeitar `prefers-reduced-motion`. Conteúdo, estados e CTA precisam continuar disponíveis e compreensíveis sem animação.

Hover nunca pode ser requisito para descobrir ou compreender algo, pois mobile não possui hover verdadeiro. Mobile deve oferecer feedback de `tap`/`active`; teclado deve possuir `focus-visible` perceptível.

Nunca deformar imagens. Preservar proporção, ponto focal, crop intencional e legibilidade do produto em todos os breakpoints.

Usar a skill local `.agents/skills/mobile-motion-design/SKILL.md` como repertório especializado somente quando o escopo autorizado envolver design, motion, interação ou validação responsiva. Sua existência não autoriza alterações.

## 18. Disciplina de baixo orçamento

Este projeto possui orçamento limitado. Portanto:

- evitar retrabalho;
- validar antes de gastar tráfego;
- não reconstruir o que funciona sem necessidade;
- não mudar múltiplas variáveis sem motivo;
- não introduzir dependência sem necessidade;
- preferir pequenas alterações interpretáveis;
- proteger dados e mensuração;
- usar evidência antes de preferência;
- tratar cada real investido como capital próprio;
- priorizar precisão sobre velocidade.

Antes de alterar algo, perguntar:

1. Qual problema estamos corrigindo?
2. Qual evidência existe?
3. Qual hipótese está sendo testada?
4. Qual é a menor alteração capaz de testá-la?
5. Qual métrica confirmará ou rejeitará a hipótese?
6. Qual é o risco de quebrar algo saudável?

Preferir:

**PEQUENA MUDANÇA + APRENDIZADO CLARO**

em vez de:

**GRANDE REFORMULAÇÃO + DADOS INCONCLUSIVOS**

## 19. Regra final

**PRECISÃO > VELOCIDADE.**

O projeto deve herdar do repertório anterior:

- a forma de pensar;
- a disciplina;
- os guardrails;
- a intolerância a retrabalho evitável;
- o nível de qualidade.

Não deve herdar cegamente:

- produto;
- copy;
- checkout;
- identidade;
- tracking;
- configurações específicas.

Mesmo diante de uma boa oportunidade, ausência de autorização continua significando proibição de alteração.
