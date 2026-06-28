---
name: compound-memory
description: |
  Skill pro čerpání z XLAB znalostní báze (compound memory) a ukládání do ní.
  Znalostní báze obsahuje naše projekty, realizované akce, nabídky, technologie
  a tržní inspiraci — vše na jednom místě, prohledatelné přirozeným dotazem.
  Aktivuj tento skill, kdykoli Jindřich řekne nebo napíše jednu z těchto věcí:
  „použij XLAB knowledge base", „použij naši knowledge base", „použij compound
  memory", „použij naši paměť", „co víme o X", „co máme k X", „hoď inspiraci",
  „jaké technologie na X", „vypracuj koncept", „vypracuj nabídku s naší pamětí",
  „ulož do paměti", „ulož do knowledge base" nebo „tohle je naše nabídka".
  XLAB = jedna inspirace z mnoha — nepreferuje naše, jen označuje původ
  štítky [NAŠE]/[INSPIRACE]. Výstup je vždy jen draft, nikdy neodesílá.
---

# Compound Memory — XLAB znalostní paměť

Skill pro **čerpání** a **ukládání** v XLAB compound memory. Přístup je přes MCP
konektor **„XLAB Knowledge base"** (musí být v projektu připojený).

---

## Co tento skill umí

**Čerpání (retrieval)** — prohledá znalostní bázi a vrátí relevantní reference,
nápady nebo fakta:
- **Rychlá inspirace** — 5–8 nápadů z mixed poolu naše+trh, řazených podle relevance
- **Tech scouting** — jaké technologie, nástroje nebo platformy existují na dané téma
- **Koncept pro klienta** — strukturovaný kreativní návrh s precedenty a cross-pollination
- **Nabídka** — celý strukturovaný draft s referencemi, technikami a cenovou kotvou

**Ukládání (save)** — uloží nový dokument (nabídku, projekt, inspiraci) do znalostní
báze s korektní klasifikací (content_kind + provenance), aby byl dohledatelný příště.

**Klíčový princip:** XLAB je jedna inspirace z mnoha. Reference se řadí podle
**relevance**, ne podle původu. Každý výsledek je označen štítkem `[NAŠE]` (naše
projekty a nabídky) nebo `[INSPIRACE]` (tržní reference), aby Jindřich vždy věděl,
co je čí. Na vyžádání lze vyfiltrovat jen naše věci (`provenance=xlab`). Výstup
je vždy jen draft k doladění — skill nikdy nic neodesílá.

---

## Závislost

- Připojený konektor **„XLAB Knowledge base"** (MCP). Bez něj skill nefunguje.
- Klíčové nástroje konektoru: `search_knowledge` (čerpání, read-only) a
  `add_document` (ukládání, zapisuje na disk + indexuje).
- Když konektor není dostupný: „⚠ Konektor ‚XLAB Knowledge base' není připojený.
  Připoj ho v nastavení projektu."

---

## ČERPÁNÍ (retrieval)

Vždy **nejdřív zavolej `search_knowledge`** konektoru „XLAB Knowledge base".
Detekuj mód z formulace — **nedoptávej se zbytečně**.

### Štítkování původu (platí pro všechny módy)

- Každou referenci označ `[NAŠE]` (provenance `xlab` / `xlab_presale`) nebo
  `[INSPIRACE]` (provenance `industry`).
- **Neřaď naše dopředu, nedávej je jako důkaz.** Řadíš podle relevance.
- Na konci připomeň: „Chceš **jen naše**? Vyfiltruju `provenance=xlab`."
- **NIKDY neodesílej** — výstup je vždy draft k doladění.

### Mód A — Rychlá inspirace

Trigger: „hoď inspiraci", „nápady na X", „co bychom mohli dělat pro Y", „brainstorm".

0 otázek. Zavolej `search_knowledge` (mixed pool, bez pinování provenance):
```
search_knowledge(query="<sektor / klíčová slova> event aktivace originální nápady",
                 content_kind="deep-case-study", max_results=6, expand_graph=true)
```
Výstup: **5–8 nápadů** v jednom relevance-řazeném seznamu, každý se štítkem
`[NAŠE]`/`[INSPIRACE]`, + 1–2 „divoké kombinace" (cross-sector). Stručně, energicky.

### Mód B — Jaké technologie na X

Trigger: „jaká technologie na X", „co existuje na Y", „čím udělat Z", „tech scout".

0 otázek. Tři úhly:
```
search_knowledge(query="<téma> nástroj software platforma", content_kind="tech-knowhow", max_results=5)
search_knowledge(query="<téma> novinky trend aplikace", content_kind="ai-trend", max_results=4)
search_knowledge(query="<téma> case study nasazení event", content_kind="deep-case-study", max_results=3)
```
Výstup: nástroje & platformy → kde to někdo použil (se štítkem) → relevance pro XLAB.

### Mód C — Koncept pro klienta

