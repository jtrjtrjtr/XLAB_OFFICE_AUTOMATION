# references/ — Zdroje dat a šablony

## Přehled souborů

### Zdrojová data (udržuje uživatel)

| Soubor | Formát | Obsah | Jak aktualizovat |
|--------|--------|-------|-----------------|
| `company-data.md` | MD | Identifikace XLAB, statutární orgán, kontakty, obraty, pojištění | Editovat přímo v textu |
| `xlab-reference-events.xlsx` | Excel | Seznam referenčních zakázek (klient, hodnota, popis, kontakt) | Přidat řádek do sheetu "Zakazky" |
| `xlab-project-team.xlsx` | Excel | Klíčový tým (pozice, osoba, praxe) | Přidat/upravit řádek v sheetu "Sheet1" |

### Šablony dokumentů (udržuje Claude / skill autor)

| Soubor | Kdy se používá |
|--------|---------------|
| `templates/cestne-prohlaseni.md` | Tender vyžaduje čestné prohlášení a neposkytl vlastní šablonu |
| `templates/kryci-list.md` | Tender vyžaduje krycí list a neposkytl vlastní šablonu |
| `templates/seznam-referenci.md` | Formátování referencí z Excelu do požadované struktury |
| `templates/seznam-tymu.md` | Formátování týmu z Excelu do požadované struktury |
| `templates/sankce-prohlaseni.md` | Prohlášení k mezinárodním sankcím (EU, Rusko/Bělorusko) |

### Pravidla

| Soubor | Obsah |
|--------|-------|
| `patterns/fill-logic.md` | Rozhodovací strom pro vyplňování šablon, placeholder mapping |

---

## Jak Claude pracuje s daty

### Reference (xlab-reference-events.xlsx)

Claude čte Excel přes openpyxl. Struktura sheetu "Zakazky":

| Sloupec | Obsah |
|---------|-------|
| A | Pořadové číslo |
| B | Předmět plnění (popis zakázky) |
| C | Místo poskytování služeb |
| D | Poskytovatel (vždy XLAB s.r.o.) |
| E | Období poskytování |
| F | Objednatel — firma, osoba, telefon |
| G | Finanční objem |
| H | Poznámka |
| I | Bod 6.2.1. (ČEZ specifické — ignorovat u jiných tendrů) |
| J | Bod 6.2.2. (ČEZ specifické — ignorovat u jiných tendrů) |

**Matching logika:**

1. Načti požadavky tenderu (minimální hodnota, počet osob, sektor, období)
2. Filtruj řádky Excelu podle parametrů
3. Seřaď podle relevance (nejlepší match nahoře)
4. Navrhni uživateli: "Pro tento tender doporučuji reference #1, #6, #9 — souhlasíš?"
5. Po potvrzení formátuj do požadované struktury (tabulka / formulář / volný text)

### Tým (xlab-project-team.xlsx)

Sheet "Sheet1": Pozice | Osoba | Praxe

Claude mapuje pozice z Excelu na požadované role v tenderu.

### Firemní údaje (company-data.md)

Strukturovaný MD soubor s placeholder formátem `[DOPLNIT]` pro chybějící údaje.
Claude při vyplňování šablon:
1. Načte company-data.md
2. Doplní známé hodnoty
3. U `[DOPLNIT]` upozorní uživatele

---

## Pravidlo #1: Zadavatelova šablona má VŽDY přednost

Pokud tender poskytl vlastní formulář (DOCX/XLSX) → Claude vyplní TEN, ne vlastní šablonu.
Vlastní šablony v `templates/` jsou jen fallback pro případy, kdy zadavatel šablonu neposkytl.

## Pravidlo #2: Update = výměna souboru

Když se mění reference nebo tým:
1. Uživatel upraví Excel
2. Nahraje novou verzi do projektu (nahradí starý soubor)
3. Claude automaticky pracuje s novou verzí

Žádné ruční editování MD souborů pro tabulková data.
