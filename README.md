# Quando Bate o Doce

Landing page React + Vite + TypeScript para o guia situacional de consulta **Quando Bate o Doce**.

## Desenvolvimento

```bash
npm install
npm run dev
```

## Validação

```bash
npm run typecheck
npm run build
```

A saída de produção é gerada em `dist/` e está preparada para publicação na Netlify.

## Checkout

As URLs de checkout de produção e QA são definidas explicitamente em `src/config.ts`. Os CTAs mantêm um `<a href>` real e só emitem o evento de clique quando a URL ativa é HTTPS e válida.

## Tracking

A landing inicializa Meta Pixel e GA4 somente no domínio canônico de produção. Sem parâmetro, utiliza a configuração de produção; `?qa=1` ativa QA e `?internal_test=1` permanece como alias legado de QA. Esses parâmetros de modo não são persistidos nem enviados ao checkout.

As atribuições allowlisted são armazenadas em namespaces independentes de `sessionStorage`: `qbd_production_*` e `qbd_qa_*`. O storage legado compartilhado `qbd_*` é ignorado, evitando que UTMs, `src`, `s1`/`s2`/`s3` ou `fbclid` de QA reapareçam em produção.

O `sck` recebido na entrada não é preservado: o `sck` de saída continua sendo derivado do `journey_id` local do respectivo ambiente. Essa regra foi somente documentada; seu comportamento não foi alterado.

A landing emite Meta `PageView`, `ViewContent` e `CheckoutClick`, além de GA4 `page_view`, `view_item`, `landing_engaged`, `offer_view`, `cta_view`, `quiz_start`, `quiz_complete` e `checkout_click`. `InitiateCheckout`, `Purchase`, `begin_checkout` e `purchase` permanecem sob responsabilidade da Kiwify e não são emitidos pela landing.
