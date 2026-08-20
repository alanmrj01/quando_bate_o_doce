# Prato 10x — Landing Page v2.3 Tracking Safe

Landing page React + Vite + TypeScript, preparada para StackBlitz e deploy na Netlify.

## Rodar localmente / StackBlitz

```bash
npm install
npm run dev
```

## Build de produção

```bash
npm run build
```

Saída: `dist/`

## Tracking comercial

- GTM: `GTM-KSGSGL26`
- Meta Pixel de produção: `2073559566628743`
- Checkout comercial Kiwify: `https://pay.kiwify.com.br/qpiXBDM`
- O `InitiateCheckout` NÃO é disparado manualmente na landing. A Kiwify é a fonte do evento quando o checkout realmente abre.
- UTMs, `fbclid`, `_fbp`/`fbp`, `_fbc`/`fbc`, `src`, placement e IDs de campanha/anúncio são preservados em `sessionStorage` e repassados ao checkout quando disponíveis.
- Cada sessão recebe um `journey_id` anônimo, enviado à Kiwify em `s1`.

## Modo de teste — SEM contaminar o Meta de produção

Abra a mesma landing acrescentando:

```text
?internal_test=1
```

Exemplo:

```text
https://SEU-DOMINIO/?internal_test=1
```

Nesse modo:

1. o bootstrap cria `internal_test=1` no `dataLayer` antes do GTM;
2. o `fbq` é neutralizado antes do GTM e o Meta Pixel hardcoded não é inicializado;
3. eventos da landing continuam disponíveis no `dataLayer` com `debug_mode=true`;
4. CTAs usam exclusivamente o checkout de teste `https://pay.kiwify.com.br/4B5VArF`;
5. o checkout recebe `src=internal_test`;
6. respostas do quiz não são enviadas ao Netlify Forms comercial;
7. uma faixa roxa deixa claro que a sessão está em QA.

O modo teste NÃO é persistente: sem `?internal_test=1`, a página funciona em produção normalmente. Isso reduz o risco de esquecer o navegador preso em modo QA.

## Atenção ao GTM

O código neutraliza snippets Meta padrão via `fbq` durante `internal_test=1` e publica `internal_test` no `dataLayer`. Se futuramente for criada qualquer nova tag Meta/CAPI dentro do GTM, mantenha também uma exceção de disparo para `internal_test = 1`. Não criar uma segunda origem de `PageView`, `InitiateCheckout` ou `Purchase`.

## Esta versão preserva

- hero, copy, quiz, oferta e layout existentes;
- Netlify Forms em produção;
- GTM e GA4 em produção;
- Meta Pixel de produção para visitantes reais;
- passagem de atribuição até o checkout;
- checkout comercial inalterado para tráfego real.
