# Prato 10x v2.3 — Validação de tracking

## Alterações cirúrgicas realizadas

- Modo QA explícito por `?internal_test=1`.
- Meta Pixel hardcoded não inicializa em QA.
- `fbq` é neutralizado antes do GTM em QA para bloquear snippets Meta padrão nessa sessão.
- `internal_test=1` e `debug_mode=true` são publicados no `dataLayer` antes do GTM.
- Checkout de QA: `https://pay.kiwify.com.br/4B5VArF`.
- Checkout comercial preservado: `https://pay.kiwify.com.br/qpiXBDM`.
- Removido o `InitiateCheckout` manual da landing; a Kiwify fica responsável pelo evento quando o checkout realmente carrega.
- UTMs, `fbclid`, `fbp`, `fbc`, `src`, placement e IDs de campanha/anúncio são capturados/preservados quando disponíveis.
- `journey_id` anônimo é criado por sessão e enviado em `s1` para a Kiwify.
- Quiz em QA não grava resposta no formulário comercial.
- Banner de QA visível somente em modo teste.

## Testes executados neste pacote

- `analytics.ts` + `config.ts`: typecheck estrito OK.
- Projeto TS/TSX completo: validação TypeScript com stubs das dependências de runtime OK.
- Todos os arquivos TS/TSX: transpile/syntax OK.
- Scripts inline do `index.html`: `node --check` OK.
- HTML: parser OK.
- CSS: balanceamento de blocos OK.
- Smoke test de checkout de produção: URL comercial correta, UTMs + `fbclid` + `fbp` + `fbc` + `s1` preservados.
- Smoke test de checkout QA: URL de teste correta, `src=internal_test` aplicado.
- Smoke test: landing não chama mais `fbq('track', 'InitiateCheckout')`.

## Observação do ambiente de validação

O `npm install` não pôde ser concluído no runtime de geração porque o acesso ao registry expirou por timeout. Por isso o `vite build` final não foi executado aqui. As validações acima foram feitas sem alterar as versões de dependência declaradas no `package.json`.
