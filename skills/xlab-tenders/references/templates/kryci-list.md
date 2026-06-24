# Šablona: Krycí list nabídky

> Použití: Když tender vyžaduje krycí list a NEPOSKYTL vlastní šablonu.

## Struktura

```
                    KRYCÍ LIST NABÍDKY

Veřejná zakázka:    {{ZAKAZKA}}

━━━ ZADAVATEL ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Název:              {{ZADAVATEL_NAZEV}}
Sídlo:              {{ZADAVATEL_SIDLO}}
IČO:                {{ZADAVATEL_ICO}}

━━━ DODAVATEL ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Název:              {{FIRMA}}
Sídlo:              {{SIDLO}}
IČO:                {{ICO}}
DIČ:                {{DIC}}
Datová schránka:    {{DATOVA_SCHRANKA}}
Kontaktní osoba:    {{KONTAKT_OBCHOD_JMENO}}
Telefon:            {{KONTAKT_OBCHOD_TELEFON}}
E-mail:             {{KONTAKT_OBCHOD_EMAIL}}
Osoba oprávněná jednat: {{JEDNATEL_1}}

━━━ NABÍDKOVÁ CENA ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cena bez DPH:       {{CENA_BEZ_DPH}} Kč
DPH (21 %):         {{DPH}} Kč
Cena vč. DPH:       {{CENA_S_DPH}} Kč

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

V {{SIDLO_MESTO}} dne {{DATUM}}


................................................................
Podpis oprávněné osoby         Razítko

{{JEDNATEL_1}}
{{JEDNATEL_1_FUNKCE}}
```

## Logika pro Claude

1. Všechny firemní údaje → `company-data.md`
2. Zadavatelské údaje → extrahovat z tender dokumentace
3. Cena → VŽDY vyžadovat od uživatele (nikdy neodhadovat)
4. DPH → vypočítat (standardně 21 %, ověřit u uživatele)
5. Podpis a razítko → ponechat prázdné

## Formát DOCX

- Tabulková struktura (3 sloupce: label | hodnota | prázdné/razítko)
- Orámované buňky
- Font: Calibri 11
- Hlavička tučně, zvětšeně
