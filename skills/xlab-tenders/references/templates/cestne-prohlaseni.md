# Šablona: Čestné prohlášení o splnění kvalifikace

> Použití: Když tender vyžaduje čestné prohlášení a NEPOSKYTL vlastní šablonu.
> Pokud zadavatel poskytl vlastní vzor → VŽDY použij jeho vzor, ne tuto šablonu.

## Varianty

### Varianta A: Základní + Profesní způsobilost (nejčastější)

Použij když tender požaduje prokázání základní a profesní způsobilosti čestným prohlášením bez dalších detailů.

### Varianta B: Základní + Profesní + Reference + Tým (kompletní)

Použij když tender požaduje vše v jednom dokumentu (typické pro VZMR).

---

## Text šablony — Varianta A

```
PÍSEMNÉ ČESTNÉ PROHLÁŠENÍ DODAVATELE

o prokázání kvalifikace pro veřejnou zakázku s názvem

„{{ZAKAZKA}}"


Dodavatel — {{FIRMA}}, se sídlem {{SIDLO}}, IČO: {{ICO}}, {{OR_ZAPIS}},
zastoupený {{JEDNATEL_1}},

jako dodavatel předmětné veřejné zakázky

tímto čestně prohlašuje, že splňuje základní způsobilost, neboť:

a) nebyl v zemi svého sídla v posledních 5 letech před zahájením zadávacího
   řízení pravomocně odsouzen pro trestný čin uvedený v příloze č. 3
   k zákonu č. 134/2016 Sb. nebo obdobný trestný čin podle právního řádu
   země sídla dodavatele; k zahlazení odsouzení se nepřihlíží,

b) nemá v České republice nebo v zemi svého sídla v evidenci daní zachycen
   splatný daňový nedoplatek, a to i ve vztahu ke spotřební dani,

c) nemá v České republice nebo v zemi svého sídla splatný nedoplatek
   na pojistném nebo na penále na veřejné zdravotní pojištění,

d) nemá v České republice nebo v zemi svého sídla splatný nedoplatek
   na pojistném nebo na penále na sociální zabezpečení a příspěvku
   na státní politiku zaměstnanosti,

e) není v likvidaci, nebylo proti němu vydáno rozhodnutí o úpadku, nebyla
   vůči němu nařízena nucená správa podle jiného právního předpisu nebo
   není v obdobné situaci podle právního řádu země sídla dodavatele.

{{IF_PRAVNICKA_OSOBA}}
Dodavatel dále čestně prohlašuje, že podmínku podle písm. a) splňuje
tato právnická osoba a zároveň každý člen statutárního orgánu.
{{/IF_PRAVNICKA_OSOBA}}


Dodavatel dále čestně prohlašuje, že splňuje profesní způsobilost, neboť:

- je zapsán v obchodním rejstříku nebo jiné obdobné evidenci,
- je oprávněn podnikat v rozsahu odpovídajícímu předmětu veřejné zakázky
  na území České republiky.


V {{SIDLO_MESTO}} dne {{DATUM}}


................................................................
{{JEDNATEL_1}}
{{JEDNATEL_1_FUNKCE}}
{{FIRMA}}
```

---

## Text šablony — Varianta B (rozšířená o reference a tým)

Jako Varianta A, plus následující sekce za profesní způsobilostí:

```
Dodavatel dále prokazuje splnění technické kvalifikace:

SEZNAM VÝZNAMNÝCH ZAKÁZEK

{{FOR_EACH_REFERENCE}}
{{REF_N}}.
Název zakázky:     {{REF_N_NAZEV}}
Objednatel:        {{REF_N_KLIENT}}
Kontaktní osoba:   {{REF_N_KONTAKT}}
Rok realizace:     {{REF_N_ROK}}
Hodnota plnění:    {{REF_N_HODNOTA}} Kč bez DPH
Stručný popis:     {{REF_N_POPIS}}
{{/FOR_EACH_REFERENCE}}


SEZNAM REALIZAČNÍHO TÝMU

{{FOR_EACH_TEAM_MEMBER}}
Jméno:             {{TEAM_N_JMENO}}
Role:              {{TEAM_N_ROLE}}
Délka praxe:       {{TEAM_N_PRAXE}} let
Klíčové zkušenosti: {{TEAM_N_ZKUSENOSTI}}
{{/FOR_EACH_TEAM_MEMBER}}
```

---

## Logika pro Claude

### Při generování:

1. Načti `company-data.md` → doplň firemní placeholdery
2. Načti tender header card → doplň `{{ZAKAZKA}}` a `{{ZADAVATEL}}`
3. Pokud varianta B:
   a. Načti `reference-database.md` → filtruj podle požadavků tenderu
   b. Navrhni výběr referencí uživateli → po potvrzení doplň
   c. Zeptej se na tým → doplň
4. Nastav `{{DATUM}}` na aktuální datum
5. Ponechej podpisové pole prázdné
6. Vygeneruj DOCX přes `docx` skill

### Odchylky od standardu (co sledovat):

| Tender specificky požaduje... | Akce |
|------------------------------|------|
| Trestné činy s rozšířeným výčtem | Přidej specifické body (viz ČEZ vzor s body a-g) |
| Prohlášení o subdodavatelích | Přidej sekci o subdodavatelích |
| Prohlášení o střetu zájmů | Přidej sekci (typické pro Roche, pharma) |
| Ekonomickou kvalifikaci (obrat) | Přidej sekci s obratovými údaji |
| Konkrétní číslo §§ odkazů | Uprav podle požadovaných paragrafů |

### Typické chyby (prevence):

- ❌ Chybějící bod o právnické osobě a statutárním orgánu → VŽDY přidat pro s.r.o./a.s.
- ❌ Datum starší než 3 měsíce → některé tendery to vyžadují
- ❌ Podpis neodpovídá statutárnímu orgánu → ověřit kdo podepisuje
- ❌ Chybějící IČO nebo sídlo → VŽDY kontrolovat kompletnost
