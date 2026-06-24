# Šablona: Seznam realizačního týmu

> Použití: Technická kvalifikace — velmi časté u VZMR a korporátních tendrů.

## Struktura

```
SEZNAM REALIZAČNÍHO TÝMU

Dodavatel: {{FIRMA}}, IČO: {{ICO}}
K veřejné zakázce: „{{ZAKAZKA}}"


1. {{TEAM_1_ROLE}} ({{TEAM_1_VZTAH}})

   Jméno:               {{TEAM_1_JMENO}}
   Délka praxe:          {{TEAM_1_PRAXE}} let v oboru
   Relevantní zkušenosti:
   - {{TEAM_1_REF_1}}
   - {{TEAM_1_REF_2}}


2. {{TEAM_2_ROLE}} ({{TEAM_2_VZTAH}})

   Jméno:               {{TEAM_2_JMENO}}
   Délka praxe:          {{TEAM_2_PRAXE}} let v oboru
   Relevantní zkušenosti:
   - {{TEAM_2_REF_1}}
   - {{TEAM_2_REF_2}}
```

## Typické požadované role (napříč tendery)

| Role CZ | Role EN | Kdo u XLAB |
|---------|---------|------------|
| Vedoucí organizátor / Project lead | Project Lead | [DOPLNIT] |
| Projektový manažer | Project Manager | [DOPLNIT] |
| Kreativní ředitel | Creative Director | [DOPLNIT] |
| Technický ředitel | Technical Director | [DOPLNIT] |
| Architekt / Scénograf | Architect / Set Designer | [DOPLNIT] |
| Asistent produkce | Production Assistant | [DOPLNIT] |

## Logika

- `{{TEAM_N_VZTAH}}` = "zaměstnanec dodavatele" nebo "externí spolupracovník"
- Zkušenosti uvádět KONKRÉTNĚ: "Produkce konference XY pro 300 účastníků (2024)"
- Pokud tender požaduje minimální praxe (např. 5 let) → ověřit a explicitně uvést
- Pokud tender požaduje reference na konkrétní osobu → reference musí být oddělené od firemních
