---
name: xlab-new-project
description: Scaffold a new XLAB Cowork project in the current working folder — creates folder structure (inputs/outputs/done/references/skills), a customized CLAUDE.md, MEMORY.md, project instructions, change-log, and routes to the right XLAB skills. Asks a few short questions first. Use when starting or configuring a new Cowork project, or when the user says "založ projekt", "nastav projekt", "setup this project", "scaffold project".
---

# XLAB New Project

Set up a new XLAB Cowork project in the **current working folder**. Ask a few questions, then create the file structure and config so the project is ready to work in. Communicate in **Czech, briefly**.

## Step 0 — Confirm the folder

State which folder you'll set up (the current project folder) and confirm it's empty or new.
- If a `CLAUDE.md` already exists here → **stop and ask** before overwriting. Never blow away an existing config.
- Show a 5-item TODO so the user sees progress: 1) otázky 2) struktura složek 3) config soubory 4) routing skills 5) shrnutí + GUI kroky. Mark each done as you go.

## Step 1 — Ask (max 6 questions, in one go)

Check memory first — if you already know the answer, state it back, don't ask. Otherwise ask:

1. **Název projektu** (krátký, kebab-case pro složku).
2. **Účel** — jednou větou, co je cílem této složky.
3. **Typ** — vyber: `presale` / `nabídka (proposal)` / `tender` / `reporting` / `research` / `jiné`.
4. **Režim jazyka** — `kreativní` (živý, obrazný jazyk vítán — koncepty, scénáře, pitch) nebo `běžný` (věcný, klidný komunikační tón)? Default `běžný`.
5. **Vstupy** — co půjde do `inputs/` (např. PPTX briefy, maily, data)?
6. **Opakovaně?** — má z toho být i scheduled task (ano/ne, jak často)?

Keep it to these. If the user says "vyplň rozumně", proceed with sensible defaults.

## Step 2 — Create folder structure

In the current folder create:
```
inputs/        (read-only zdroje)
outputs/       (sem zapisuješ výstupy)
done/          (hotové)
references/    (trvalé reference, read-only)
skills/        (project-level skills, volitelně)
```
Add an empty `.gitkeep` to each so prázdné složky přežijí.

## Step 3 — Write config files

Write these files into the project root, **filled with the user's answers**:

### `CLAUDE.md`
Use this skeleton, doplň název/účel/typ:
```
# CLAUDE.md — Cowork projekt (XLAB): <NÁZEV>

## Kdo jsem
- Jindřich Trapl — CEO XLAB (kreativní tech / immersive eventy). Jazyk: česky.

## Co tenhle projekt dělá
<ÚČEL — jedna věta>

## Jazyk a tón
- Voice guide drží skill **xlab-content** — řiď se jím. Tenhle projekt je **<REŽIM>**.
- Kreativní → jazyk smí být živý a obrazný. Běžný → věcný a klidný, necháváme mluvit práci. (Superlativy ani v kreativním ne.)
- Píšeme pozitivně — popisujeme, co děláme. Vymezování „děláme X, ne Y" používej jen výjimečně.

## Jak pracovat
- Pracuj jen uvnitř této složky. Vstupy z inputs/ a references/, výstupy do outputs/, hotové do done/.
- Na konci úkolu připiš řádek do change-log.md (datum, co, soubory).
- Cituj zdroje (soubor/URL). Když si nejsi jistý zadáním, zeptej se.

## ⚠️ Bezpečnost souborů (SharePoint sync)
- Zdroje v inputs/ a references/ jsou read-only — neměň je.
- Zapisuj jen do outputs/, done/, change-log.md. Měníš výstup → verzuj (_v2) místo přepsání naslepo.
- Drž se uvnitř této složky. Odchozí akce (mail/3. strana) jen na pokyn. Chybí fakt → označ „TBD" a zeptej se.
```

### `MEMORY.md`
Seed se sekcemi: `## Stav`, `## Rozhodnutí`, `## Otevřené body`. Pozn. o ~200řádkovém capu.

### `PROJECT_INSTRUCTIONS.md`
Krátký text (elevator pitch projektu) k vložení do pole "Project Instructions" v Cowork UI. Odkaž na CLAUDE.md, na voice guide ve skillu xlab-content, na režim jazyka projektu, a na pravidla (česky, jen uvnitř složky, vstupy read-only).

### `change-log.md`
První řádek: `**[dnešní datum]** Projekt založen přes xlab-new-project.`

### `references/people.md`
Stub s Jindřich (CEO), místo pro klientské kontakty.

## Step 4 — Route to existing XLAB skills

Podle **Typu** řekni uživateli, které existující skills použít:
- `nabídka/proposal` → **xlab-proposal** (+ xlab-brand, xlab-pptx-template)
- `tender` → **xlab-tenders**
- `presale` → **xlab-events**, **xlab-pricing**, **xlab-locations**
- `reporting` → **xlab-content** / public `docx`/`xlsx`
- `research` → web search + **consolidate-memory**

Nepřepisuj je — jen nasměruj ("na tvorbu nabídky spusť /xlab-proposal").

## Step 5 — Wrap: GUI kroky (musí udělat uživatel)

Stručně připomeň 3 věci, které skill nemůže udělat za něj:
1. Pokud je složka v SharePointu → Finder → **"Always Keep on This Device"** (vypnout Files On-Demand), jinak hrozí tichá ztráta dat.
2. V Cowork appce vlož text z `PROJECT_INSTRUCTIONS.md` do pole **Project Instructions**.
3. Scheduled task (pokud chtěl) → přes `/schedule`.

Připiš řádek do `change-log.md` a ukonči krátkým: "Projekt <NÁZEV> je připravený."

## Ground rules
- Píš jen do **aktuální** projektové složky. Nikdy mimo ni.
- Existující soubory nepřepisuj bez dotazu.
- Jeden krok po druhém, krátké zprávy.
- Čeština. Tón věcný a přátelský — jazyk drž podle voice guide (xlab-content) a režimu projektu.
