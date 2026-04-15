# Projekt: michaltrs-hp-astro

Osobní web Michala Trse. Astro 5 + Tailwind v4, statický build. Migrováno ze starého PHP webu (www-2008-20/).

## Architektura

- **2 stránky**: index.astro (homepage), vault.astro (timeline archiv)
- **1 content collection**: vault (195 entries, 5 kategorií: news, blog, cnk, cvut-fel, spse-v-uzlabine)
- **Archive Astro pages**: 136 stránek v src/pages/archive/ (blog 78, cvut-fel 37, spse 8, cnk 11, root 2) + 104 nested HTML (Doxygen, projekty) v public/archive/
- **Migrace hotové**: ČVUT FEL (kompletní), SPŠE (kompletní), Blog (z Bloggeru), News (z RSS), CNK (kompletní)

## Plán práce

### P0 — Hero stránka: revize textu a ikon ✓
- [x] Hero subtitle: "CTO" → "CTO @ Auris One"
- [x] Auris One: 2023→2024, "Pioneer v oblasti AI-first" → "Osvobozujeme lékaře od administrativy"
- [x] Avast: 2005–2023→2006–2024, "lokálního startupu" → "garážovky"
- [x] Pivovar: "Němý Medvěd Brewery" → "Pivovar Němý Medvěd", nový text + CTA Brloh Mělník
- [x] Pivovar ikona: shield → beer SVG, přidán podcast link (10 let pivovaru)
- [x] Movember ikona: dollar sign → knír SVG podle Movember favicon

### P1 — Quick wins ✓
- [x] Opravit Lorem ipsum v Hero.astro (subtitle)
- [x] Vytvořit favicon.svg (Layout.astro ho linkuje ale soubor neexistuje)
- [x] Nastavit `site` v astro.config.mjs (sitemap nefunguje)
- [x] Opravit broken linky ve vault entries — 8 CNK entries opraveno na `/archive/cnk/...` cesty

### P1 — Design & obsah Hero stránky ✓
- [x] Začistit design Hero sekce — layout, typografie, barvy, CTA tlačítka
- [x] Vybrat lepší Vault items na Hero page (VaultSummary) — 4 milníky (SPŠE, CNK, ČVUT, Blog)
- [x] Implementace sociálních odkazů (YouTube, Instagram, Facebook, LinkedIn, Strava, Podcast)

### P2 — Blog image fix ✓
- [x] Zkopírovat 90 obrázků + 1 KMZ z www-2008-20 → public/assets/migrated/
- [x] Opravit 65 blog archive HTML souborů (uploaded_images, cross-refs, CNK linky, picasaweb, ggpht, onblur)
- [x] Vyčistit 33 vault entries s broken placeholder.jpg
- [x] Migrační skript: scripts/fix-blog-refs.py

### P2 — CNK migrace (Cesty na kole) ✓
- [x] Vytvořit archive stránky pro 8 expedic + vrcholy + bike + landing page (11 HTML stránek, 294 assetů)
- [x] Migrační skript: scripts/migrate_cnk.py
- [x] Vault entry opraven: 2009-maroko link
- Konvence cest: `/archive/cnk/{rok}-{nazev}/` (např. 2009-maroko, 2006-pyreneje, 2007-turecko, 2008-dolomiti, vrcholy)

### P2 — Formátování archive stránek ✓
- [x] Lepší zarovnání obrázků v textu (float, marginy, responzivita) — CSS třídy .img-left/.img-right/.img-center
- [x] Rozhodnout velikost obrázků — max-width: 500px, na mobilu 100%
- [x] Sjednotit styling napříč všemi kategoriemi (blog, cnk, cvut-fel, spse-v-uzlabine)
- [x] Vylepšit `public/archive/style.css` — image classes, lightbox overlay, mobile breakpoint
- [x] Lightbox pro obrázky s větší verzí (public/archive/lightbox.js)
- [x] Blogger table wrappers nahrazeny za `<figure>` s `<figcaption>`
- [x] Migrační skript: scripts/fix-blog-styles.py (238 souborů zpracováno)

