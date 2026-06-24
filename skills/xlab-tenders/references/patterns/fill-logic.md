# Fill Logic — Pravidla pro vyplňování šablon

## Rozhodovací strom

```
Tender požaduje dokument X
    │
    ├── Zadavatel POSKYTL šablonu pro X?
    │   ├── ANO → Použij zadavatelovu šablonu
    │   │         Vyplň údaje z company-data.md
    │   │         Vypiš co zůstalo nevyplněné
    │   │         Generuj DOCX
    │   │
    │   └── NE → Existuje šablona v templates/?
    │       ├── ANO → Použij šablonu z templates/
    │       │         Adaptuj na specifika tenderu
    │       │         Vyplň údaje z company-data.md
    │       │         Generuj DOCX
    │       │
    │       └── NE → Upozorni uživatele
    │                 Navrhni obsah a strukturu
    │                 Po potvrzení generuj DOCX
```

## Mapování placeholder → zdroj

### Automaticky vyplnitelné (bez dotazu na uživatele)

| Placeholder | Zdroj | Příklad |
|-------------|-------|---------|
| `{{FIRMA}}` | company-data.md → FIRMA | XLAB s.r.o. |
| `{{SIDLO}}` | company-data.md → SIDLO | Příčná 1892/4, 110 00 Praha 1 |
| `{{ICO}}` | company-data.md → ICO | 12345678 |
| `{{DIC}}` | company-data.md → DIC | CZ12345678 |
| `{{OR_ZAPIS}}` | company-data.md → OR_ZAPIS | zapsaná v OR vedeném MS v Praze, C 12345 |
| `{{JEDNATEL_1}}` | company-data.md → JEDNATEL_1 | Ing. Jan Novák |
| `{{DATOVA_SCHRANKA}}` | company-data.md → DATOVA_SCHRANKA | abc1234 |
| `{{DATUM}}` | aktuální datum | 12. 3. 2026 |
| `{{ZAKAZKA}}` | tender header card | Dům ČT – MFF Karlovy Vary 2026 |
| `{{ZADAVATEL_NAZEV}}` | tender header card | Česká televize |

### Vyžadují dotaz na uživatele

| Placeholder | Proč | Jak se zeptat |
|-------------|------|---------------|
| `{{CENA_BEZ_DPH}}` | Strategické rozhodnutí | "Jakou nabídkovou cenu chceš uvést?" |
| `{{TEAM_N_JMENO}}` | Aktuální dostupnost | "Kdo bude v realizačním týmu?" |
| `{{REF_N_*}}` | Výběr z databáze | "Navrhuji tyto reference: [seznam]. Souhlasíš?" |

### Odvozené (Claude vypočítá)

| Placeholder | Odvozeno z |
|-------------|-----------|
| `{{DPH}}` | `{{CENA_BEZ_DPH}} × 0.21` |
| `{{CENA_S_DPH}}` | `{{CENA_BEZ_DPH}} × 1.21` |
| `{{SIDLO_MESTO}}` | Poslední část `{{SIDLO}}` (za PSČ) |

## Pravidla pro vyplňování zadavatelových šablon

### DOCX šablony (nejčastější)

1. Načti šablonu přes `docx` skill (unpack → edit XML → repack)
2. Hledej placeholdery typu:
   - `[DOPLNÍ DODAVATEL]` / `/DOPLNÍ DODAVATEL/`
   - `………………………` (tečkované řádky)
   - `[obchodní firma]`, `[adresa sídla]` atd.
   - Žlutě zvýrazněná pole
   - Prázdné buňky v tabulkách
3. Nahraď odpovídajícími hodnotami
4. **Pokud je aktivován Sledování změn (Track Changes):**
   - Zachovej revizní mód
   - Změny budou viditelné jako revize
5. Ponechej podpisová pole prázdná
6. Ulož jako DOCX (ne PDF!)

### XLSX šablony (cenové)

1. Načti přes `xlsx` skill
2. Identifikuj buňky určené k vyplnění (typicky: bílé pozadí, odemčené, s placeholder textem)
3. **NIKDY neupravuj vzorce** — pouze vstupní buňky
4. Po vyplnění ověř, že vzorce dávají korektní výsledky
5. Prezentuj souhrn uživateli k potvrzení

### PDF šablony (read-only)

1. PDF nelze přímo editovat → informuj uživatele
2. Nabídni alternativy:
   - Pokud existuje DOCX verze → použij tu
   - Pokud ne → vytvoř nový dokument se stejným obsahem

## Řazení dokumentů v nabídce

Standardní řazení (pokud tender nestanoví jiné):

```
1. Krycí list nabídky
2. Vyplněný návrh smlouvy (pokud požadováno)
3. Čestné prohlášení
4. Seznam referencí
5. Seznam realizačního týmu
6. Cenová nabídka / pricing template
7. Kreativní nabídka / prezentace (pokud požadováno)
8. Doklady (výpis z OR, pojištění atd.)
9. Compliance dokumenty (etický kodex, sankce, NDA)
10. Přílohy
```

## Kontrolní body před odevzdáním

Claude projde tento checklist a reportuje stav:

```
PRE-SUBMISSION CHECK:
━━━━━━━━━━━━━━━━━━━━
[?] Jsou všechny požadované dokumenty přítomny?
    → porovnat SUBMISSION CHECKLIST z Phase 2.4 vs. připravené soubory

[?] Jsou všechny placeholder vyplněné?
    → vyhledat zbývající {{...}} nebo [DOPLNIT] v dokumentech

[?] Jsou podpisová pole připravená?
    → upozornit kdo musí co podepsat

[?] Sedí ceny?
    → krycí list = pricing template = návrh smlouvy

[?] Sedí jazyk?
    → CZ dokumenty v CZ, EN v EN

[?] Sedí formáty?
    → požadovaný formát (DOCX/PDF/XLSX) odpovídá

[?] Sedí velikost?
    → některé platformy mají limit (ČT: max 100MB/soubor, 600MB celkem)

[?] Je registrace na platformě hotová?
    → Tender arena / VW Group Supply / jiné
```
