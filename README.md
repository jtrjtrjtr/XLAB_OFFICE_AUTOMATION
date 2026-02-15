# OFFICE automation

Interní repozitář pro správu Claude AI skills, system promptů a šablon používaných v XLAB.

## Struktura

```
skills/          Skills nahrávané do Claude projektů (1 adresář = 1 skill)
prompts/         System prompty a kontextové dokumenty pro Claude projekty
  system/        Hlavní system prompty
  templates/     Šablony dokumentů (nabídky, briefy, reporty)
docs/            Interní poznámky, konvence, postupy
```

## Jak pracovat se skills

Každý skill má vlastní adresář s `SKILL.md` a případně `assets/` podadresářem.

**Nahrání skillu do Claude projektu:**
1. Zazipovat adresář skillu (např. `xlab-brand/`)
2. V Claude projektu otevřít nastavení
3. Nahrát ZIP jako nový skill

**Aktualizace skillu:**
1. Upravit soubory v tomto repozitáři
2. Commit + Push
3. Zazipovat a nahrát do Claude projektu jako náhradu

## Přehled skills

| Skill | Popis |
|-------|-------|
| `xlab-brand` | XLAB brand identita — barvy, typografie, loga, layouty |

## Konvence

- Jazyk souborů: čeština, pokud není důvod psát anglicky
- SKILL.md vždy v angličtině (Claude s ním pracuje interně)
- Assety pojmenovávat bez diakritiky a mezer, snake_case
- Commit zprávy stručně, česky nebo anglicky