### P2b — Odstranění layout tabulek z CNK archivu ✓
- [x] Kompletní odstranění layout tabulek ze 2001-svycarsko (5 tabulek + 5 img align)
- [x] Kompletní odstranění layout tabulek ze 2003-viden (30+ tabulek vč. vnořené foto mřížky)
- [x] `<table class="stred">` galerie → `<div class="gallery">` (flex wrap)
- [x] `<table width="..." align="...">` thumbnaily → `<div class="img-left/right">`
- [x] `<table align="center">` → `<div class="gallery">`
- [x] Stats tabulky (vzdálenost + profil) → `<div class="info">`
- [x] Text+mapa tabulky → unwrap s `<div class="img-right">` pro mapy
- [x] Standalone `<img align="...">` → CSS class, `<div align="right">` → inline style
- [x] Ponechány datové tabulky `<table class="tab">` a bike specs `<table class="stred">`
- [x] Přidán `.gallery` CSS do style.css (flex layout, responsive)
- [x] Rozšířen skript scripts/fix-blog-styles.py — 33 layout tabulek odstraněno

### P3 — Archive design cleanup ✓
- [x] Gallery CSS fix — `clear: both`, `.odstavec` margins, float clearing
- [x] Video/embed responsive — 25 embed konverzí (20 YouTube→iframe, 1 Google Maps, 4 dead Flash→placeholder)
- [x] Blog cleanup — 5 Picasa badge removals, 3 photo table→figure, center unwrap
- [x] CNK landing page — 8× `<table class="fv">` → `<div class="card">` + CSS
- [x] SPŠE bare tables — `class="tab"` přidáno ke 4 datovým tabulkám
- [x] CVUT-FEL deprecated HTML — `<center>`, `<font>`, `<hr>` attrs, cellspacing/cellpadding, align→CSS (8 souborů, Doxygen přeskočeny)
- [x] CNK viden stats normalizace — „Ujetá vzdálenost: **X km**" → „vzdálenost: X km | profil cesty"
- [x] `.video-responsive` CSS wrapper (16:9 aspect ratio, max-width 640px)
- [x] `.card` CSS (expedition cards na CNK landing)
- [x] Rozšířen skript scripts/fix-blog-styles.py — video embeds, Picasa badges, Blogger tables, deprecated HTML

### P4 — Konzistence nadpisů a CSS cleanup ✓
- [x] Odstranit duplicitní `<h1>` z 11 CNK archive stránek (řádek 15, duplicát h1 v header divu)
- [x] Změnit `<h1>Deníček cesty...</h1>` → `<h2>` v 5 CNK souborech (sekční nadpis, ne titulek)
- [x] Přidat `.tab` CSS do `public/archive/style.css` (chyběla definice pro 12 souborů)
- [x] Audit CSS — žádné nepoužité třídy k odstranění (`.lightbox-overlay` dynamická, `.content` 84×, `.img-inline` 7×)

### P2 — Hero stránka — opravy obsahu ✓
- [x] Text „Vítejte na palubě" je dětinský — nahrazeno „CTO · MTB rider · otec 3 dětí · Praha"
- [x] Pod první sekcí jsou jen 2 tlačítka — přidán terciární odkaz na The Vault
- [x] Odkazy z timeline (VaultSummary) nefiltrují ve Vault správně — DOM refs přesunuty do init()

### P3b — Remaining cleanup ✓
- [x] Odstranit `updated:` field z 78 blog entries (není ve schema)
- [x] Vyřešit 49 entries s prázdným `link: ""` (kosmetické)
- [x] Vytvořit 404 stránku
- [x] 6 foto placeholderů v PersonalSection — skutečné fotky (MTB alpy, Blinduro, sunset, party, rodina na vrcholu, skialpový sjezd)
- [x] Professional foto/headshot — B&W portrét v ProfessionalSection
- [x] Vyměněny 2 slabé fotky: pivovar → rodinné selfie na vrcholu, lyže flat lay → skialpový sjezd v prašanu
- [x] Strava iframe widget (samé nuly) → link card v řadě s Brewery a Movember (3+3 layout)

### P4b — Archive: validace obsahu a odkazů ✓
- [x] Ověřit že všechny embed obrázky se načítají (žádné broken images) — 9 broken → 0 (imb-cvut cesty opraveny, silvretta panorama nahrazeno)
- [x] Ověřit že všechny embed videa fungují (YouTube iframes, ne dead Flash/placeholder) — 19 YouTube embeds OK, 0 broken
- [x] Konkrétně zkontrolovat video z USA národních parků (2011-08-09 entries) — doplněn YouTube embed (vBWIuTHdDqI)
- [x] Opravit nalezené broken obrázky a videa
- [x] Zkontrolovat všechny externí odkazy ve všech archive stránkách — 361 URL zkontrolováno (122 živých, 142 přesměrovaných, 97 mrtvých)
- [x] Mrtvé odkazy nahradit `<span class="dead-link">` — 79 nahrazení v 56 souborech, `.dead-link` CSS přidáno
- [x] Validační skript: `scripts/validate-archive.py` (238 HTML, report + link-history.md)
- [x] `link-history.md` — kompletní seznam 289 externích odkazů seskupený po stránkách