Trigger: „vypracuj koncept", „připrav koncept pro klienta", „rozvij myšlenku", „navrhni aktivaci".

**Max 1–2 doptávací otázky**, pak koncept. Ptej se JEN když chybí kritická
informace (sektor / příležitost). Pak mixed-pool retrieval (deep-case-study,
bez pinování provenance) + jeden wildcard cross-sector dotaz. Výstup:
- **KONCEPT** (4–6 vět, příběh — ne výčet techniky)
- **Opřeno o reference** — relevance-řazené, štítky `[NAŠE]`/`[INSPIRACE]`, filepath
- **Cross-pollination** — 1–2 nečekané nápady z jiných sektorů
- **Navrhovaný postup** (schválit → scoping → rozvinout do nabídky)

### Mód D — Vypracuj nabídku

Trigger: „vypracuj nabídku", „připrav nabídku pro klienta", „draft proposal", „brief v příloze".

Strukturovaný draft. Max 1–2 otázky jen když chybí sektor/formát. Retrieval =
mixed pool (deep-case-study + tech-knowhow na feasibility), **bez pinování
provenance**. Struktura draftu:
- Hlavička: `_Draft — k doladění. Neposlat bez schválení._`
- **KONCEPT** (příběh, co je překvapivé)
- **REFERENCE A INSPIRACE** — jeden relevance-řazený seznam, štítky původu,
  filepath; **ne naše-první, žádná NAŠE-kvóta**
- **NAVRŽENÉ TECHNIKY** (technika | proč | feasibilita)
- **CENOVÁ KOTVA** (volitelně — naše i tržní reference, nepinuj jen na xlab)
- **DOPORUČENÝ POSTUP**

### GOOD doptávací otázky (mód C/D, max 1–2)

Navrhni 2–3, vyber max 2 nejdůležitější. Dobré osy:
- **Míra kreativity:** „Bezpečně z naší praxe, nebo překvapivá divočina?"
- **Jazyk výstupu:** „Czech nebo English?"
- **Sektor / formát** — JEN když úplně chybí v briefu.

Nikdy se neptej na interní taxonomii (police, content_kind, provenance).

---

## UKLÁDÁNÍ (save)

Když Jindřich řekne **„ulož do paměti", „přidej do KB", „tohle je naše nabídka"**,
zavolej `add_document` konektoru „XLAB Knowledge base".

**TY klasifikuješ** (server heuristiku neřeš — frontmatter od volajícího vyhrává;
klasifikátor sám NIKDY nenastaví `xlab_presale`):

1. Přečti obsah, vyber:
   - `content_kind`: `deep-case-study` (rozpracovaná nabídka / case study),
     `case-study`, `tech-knowhow`, `ai-trend`, `playbook`, `dataset`
   - `provenance` (dle decision #635):
     - `xlab_presale` — **naše nabídka / pitch** (rozpracované, ještě nedodané)
     - `xlab` — **naše dodaná práce** (realizovaný projekt)
     - `industry` — **externí inspirace** (cizí reference)
   - `sector` / `technika` / `mood` — pokud je signál (jinak vynech)

2. Zavolej `add_document` s obsahem + prepended frontmatter blokem:
   ```yaml
   ---
   content_kind: <tvá volba>
   provenance: <xlab_presale | xlab | industry>
   sector: <sektor nebo vynech>
   technika: [<seznam nebo vynech>]
   mood: <mood nebo vynech>
   added_by: jindrich.trapl
   source_write: skill-compound-memory
   ---
   ```
   - `filepath`: relativní cesta dle původu — pro externí inspiraci `wiki/sources/...`.
   - Nepředávej prázdnou/špatnou kategorii.

3. Potvrď: „Uloženo jako `<content_kind>` / `<provenance>` do `<filepath>`."

**Mapování fráze → provenance:**
| Jindřich řekne | provenance |
|---|---|
| „tohle je naše nabídka / náš pitch" | `xlab_presale` |
| „tohle jsme dodali / náš hotový projekt" | `xlab` |
| „tohle je inspirace z trhu / cizí reference" | `industry` |

---

## GUARDRAILS

- **Nikdy neodesílej, neposílej, nepřeposílej** — výstup je vždy draft.
- **XLAB = jedna inspirace z mnoha** — neřaď naše dopředu, nedávej je jako důkaz.
  Relevance rozhoduje; štítek jen ukazuje původ.
- **Nikdy necituj `content_kind: session-note`** — interní paměť, ne klientská inspirace.
- **Neprozrazuj** interní náklady, ceny dodavatelů, post-mortem poznámky.
- **Necommituj cenu** — kotva je orientační rozsah z historie, ne nabídka.
- **Neptej se na police/content_kind/provenance** — Jindřicha interní taxonomie nezajímá.
- Tento skill píše do paměti JEN přes `add_document`. Nikdy nevolá reindex.
- Vyžaduje připojený konektor **„XLAB Knowledge base"**.
