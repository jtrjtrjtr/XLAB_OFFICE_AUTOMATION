# xlab-tenders — Design Rationale

## Zdroje vzorů

Skill byl navržen na základě analýzy 9 reálných výběrových řízení od 8 zadavatelů:

| # | Zadavatel | Typ | Jazyk | Klíčová specifika |
|---|-----------|-----|-------|-------------------|
| 1 | ČEZ | Framework tender (rámcová dohoda) | CZ | Nejvyšší složitost, obratový práh 50M CZK, sociální podnik, sankce |
| 2 | Škoda — Design Insight 2026 | Corporate RFQ | CZ/EN | VW Group Supply, day-rate pricing, Tissax, security |
| 3 | Škoda — Vision O | Corporate RFP (media agency) | EN | Schachzug zprostředkování, podrobný technický scope, org chart povinný |
| 4 | Roche — CDMA | Corporate RfP | CZ | Supplier Code of Conduct, 60-day payment, 90-day validity |
| 5 | RFI AI produkce (neidentifikovaný klient) | RFI + cenová nabídka | CZ | Jednoduchá struktura, 4 typy služeb, jednotkové ceny |
| 6 | E.ON | RFI (pool agentur) | CZ | Dvoukolový proces RFI→RFP, pool 2-4 agentur, 3 roky |
| 7 | PDS Vltavská filharmonie | VZMR | CZ | Tender arena, 3 hodnotící kritéria, reference s osvědčením |
| 8 | Česká televize — Dům ČT MFF KV | VZMR | CZ | eGORDION, vizualizace povinná, kvalita návrhu 40%, registr smluv |

## Identifikované vzory

### Dokumentová taxonomie (8 kategorií)

Všechny tendery, bez ohledu na zadavatele, obsahují dokumenty z těchto kategorií:
A) Cover/Invitation, B) Main specification, C) Pricing template, D) Qualification docs,
E) Contract draft, F) Compliance/Ethics, G) Technical annexes, H) Evaluation forms.

Některé tendery mají všech 8 (ČEZ, PDS), jiné jen 3-4 (RFI E.ON, Škoda RFQ).

### Kvalifikační vrstvy (5 úrovní)

Kvalifikace je vždy vícevrstvá, ale ne vždy jsou všechny vrstvy přítomny:

1. **Základní způsobilost** — přítomna vždy u VZMR, někdy implicitní u private
2. **Profesní způsobilost** — přítomna vždy
3. **Ekonomická kvalifikace** — nejčastější blocker (ČEZ: 50M, PDS: ne, ČT: ne)
4. **Technická kvalifikace** — reference + tým (přítomna vždy, liší se parametry)
5. **Compliance** — etické kodexy (Roche, RBI), sankce (ČEZ), NDA (Škoda)

### Hodnotící modely (3 archetypy)

1. **Cena dominantní** (60%+ váha na ceně) — ČT, některé VZMR
2. **Vyvážený** (40-50% cena, 40-50% kvalita/reference) — PDS, ČEZ
3. **Kvalita dominantní** (kreativní pitch rozhoduje) — Škoda Vision O, RFP fáze E.ON

### Procesní fáze (vždy stejná sekvence)

```
INTAKE → CLASSIFY → EXTRACT → GO/NO-GO → PLAN → PREPARE → CHECK → SUBMIT
```

Tato sekvence je invariantní. Liší se jen hloubka jednotlivých fází:
- RFI: lehký intake, žádná kvalifikace, rychlý output
- VZMR: plný průchod všemi fázemi
- Framework tender: nejhlubší analýza, nejdelší příprava

## Co se dá automatizovat

| Úloha | Míra automatizace | Poznámka |
|-------|-------------------|----------|
| Klasifikace dokumentů | 95% | Claude zvládne téměř vždy |
| Extrakce požadavků | 90% | Občas nejasné formulace vyžadují dotaz |
| Go/No-Go assessment | 70% | Claude doporučí, člověk rozhodne |
| Čestná prohlášení | 80% | Vyplnění šablony, podpis = člověk |
| Reference lists | 60% | Potřebuje zdroj dat (proposal_source.xlsx?) |
| Pricing strategy | 50% | Analýza vah + doporučení, čísla = člověk |
| Contract review | 40% | Zvýraznění rizik, právní posouzení = člověk |
| Kreativní obsah | 0% zde | Delegovat na xlab-events |

## Vztah k ostatním skillům

```
xlab-tenders (tento skill)
    ├── Fáze 1-3: Analýza + Go/No-Go
    │   (samostatně, bez jiných skillů)
    │
    ├── Fáze 4: Akční plán
    │   (samostatně, výstup = DOCX přes docx skill)
    │
    └── Fáze 5: Příprava podkladů
        ├── Kvalifikační docs → docx skill
        ├── Cenový template → xlsx skill + xlab-pricing
        ├── Kreativní nabídka → xlab-events → xlab-proposal
        └── Presentation → xlab-proposal
```

## Budoucí rozšíření

1. **Reference database** — napojení na proposal_source.xlsx nebo podobný zdroj
2. **Template library** — předpřipravené čestné prohlášení, krycí listy
3. **Competitor intelligence** — vzory pro odhad konkurence podle typu tenderu
4. **Win/loss tracking** — učení se z výsledků předchozích tendrů
