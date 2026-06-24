# Šablona: Seznam významných zakázek (Reference List)

> Použití: Technická kvalifikace — téměř každý tender.
> Formát se liší — tabulka vs. prostý seznam vs. formulář.

## Varianta A: Tabulka (nejčastější)

```
SEZNAM VÝZNAMNÝCH SLUŽEB

Dodavatel: {{FIRMA}}, IČO: {{ICO}}

K veřejné zakázce: „{{ZAKAZKA}}"

┌────┬──────────────────┬──────────┬─────────────┬────────────┬──────────────────────────┐
│ #  │ Název zakázky     │ Rok      │ Objednatel  │ Hodnota    │ Stručný popis            │
│    │                   │          │ + kontakt   │ (Kč b. DPH)│                          │
├────┼──────────────────┼──────────┼─────────────┼────────────┼──────────────────────────┤
│ 1  │ {{REF_1_NAZEV}}  │ {{ROK}}  │ {{KLIENT}}  │ {{HODNOTA}}│ {{POPIS}}                │
│    │                   │          │ {{KONTAKT}} │            │                          │
├────┼──────────────────┼──────────┼─────────────┼────────────┼──────────────────────────┤
│ 2  │ {{REF_2_NAZEV}}  │ {{ROK}}  │ {{KLIENT}}  │ {{HODNOTA}}│ {{POPIS}}                │
│    │                   │          │ {{KONTAKT}} │            │                          │
└────┴──────────────────┴──────────┴─────────────┴────────────┴──────────────────────────┘
```

## Varianta B: Podrobný seznam (PDS styl — s osvědčeními)

```
REFERENČNÍ ZAKÁZKA č. {{N}}

Název zakázky:          {{REF_N_NAZEV}}
Objednatel:             {{REF_N_KLIENT}}
Kontaktní osoba:        {{REF_N_KONTAKT}} ({{REF_N_KONTAKT_EMAIL}}, {{REF_N_KONTAKT_TEL}})
Rok realizace:          {{REF_N_ROK}}
Hodnota plnění:         {{REF_N_HODNOTA}} Kč bez DPH
Počet účastníků:        {{REF_N_POCET_UCASTNIKU}}

Stručný popis zakázky:
{{REF_N_POPIS}}

Subdodavatelé:          {{REF_N_SUBDODAVATELE}}

Osvědčení objednatele:  [PŘÍLOHA — přiložit jako samostatný dokument]
```

## Logika pro Claude

### Výběr referencí

1. Načti požadavky tenderu:
   - Minimální počet referencí
   - Minimální hodnota za referenci
   - Požadovaný sektor / typ akce
   - Minimální počet účastníků
   - Časové omezení (typicky posledních 3-5 let)
   - Specifické požadavky (veřejný sektor, osvědčení nutné)

2. Filtruj `reference-database.md`:
   ```
   MATCH = reference WHERE
     VALUE >= požadované minimum AND
     YEAR >= aktuální_rok - požadovaný_horizont AND
     TYPE matches požadovaný typ AND
     (PUBLIC_SECTOR = ANO if požadováno) AND
     (CONFIRMATION = ANO if požadováno)
   ```

3. Seřaď podle relevance:
   - Přesný match sektoru → +3 body
   - Osvědčení k dispozici → +2 body
   - Hodnota nad minimem → +1 bod
   - Novější než 2 roky → +1 bod

4. Navrhni TOP N referencí uživateli (kde N = požadovaný počet)

5. Po potvrzení formátuj do požadované varianty (A nebo B)

### Popis reference (jak psát POPIS)

- Max 3 věty
- Začni TYPEM služby: "Kompletní produkční zajištění..." / "Kreativní koncept a realizace..."
- Uveď KLÍČOVÉ parametry relevantní pro tender (počet osob, typ techniky, délka)
- Zakonči VÝSLEDKEM, pokud je k dispozici
- Nepsat genericky — být specifický pro danou zakázku

**Dobrý příklad:**
"Kompletní technické a produkční zajištění dvoudenní manažerské konference pro 250 účastníků včetně stage designu, AV techniky, LED stěny 12×4m, livestreamu pro 500 online účastníků a koordinace cateringu."

**Špatný příklad:**
"Organizace akce pro klienta z energetického sektoru."