### P4c — Archive: obtékání obrázků a videí ✓
- [x] Odstranit `class="img-center"` z `<img>` uvnitř `<figure>` — 7 souborů, 22 instancí (figure už má správnou třídu)
- [x] Přidat `class="img-center"` k 2 `<figure>` bez třídy (london-trip, whistler)
- [x] CSS: `figure { margin: 0; }` reset + `figcaption` styling (font-size, color, text-align)
- [x] CNK neklasifikované obrázky → `class="img-right"` float (2007-turecko: 10 img, 2006-pyreneje: 9 img)

### P4d — Migrace Blogger CDN obrázků na lokální hosting ✓
- [x] Stáhnout všechny obrázky z `blogger.googleusercontent.com` do `public/assets/migrated/blog/` — 90 obrázků
- [x] Aktualizovat HTML reference ve 27 blog archive souborech na lokální cesty — 93 referencí
- [x] Opravit `<a href="#">` na lightbox linky u 5 migrovaných obrázků
- [x] Migrační skript: `scripts/migrate-blogger-images.py`
- [x] Ověřeno: 0 zbývajících Blogger URL v archivu

### P4e — Screenshoty původního webu do Vault ✓
- [x] Udělat screenshoty klíčových sekcí původního webu — 6 stránek (homepage, fotky, cnk, cvut-fel, spse, blog)
- [x] Screenshoty pořízeny z živého webu michaltrs.net a blog.michaltrs.net pomocí Playwright
- [x] Přidány jako vault entry (2013-12-31, milestone) s popisem každé sekce
- [x] Uloženo v `public/assets/screenshots/` (6 JPG, celkem 1.7MB)

### P5 — Vault gap 2013–2026 ✓
- [x] Varianta C zvolena — bridge entry + jeden životní milník
- [x] 2012: "Teamleader a táta" — první syn + Ondra Vlček udělal teamleadera, obě role naráz (milestone)
- [x] 2014: "Éra sociálních sítí" — bridge entry s archive stránkou a odkazy na profily
- [x] Research sociálních sítí odložen na neurčito — launch neblokuje

