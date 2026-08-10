# michaltrs.net

Můj osobní web. Astro 7 + Tailwind v4, statický build, nasazeno na Cloudflare Pages.

[![michaltrs.net](https://img.shields.io/website?url=https%3A%2F%2Fmichaltrs.net&label=michaltrs.net)](https://michaltrs.net)
[![Cloudflare Pages](https://img.shields.io/badge/Deployed%20on-Cloudflare%20Pages-F38020?logo=cloudflare&logoColor=white)](https://pages.cloudflare.com)
[![Built with Astro](https://img.shields.io/badge/Built%20with-Astro-FF5D01?logo=astro&logoColor=white)](https://astro.build)

## O projektu

CTO · MTB rider · otec 3 dětí · Praha. Osobní web s profilem a archivem obsahu z let 2001–2013.

**[→ michaltrs.net](https://michaltrs.net)**

## Architektura

- **Astro 7** + **Tailwind v4**, statický build
- 2 hlavní stránky: homepage (`/`), archiv The Vault (`/vault/`)
- 202 vault entries — news, blog, cnk, cvut-fel, spse-v-uzlabine
- 136 Astro archive stránek + 105 statických HTML (Doxygen, projekty)
- **SEO & optimalizace**: konkrétní pravidla v `robots.txt` pro zamezení indexace tenkých dokumentačních stránek (ČVUT FEL Doxygen), sitemap-index.xml a automatický post-build skript injektující `noindex` do legacy HTML souborů bez kanonických tagů.

## Vývoj

```bash
pnpm install
pnpm dev    # localhost:4321
pnpm build  # dist/
```

## Deployment

Automatický build + deploy přes Cloudflare Pages při push na `main`.
