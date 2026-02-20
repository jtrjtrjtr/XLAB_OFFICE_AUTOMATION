# XLAB Skills Manual

Přehled všech custom skillů, jejich módů, triggerů a scénářů použití.

Verze: 1.0 | Datum: 20. 2. 2026

---

## Obsah

1. Přehled skillů a routování
2. xlab-brand — Vizuální identita
3. xlab-content — Texty a brand voice
4. xlab-pricing — Cenové kalkulace
5. xlab-pptx-template — Prezentace z šablony
6. xlab-proposal — Klientské nabídky
7. Matice scénářů: Co říct, aby se aktivovalo co
8. Technické poznámky

---

## 1. Přehled skillů a routování

XLAB ekosystém tvoří pět propojených skillů. Každý má svůj účel a jasné hranice.

| Skill | Účel | Výstup |
|-------|------|--------|
| **xlab-brand** | Vizuální identita (barvy, fonty, loga, pravidla) | Podkladový skill — sám nic negeneruje, používají ho ostatní |
| **xlab-content** | Texty, brand voice, produktové portfolio | Texty v CZ/EN |
| **xlab-pricing** | Cenové kalkulace eventů | Excel (.xlsx) |
| **xlab-pptx-template** | Interní prezentace z XLAB šablony | PowerPoint (.pptx) |
| **xlab-proposal** | Klientské nabídky/propozály | PowerPoint (.pptx) |

### Rozhodovací strom — Co chci vytvořit?

```
Potřebuji...
├── cenovou kalkulaci / nacenit event → xlab-pricing
├── nabídku / proposal / pitch deck pro klienta → xlab-proposal
├── interní prezentaci s XLAB brandem → xlab-pptx-template
├── obecnou prezentaci bez XLAB brandu → veřejný pptx skill
├── napsat text pro XLAB (web, social, email, PR) → xlab-content
└── vizuální pravidla, barvy, loga → xlab-brand
```

### Závislosti mezi skilly

```
xlab-proposal
├── xlab-brand (barvy, loga, témata)
└── xlab-pptx-template (cover + closing slide)

xlab-pptx-template
└── xlab-brand (pravidla pro BLACK/WHITE téma)

xlab-pricing
└── xlab-brand (logo do Excelu)

xlab-content
└── xlab-brand (doporučeno — pro vizuální výstupy)
```

---

## 2. xlab-brand — Vizuální identita

### Kdy se aktivuje

Automaticky, kdykoliv jiný skill potřebuje vizuální prvky XLAB. Sám o sobě se spouští, když uživatel potřebuje informace o brandingu — barvy, loga, pravidla.

### Co obsahuje

