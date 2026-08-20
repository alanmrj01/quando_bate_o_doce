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

Defina `VITE_CHECKOUT_URL` com a URL comercial real quando ela estiver disponível. Sem essa variável, os CTAs mostram a mensagem segura “Checkout ainda não configurado.”

## Tracking

A página preserva em `sessionStorage` parâmetros de atribuição disponíveis e reconhece `?internal_test=1`. Nenhum Pixel, GTM, GA4 ou emissor externo é incluído por padrão.

