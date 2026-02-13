# Projekt: michaltrs-hp-astro

Osobní web Michala Trse. Astro 5 + Tailwind v4, statický build. Migrováno ze starého PHP webu (www-2008-20/).

## Architektura

- **2 stránky**: index.astro (homepage), vault.astro (timeline archiv)
- **1 content collection**: vault (195 entries, 5 kategorií: news, blog, cnk, cvut-fel, spse-v-uzlabine)
- **Archive HTML**: statické stránky v public/archive/ (blog 78, cvut-fel 37, spse-v-uzlabine 8, cnk 11)
- **Migrace hotové**: ČVUT FEL (kompletní), SPŠE (kompletní), Blog (z Bloggeru), News (z RSS), CNK (kompletní)

## Plán práce

### P1 — Quick wins ✓
- [x] Opravit Lorem ipsum v Hero.astro (subtitle)
- [x] Vytvořit favicon.svg (Layout.astro ho linkuje ale soubor neexistuje)
- [x] Nastavit `site` v astro.config.mjs (sitemap nefunguje)
- [x] Opravit broken linky ve vault entries — 8 CNK entries opraveno na `/archive/cnk/...` cesty

### P1 — Design & obsah Hero stránky ✓
- [x] Začistit design Hero sekce — layout, typografie, barvy, CTA tlačítka
- [x] Vybrat lepší Vault items na Hero page (VaultSummary) — 4 milníky (SPŠE, CNK, ČVUT, Blog)
- [x] Implementace sociálních odkazů (YouTube, Instagram, Facebook, LinkedIn, Strava, Podcast)

### P1 — Vault gap 2013–2026 (odloženo)
- [ ] Vyřešit co s Vault od roku 2013 do současnosti — 13 let prázdného období
- [ ] Rozhodnout: doplnit zpětně klíčové milníky? Přidat novou kategorii? Napojit na aktuální obsah?

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

### P3b — Remaining cleanup
- [x] Odstranit `updated:` field z 78 blog entries (není ve schema)
- [x] Vyřešit 49 entries s prázdným `link: ""` (kosmetické)
- [x] Vytvořit 404 stránku
- [ ] 6 foto placeholderů v PersonalSection (potřeba skutečné fotky)
- [ ] Professional foto/headshot (zatím SVG placeholder)

### P4b — Archive: validace obsahu a odkazů ✓
- [x] Ověřit že všechny embed obrázky se načítají (žádné broken images) — 9 broken → 0 (imb-cvut cesty opraveny, silvretta panorama nahrazeno)
- [x] Ověřit že všechny embed videa fungují (YouTube iframes, ne dead Flash/placeholder) — 19 YouTube embeds OK, 0 broken
- [x] Konkrétně zkontrolovat video z USA národních parků (2011-08-09 entries) — doplněn YouTube embed (vBWIuTHdDqI)
- [x] Opravit nalezené broken obrázky a videa
- [x] Zkontrolovat všechny externí odkazy ve všech archive stránkách — 361 URL zkontrolováno (122 živých, 142 přesměrovaných, 97 mrtvých)
- [x] Mrtvé odkazy nahradit `<span class="dead-link">` — 79 nahrazení v 56 souborech, `.dead-link` CSS přidáno
- [x] Validační skript: `scripts/validate-archive.py` (238 HTML, report + link-history.md)
- [x] `link-history.md` — kompletní seznam 289 externích odkazů seskupený po stránkách

### P4c — Archive: obtékání obrázků a videí
- [ ] Projít všechny archive stránky (blog, cnk, cvut-fel, spse-v-uzlabine) a vylepšit obtékání obrázků textem
- [ ] Zkontrolovat a opravit responsivitu obrázků (float, marginy, clearing)
- [ ] Vylepšit umístění a obtékání embedded videí
- [ ] Ověřit konzistenci napříč kategoriemi

### P5 — Vault gap 2013–2026: research sociálních sítí
- [ ] Research Facebook — významné události, fotky, milníky k doplnění do timeline
- [ ] Research LinkedIn — kariérní milníky, pozice, projekty
- [ ] Research Instagram — fotky z cest a událostí
- [ ] Research Strava — významné cyklo/běžecké výkony, statistiky
- [ ] Na základě researche doplnit vault entries pro období 2013–2026

### Nemigrované (rozhodnout zda vůbec)
- [ ] Fotogalerie — 15 galerií se stovkami fotek (velký rozsah, možná nahradit odkazem na Google Photos/Flickr)
- [ ] ~~Video — nahrazeno YouTube linkem (asi OK)~~ — hotovo (P3)

## Známé problémy
- `fast-xml-parser` je v dependencies ale potřeba jen pro migrační skripty
- ~~Blog archive stránky stále odkazují na externí Blogger/Google image URLs~~ — opraveno (P2)
- ~~Sitemap plugin nainstalován ale nefunkční (chybí `site`)~~ — opraveno, `site` nastaven