- **Barevné schéma**: XLAB Black (#000000), XLAB White (#F8F7F2), Neon Yellow (#E3E829), Mid Gray (#4a4a4a), Dark Gray (#1a1a1a), Light Gray (#888888)
- **Typografie**: GT America (fallback: Arial)
- **Logotypy**: X symbol (white/black), XLAB logo (white/black) — uložené jako base64 v `extract_assets.py`
- **Dvě témata**: BLACK (výchozí) a WHITE

### Klíčová pravidla

- Žlutá (#E3E829) se **nikdy** nepoužívá jako pozadí nebo gradient
- Na bílém podkladu je žlutá **pouze** dekorativní (linky, pruhy) — nikdy pro text
- X symbol má poměr stran **1.6:1** — nikdy čtverec
- X symbol je na **každém** slidu **kromě coveru** (vpravo dole)
- Na coveru je X symbol **zakázán**

### Dva režimy tématu

| Vlastnost | BLACK (výchozí) | WHITE |
|-----------|-----------------|-------|
| Pozadí | #000000 | #F8F7F2 |
| Text | #F8F7F2 | #1A1A1A |
| Accent | #E3E829 (overlines, ikony, čísla) | #E3E829 (pouze dekorativní linky) |
| Karty | #1A1A1A | #EBEBEB |
| X symbol | bílý | černý |

### Jak přepnout téma

Řekněte: "bílé téma" / "white theme" / "světlý vzhled". Výchozí je vždy černé.

---

## 3. xlab-content — Texty a brand voice

### Kdy se aktivuje

Kdykoliv píšete text nesoucí jméno XLAB — web, social media, nabídky, emaily, tiskové zprávy, prezentační obsah.

### Triggery

- "napiš text pro XLAB"
- "připrav příspěvek na sociální sítě"
- "přelož do angličtiny" (u XLAB textů)
- "zkontroluj, jestli text odpovídá brand voice"
- "napiš popis služby"
- "připrav newsletter"

### Dva komunikační módy

#### Communication Mode (výchozí)

**Kdy se aktivuje:** Automaticky pro veškerou klient-facing a marketingovou komunikaci.

**Platí pro:** web, sociální sítě, nabídky, tiskové zprávy, emaily, popisy služeb, klientské dokumenty.

**Pravidla:**
- Faktický, přesný, žádné superlativy
- Žádné marketingové fráze ("unikátní", "komplexní řešení", "inovativní přístup")
- Žádné emocionální přehánění ("zbožňujeme", "jsme posedlí", "s hrdostí")
- Žádné vykřičníky, emoji, tři tečky
- Věty 10–20 slov, odstavce 2–3 věty
- Český text: "videomapping", "imerzivní", "kreativní design"
- Anglický text: "projection mapping", "immersive", "creative design"

**Příklad správného textu:**
> XLAB navrhuje a produkuje eventy, vizuální show, holografické instalace a imerzivní prostory. Působíme od roku 1998.

#### Creative Mode

**Kdy se aktivuje:** Automaticky, když uživatel žádá kreativní práci — koncepty, scénáře, pitch nápady.

**Platí pro:** kreativní koncepty, show scénáře, dramaturgické skripty, moodboardy, pitch decky (prodej nápadu), umělecké briefy, mapping storyboardy.

**Uvolněná pravidla:**
- Jazyk **může** být živý, poetický, atmosférický, emocionálně expresivní
- Obrazy a metafory jsou vítány: "fasáda se rozpouští ve světle", "prostor dýchá s publikem"
- Superlativy **zůstávají zakázané** — i v kreativním módu XLAB nekřičí
- Jádro identity zůstává: klidná sebejistota, žádné vykřičníky, žádné emoji

**Klíčový rozdíl:** Communication mode popisuje, co děláme. Creative mode představuje, jak něco může působit.

### Jak přepnout mód

| Chci... | Řeknu... | Aktivuje se... |
|---------|----------|----------------|
| Web copy, popis služby | "napiš text pro web" | Communication Mode |
| Newsletter | "připrav newsletter" | Communication Mode (teplejší tón) |
| Kreativní koncept | "připrav koncept pro show" | Creative Mode |
| Pitch idea | "napiš pitch pro klienta na mapping" | Creative Mode |
| Kontrola textu | "zkontroluj tenhle text" | Communication Mode (jako referenční) |

### Produktové portfolio (6 oblastí)

Skill obsahuje kompletní popisy v CZ i EN pro všech 6 oblastí:

1. **Eventy & Produkce** — firemní, kulturní, sportovní, multimediální
2. **Videomapping / Projection Mapping** — architektonický, interiérový, objektový, umělecký
3. **Digitální lidé & AI avatary** — virtuální moderátoři, vzdělávací avatary, brand asistenti
4. **Holografický zážitek** — Holobox, stage hologram, teleport, holovějíř
5. **Imerzivní prostředí** — místnosti, tunely, LED instalace, dome
6. **Interaktivní instalace** — gesta, dotyk, mobil, AR, generativní art

---

## 4. xlab-pricing — Cenové kalkulace

### Kdy se aktivuje

Kdykoliv potřebujete nacenit event nebo projekt.

### Triggery

- "kalkulace", "cenová kalkulace", "pricing", "cost estimate", "budget"
- "kolik by stálo...", "nacenit", "připravit ceny"
- "kalkulace pro konferenci", "nacenit gala večer"

### Dva režimy

#### Standard Mode (výchozí)

**Kdy se aktivuje:** Automaticky — čerpá z přibaleného ceníku v5.

**Jak funguje:**
1. Uživatel popíše event (typ, délka, rozsah, speciální požadavky)
2. Claude vybere nejbližší alokační šablonu
3. Mapuje položky na ceník
4. Spustí výpočetní script → Excel

**Alokační šablony (7 typů):**

| Šablona | Klíčová slova |
|---------|---------------|
| Tisková konference | tiskovka, TK, press |
| Střední Event | event, akce, středně velká |
| Gala / Winter Meeting | gala, večírek, ples |
| Mezinárodní aktivace | F1, international, aktivace |
| Konference (Ventuz) | konference, conference, Ventuz |
| HoloBox | holobox, hologram, avatar |
| Dealer Meeting | dealer meeting, full service |

**Cenové úrovně:**

| Tier | Násobek |
|------|---------|
| Nákladová | interní cost |
| Snížená/Partner | Standard × 0.80 |
| Standard | 100 % |
| Premium | Standard × 1.20 |

#### Freeform Mode

**Kdy se aktivuje:** Když projekt neodpovídá standardnímu ceníku.

**Triggery:**
- "kalkulace bez ceníku"
- "vlastní ceny"
- "freeform"
- "nestandardní projekt"

**Jak funguje:** Uživatel zadá všechny položky s vlastními cenami. Stejný Excel design, jen bez automatického vyhledávání v ceníku.

### Pojmenování výstupních souborů

Formát: `CE_{JobNr}_{Klient}_{Projekt}_v01.xlsx`

Před generováním se Claude zeptá na:
- **Job Nr.** (číslo zakázky)
- **Klient** (název klienta)
- **Projekt** (název projektu/eventu)

### Klíčová pravidla

- Všechny personální sazby v ceníku jsou **hodinové**
- On-site role: výchozí = osoby × 9 hodin/den
- Tech progrese: 2 dny = 1.5×, 3 dny = 2×, 5 dní = 3×
- Zaokrouhlení: ≥200 CZK → na 50, <200 → celá čísla
- Max sleva: 20 %, platí pouze na Techniku
- EUR = Standard ÷ 25

---

## 5. xlab-pptx-template — Prezentace z šablony

### Kdy se aktivuje

Pro **interní** XLAB prezentace — ne nabídky, ne obecné prezentace.

### Triggery

- "udělej prezentaci z XLAB šablony"
- "interní prezentace", "branded prezentace"
- "prezentace pro interní meeting"

### Co NEPOUŽÍVAT pro

- Nabídky/propozály → `xlab-proposal`
- Obecné prezentace bez XLAB → veřejný `pptx` skill

### Technický princip

Pracuje s šablonou `XLAB_PPT_ALL.pptx`, která obsahuje 30 layoutů (15 BLACK + 15 WHITE). Slidy se vytvářejí z layoutů pomocí XML manipulace (unpack → add_slide → edit XML → pack).

### Dostupné layouty (15 v každém tématu)

| Layout | Název | Účel |
|--------|-------|------|
| 1 / 16 | Cover + X Ray | Úvodní slide — **vždy první** |
| 2 / 17 | Title + Text | Klasický textový slide |
| 3 / 18 | Title + Text + IMG | Text vlevo, obrázek vpravo |
| 4 / 19 | Title + Text + 4× IMG | Text + 4 obrázky (varianta A) |
| 5 / 20 | Title + Text + 4× IMG+ | Text + 4 obrázky (varianta B) |
| 6 / 21 | Title + Text + 2× IMG | Text + 2 obrázky |
| 7 / 22 | Title + Text + IMG horizontal | Horizontální varianta |
| 8 / 23 | Title + IMG horizontal | Titulek + velký obrázek |
| 9 / 24 | Full Screen IMG | Celá plocha obrázek |
| 10 / 25 | Title + Text + IMG 4 mask | Obrázek s maskováním |
| 11 / 26 | Gradient Mask | Dekorativní přechod (bez textu) |
| 12 / 27 | Title Section + Ray Logo | Sekční dělič s X logem |
| 13 / 28 | Title Section No Ray | Sekční dělič bez loga |
| 14 / 29 | Cover No Ray | Alternativní úvod |
| 15 / 30 | Bye Bye Slide | Závěrečný slide — **vždy poslední** |

### Pravidla

- **Vždy začni** Layoutem 1 (Cover) a **skonči** Layoutem 15 (Bye Bye)
- Výchozí je **černé téma** (Layouts 1–15) — bílé pouze na explicitní přání
- Nikdy neupravuj přímo originální šablonu — vždy kopie
- Dekorativní prvky (X ray, zelená linie, loga) jsou součástí layoutů — nekreslí se ručně

---

## 6. xlab-proposal — Klientské nabídky

### Kdy se aktivuje

Pro klientské nabídky, pitch decky a propozály.

### Triggery

- "nabídka", "proposal", "pitch deck", "offer"
- "nabídka pro klienta XY"
- "připrav propozál pro mapping projekt"

### Technický princip (Cesta C)

Hybridní přístup — kombinuje dva zdroje:
1. **Cover + Closing** se extrahují z XLAB_PPT_ALL šablony (xlab-pptx-template)
2. **Content slidy** se generují programaticky přes **pptxgenjs** (Node.js)
3. **Merge script** je spojí do jednoho souboru

```
Template (XLAB_PPT_ALL.pptx) → Cover slide (Layout 1) + Closing slide (Layout 15)
                                         ↓
pptxgenjs → Content slidy (2 až N-1)     ↓
                                         ↓
merge_proposal.py → Finální PPTX
```

### Dvě varianty struktury

#### Compact (6–8 slidů)

Pro menší projekty, rychlé nabídky, follow-up propozály.

| # | Sekce | Komponenta |
|---|-------|------------|
| 1 | Cover | z šablony |
| 2 | Kontext / prostor | text-with-image nebo quote-highlight |
| 3 | Kreativní koncept | 3-column-cards |
| 4 | Technické řešení | detail-with-panel |
| 5 | Harmonogram | timeline |
| 6 | Rozpočet | pricing-simple nebo pricing-table |
| 7 | Otevřené otázky | checklist |
| 8 | Closing | z šablony |

#### Extended (12+ slidů)

Pro větší projekty, nové klienty, komplexní vícefázové nabídky.

| # | Sekce | Komponenta |
|---|-------|------------|
| 1 | Cover | z šablony |
| 2 | Executive summary | quote-highlight |
| 3 | Reference | image-fullbleed |
| 4 | Porozumění zadání | text-with-image nebo checklist |
| 5 | Kreativní vize | quote-highlight nebo big-number |
| 6 | Kreativní koncept — fáze | 3-column-cards |
| 7 | Kreativní koncept — detail | detail-with-panel (1–2 slidy) |
| 8 | Technické řešení | detail-with-panel |
| 9 | Volitelná rozšíření | 3-column-cards nebo checklist |
| 10 | Realizační tým | team |
| 11 | Harmonogram | timeline |
| 12 | Cenové varianty | pricing-table nebo pricing-simple |
| 13 | Otevřené otázky | checklist |
| 14 | Closing | z šablony |

### Jak přepnout variantu

| Řeknu... | Aktivuje se... |
|----------|----------------|
| "krátká nabídka", "quick proposal", "compact" | Compact (6–8 slidů) |
| "rozšířená nabídka", "detailní proposal", "extended" | Extended (12+ slidů) |
| "nabídka" (bez upřesnění) | Claude se zeptá nebo odhadne podle rozsahu projektu |

### Knihovna komponent (content slidy)

| Komponenta | Účel | Typické použití |
|------------|------|-----------------|
| **3-column-cards** | Tři karty vedle sebe | Fáze, kroky, porovnání, varianty |
| **detail-with-panel** | Body vlevo, info panel vpravo | Technické řešení, specifikace |
| **text-with-image** | Text + obrázek | Kontext, popis prostoru |
| **pricing-table** | Tři cenové sloupce (prostřední zvýrazněný) | Cenové varianty |
| **pricing-simple** | Jednoduchý ceník s řádky | Přímočarý rozpočet |
| **checklist** | Řádky se žlutým pruhem | Otevřené otázky, požadavky |
| **timeline** | Horizontální časová osa | Harmonogram |
| **big-number** | 2–3 velká čísla | Klíčové statistiky, parametry |
| **quote-highlight** | Velký citát se žlutým pruhem | Executive summary, vize |
| **image-fullbleed** | Celostránkový obrázek s textem | Reference, vizuální přechod |
| **team** | Členové týmu s fotkou | Realizační tým |
| **two-column-text** | Dva textové sloupce | Porovnání, dvojí perspektiva |
| **diagram-with-labels** | Diagram nahoře, popisky dole | Technická schémata |

### Téma nabídky

Stejné BLACK/WHITE téma jako u ostatních skillů. Nastavuje se globálně pro celou nabídku. Cover a closing vždy používají styling šablony.

---

## 7. Matice scénářů: Co říct, aby se aktivovalo co

### Jednoduché scénáře

| Chci... | Řeknu... | Aktivuje se... |
|---------|----------|----------------|
| Nacenit event | "nacenit konferenci pro 200 lidí" | xlab-pricing (Standard) |
| Nacenit nestandardní projekt | "kalkulace bez ceníku, vlastní ceny" | xlab-pricing (Freeform) |
| Nabídku pro klienta | "nabídka pro BMW na mapping" | xlab-proposal + xlab-brand + xlab-pptx-template |
| Interní prezentaci | "prezentace z XLAB šablony" | xlab-pptx-template + xlab-brand |
| Text na web | "napiš text o videomappingu pro web" | xlab-content (Communication) + xlab-brand |
| Kreativní koncept | "připrav koncept pro show" | xlab-content (Creative) |
| Obecnou prezentaci | "udělej prezentaci o AI trendech" | veřejný pptx skill (bez XLAB) |

### Kombinované scénáře

| Scénář | Řeknu... | Aktivuje se... |
|--------|----------|----------------|
| Kompletní nabídka s cenou | "nabídka pro VISA včetně kalkulace" | xlab-proposal + xlab-pricing |
| Nabídka s kreativním konceptem | "pitch deck s kreativním konceptem pro mapping" | xlab-proposal (Creative mode obsah) |
| Newsletter s produkty | "newsletter o hologramech" | xlab-content (Communication, newsletter tón) |
| Překlad nabídky | "přelož nabídku do angličtiny" | xlab-content (terminologie CZ→EN) |

### Přepínání témat a variant

| Chci... | Řeknu... |
|---------|----------|
| Černé téma (výchozí) | nic — je automatické |
| Bílé téma | "bílé téma", "white theme", "světlý vzhled" |
| Compact nabídku | "krátká nabídka", "compact", "quick proposal" |
| Extended nabídku | "rozšířená nabídka", "extended", "detailní" |
| Communication mode text | nic — je automatický pro client-facing |
| Creative mode text | "koncept", "scénář", "pitch nápadu", "storyboard" |
| Freeform kalkulaci | "bez ceníku", "vlastní ceny", "freeform" |

---

## 8. Technické poznámky

### Generování prezentací — dva různé přístupy

V ekosystému existují **dva odlišné způsoby**, jak se generují PPTX soubory:

#### A) XML manipulace (xlab-pptx-template)

Používá se pro **interní prezentace**. Pracuje přímo s XML soubory uvnitř PPTX archivu.

```
XLAB_PPT_ALL.pptx → unpack → add_slide z layoutu → edit XML → clean → pack → výstup
```

- Všechny dekorativní prvky (X ray, zelená linie, loga) se dědí z layoutu automaticky
- Omezeno na layouty, které šablona obsahuje
- Ideální, když chcete přesnou replikaci XLAB šablony

#### B) pptxgenjs + merge (xlab-proposal)

Používá se pro **klientské nabídky**. Kombinuje šablonové slidy s programaticky generovanými.

```
XLAB_PPT_ALL.pptx → cover + closing (XML)
pptxgenjs → content slidy (Node.js)
merge_proposal.py → spojení do jednoho souboru
```

- Cover a closing přesně podle šablony
- Content slidy plně programatické — flexibilní layout
- Merge script řeší layout contamination (blank layout injection)
- Ideální pro dynamický obsah s konzistentním obalem

### Formáty výstupů

| Skill | Výstupní formát | Pojmenování |
|-------|----------------|-------------|
| xlab-pricing | .xlsx | `CE_{JobNr}_{Klient}_{Projekt}_v01.xlsx` |
| xlab-pptx-template | .pptx | dle projektu |
| xlab-proposal | .pptx | `proposal.pptx` (nebo dle projektu) |
| xlab-content | text (v chatu, nebo .md/.docx) | dle potřeby |

### Assets a loga

Všechny brand assety jsou zakódované v base64 ve scriptu `extract_assets.py`. Před použitím se vždy musí extrahovat:

```bash
python3 /mnt/skills/user/xlab-brand/scripts/extract_assets.py /tmp/xlab-assets
```

Výsledek:
- `x_symbol_white.png` — X symbol na tmavém pozadí
- `x_symbol_black.png` — X symbol na světlém pozadí
- `x_logo_white.png` — plný XLAB logotyp, tmavé pozadí
- `x_logo_black.png` — plný XLAB logotyp, světlé pozadí

Všechny PNG s průhledným pozadím (RGBA).

### QA proces (nabídky)

Po vygenerování nabídky se vždy provádí vizuální kontrola:

1. Konverze PPTX → PDF → JPEG
2. Kontrola každého slidu: overflow textu, překryvy, správné barvy, X symbol, čísla stránek
3. Oprava a re-verifikace

---

*Tento manuál slouží jako referenční dokument pro práci s XLAB skill ekosystémem. Při distribuci dalším uživatelům nebo převodu do pluginu z něj vycházejte jako z definice uživatelského rozhraní a očekávaného chování.*
