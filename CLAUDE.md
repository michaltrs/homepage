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

### P2 — Formátování archive stránek
- [ ] Lepší zarovnání obrázků v textu (float, marginy, responzivita)
- [ ] Rozhodnout velikost obrázků — miniatury vs. plná velikost, max-width
- [ ] Sjednotit styling napříč všemi kategoriemi (blog, cnk, cvut-fel, spse-v-uzlabine)
- [ ] Vylepšit `public/archive/style.css` — typografie, spacing, mobilní zobrazení

### P3 — Cleanup
- [ ] Odstranit `updated:` field z 78 blog entries (není ve schema)
- [ ] Vyřešit 49 entries s prázdným `link: ""` (kosmetické)
- [ ] Vytvořit 404 stránku
- [ ] 6 foto placeholderů v PersonalSection (potřeba skutečné fotky)
- [ ] Professional foto/headshot (zatím SVG placeholder)

### Nemigrované (rozhodnout zda vůbec)
- [ ] Fotogalerie — 15 galerií se stovkami fotek (velký rozsah, možná nahradit odkazem na Google Photos/Flickr)
- [ ] Video — nahrazeno YouTube linkem (asi OK)

## Známé problémy
- `fast-xml-parser` je v dependencies ale potřeba jen pro migrační skripty
- ~~Blog archive stránky stále odkazují na externí Blogger/Google image URLs~~ — opraveno (P2)
- ~~Sitemap plugin nainstalován ale nefunkční (chybí `site`)~~ — opraveno, `site` nastaven