### P6 — SEO & Open Graph ✓
- [x] Open Graph meta tagy (`og:type`, `og:url`, `og:title`, `og:description`, `og:image`, `og:locale`) v Layout.astro
- [x] Twitter Card meta tagy (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`)
- [x] OG image — 1200×630 JPG s headshotem, jménem a tagline (public/og-image.jpg)
- [x] robots.txt v public/ s odkazem na sitemap
- [x] Sitemap ověřena — 2 URL (/, /vault/)
- [x] Canonical URL na každé stránce
- [x] Vylepšen výchozí description

### P7 — Analytics ✓
- [x] Vybrat analytics řešení — Google Analytics 4 (G-GGVHEVQ5R4, převzato z www-2008-20)
- [x] Implementovat tracking script v Layout.astro — GA se načte až po cookie consent
- [x] Cookie consent banner — fixní spodní lišta, Přijmout/Odmítnout, localStorage pamatuje volbu

### P8 — Deployment: Cloudflare Pages ✓
- [x] ~~pipni.cz nepodporuje .htaccess, zastaralý TLS~~ → migrace na Cloudflare Pages
- [x] Cloudflare Pages: automatický build+deploy z GitHub, HTTPS zdarma, globální CDN (`homepage-dbb.pages.dev`)
- [x] Cloudflare: doména `michaltrs.net` — NS záznamy přepsány na Cloudflare, DNS propagováno
- [x] `michaltrs.net` běží na Cloudflare Pages s HTTPS
- [x] ~~Dočasný dual deploy na pipni.cz~~ — FTP workflow smazán (`.github/workflows/deploy.yml`)
- [x] ~~**Blogger: zrušit blog.michaltrs.net**~~ ✓

- [x] GitHub: smazat FTP secrets (`FTP_HOST`, `FTP_USERNAME`, `FTP_PASSWORD`) ✓
- [x] DNS cleanup: smazat `mail.michaltrs.net` A, starý `dkim._domainkey`, `_acme-challenge` záznamy
- [ ] **pipni.cz: vypovědět smlouvu** — formulář odeslán 2026-02-27, čeká na potvrzení
- [x] **Cloudflare: přidat www.michaltrs.net** jako custom domain v Pages → automatický 301 redirect na apex
- [x] **Cloudflare: Redirect Rule** pro `blog.michaltrs.net` → `https://michaltrs.net/vault/` (301) — viz P12a

### P9 — Responzivní testování & polish ✓
- [x] Otestovat mobil (Hero, foto grid, Vault timeline, archive stránky) — OK, vše responzivní
- [x] Otestovat tablet — OK
- [x] Opravit Vault subtitle (2006–2013 → 2001–2014)
- [x] Favicon ve více formátech — favicon.ico (16+32), apple-touch-icon.png (180), icon-192/512.png, site.webmanifest
- [x] Optimalizace archive obrázků — rozhodnuto nemigrovat na WebP (737 obrázků / 105 MB, největší 856 KB, neefektivní)
- Poznámka: mobilní navigace se láme na 2 řádky (kosmetické, funkční)

### P10 — Archive: konverze do Astro ✓
- [x] Vytvořit `ArchiveLayout.astro` — společný layout s header, footer, navigací, GA4, cookie consent
- [x] Konvertovat 136 archive-template HTML z `public/archive/` na Astro stránky v `src/pages/archive/`
- [x] 104 nested HTML (Doxygen, projekty) zůstává jako statické v `public/archive/` — nemají archive template
- [x] Přesunout archive CSS/JS (style.css, lightbox.js) do Astro layoutu přes `headContent` slot
- [x] Aktualizovat 168 odkazů ve vault entries a cross-referencích (`.html` → clean URL)
- [x] Odstranit 1 self-referencing link (36dbs)
- [x] Sitemap obsahuje 136 archive URL
- [x] Build: 139 stránek, 0 chyb
- [x] Migrační skripty: `scripts/migrate-archive-to-astro.py`, `scripts/fix-archive-links.py`

### Nemigrované — rozhodnuto: nemigrovat
- ~~Fotogalerie~~ — 15 galerií se stovkami fotek, nemigrujeme
- ~~Video~~ — nahrazeno YouTube linkem (P3)

### P11 — Revize kategorizace vault entries ✓
- [x] CNK — 17 blog postů přesunuto do blog (archiv na /archive/blog/)
- [x] ČVUT FEL — 5 blog postů přesunuto do blog + 1 opraven link (trailing slash) + kategorie blog
- [x] SPŠE — vše správně zařazeno, beze změn

### P12 — SEO: oprava chyb z Google Search Console

Stav ke 2026-04-14: 240 chybných stránek, indexovanost klesla z 81 → 19 za 6 týdnů.

#### P12a — Opravit 5xx Server Errors (38 stránek, Validation Failed) — KRITICKÉ ✓
- [x] **Cloudflare: přidat www.michaltrs.net** jako custom domain v Pages (bylo již Active)
- [x] **Cloudflare: Redirect Rule** `blog.michaltrs.net` → `https://michaltrs.net/vault/` (wildcard pattern, DNS A record 192.0.2.1 proxied)
  - Příčina: Blogger zrušen, ale redirect rule chybí → Cloudflare wildcard DNS zachytí request ale vrací 5xx
  - Po opravě by mělo zmizet ~38 stránek 5xx + ~48 canonical duplicit (www/non-www)

#### P12b — Opravit 404 Not Found (49 stránek)
- [ ] Zjistit konkrétní 404 URL ze Search Console (Coverage → Not found → Examples)
- [ ] Vytvořit `public/_redirects` s 301 přesměrováními pro staré vzory ze starého PHP webu
  - Typické vzory: `/fotky/`, staré PHP slugy, Blogger cesty přes michaltrs.net
- [ ] Po přidání redirects: Validate Fix v Search Console

#### P12c — Crawled not indexed (71 stránek)
- [ ] Zjistit které stránky Google crawloval ale neindexoval (Search Console → Examples)
  - Pravděpodobně `public/archive/cvut-fel/` Doxygen soubory (tenký obsah)
  - Zvážit přidání `noindex` nebo `Disallow` v robots.txt pro Doxygen podadresáře

#### P12d — Validate Fix a re-indexing
- [ ] Po opravě P12a: v Search Console kliknout "Validate Fix" na Server errors
- [ ] URL Inspection + Request Indexing pro `/` a `/vault/`
- [ ] Sledovat trend indexovanosti (cíl: zpět na 80+ stránek)

## Známé problémy
- `fast-xml-parser` je v dependencies ale potřeba jen pro migrační skripty
- ~~Blog archive stránky stále odkazují na externí Blogger/Google image URLs~~ — opraveno (P2)
- ~~Sitemap plugin nainstalován ale nefunkční (chybí `site`)~~ — opraveno, `site` nastaven
