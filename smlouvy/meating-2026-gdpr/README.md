# Smlouva o zpracování osobních údajů — MEATING 2026

Zpracovatelská smlouva podle čl. 28 odst. 3 GDPR mezi pořadatelem konference (Správce)
a XLAB s.r.o. (Zpracovatel). Vychází z rešerše a obsahu prezentace
`prezentace/meating-2026-bezpecnost/` — tvrzení ve smlouvě odpovídají tomu,
co bylo svazu odprezentováno.

**Návrh k právní kontrole.** XLAB má zavedený postup externí právní revize
(viz vzor souhlasu s užitím hlasu a podoby, SharePoint `1.2 X CASES / _VZORY_SMLUV`).
Tenhle dokument by měl projít stejnou cestou, než půjde k podpisu.

## Soubory

| Soubor | Popis |
|--------|-------|
| `XLAB_MEATING_2026_Smlouva_o_zpracovani_osobnich_udaju.docx` | Smlouva včetně tří příloh. |
| `build.js` | Generátor dokumentu (docx-js). |

Přegenerování: `npm install docx && node build.js`

## Struktura

12 článků + 3 přílohy:

1. Úvodní ustanovení a role stran — XLAB je **zpracovatel**, ne společný správce
2. Předmět, povaha, účel a doba zpracování — včetně vyloučení zvláštních kategorií
3. Pokyny Správce
4. Povinnosti Zpracovatele — mlčenlivost, čl. 32, součinnost, audit
5. Porušení zabezpečení — ohlášení do 24 hodin
6. Další zpracovatelé
7. Předávání do třetích zemí — DPF / standardní smluvní doložky
8. Výmaz a vrácení údajů
9. Umělá inteligence a transparentnost — čl. 50 AI Actu
10. Odpovědnost
11. Doba trvání
12. Závěrečná ustanovení

- Příloha 1 — popis zpracování zvlášť pro selfie zeď, eventovou aplikaci a avatara
- Příloha 2 — seznam dalších zpracovatelů a právní titul pro předání
- Příloha 3 — technická a organizační opatření

## Co doplnit před podpisem

Pole `[DOPLNIT]` v dokumentu. Kromě identifikačních údajů jde hlavně o:

1. **Kdo je Správce** — Český svaz zpracovatelů masa, nebo MULTIVAC jako objednatel?
   Určuje to, kdo stanovil účel zpracování. Ovlivňuje celý dokument.
2. **Číslo a datum Hlavní smlouvy** (čl. 1.1) — objednávka XZ26072.
3. **Seznam dalších zpracovatelů** (Příloha 2) — doplnit poskytovatele hostingu
   a případně syntézy hlasu, u obou ověřit právní titul pro předání do USA.
4. **Nejzazší datum zpracování** (čl. 2.4).

## Tvrzení, která musí sedět s realitou

Smlouva je závazek, ne prezentace. Tohle si ověřte proti kódu a provozu:

- **Výmaz vstupní fotografie bezprostředně po vygenerování a výmaz výstupu do 3 dnů**
  (čl. 8.1, Příloha 1 A). Viz `prezentace/meating-2026-bezpecnost/POZNAMKY_INTERNI.md`
  bod 2 — podle zápisu z 11. 8. bylo mazání podle stáří v MEATING verzi vypnuté.
  **Bez zapnutého automatického mazání je tenhle článek nesplnitelný.**
- **Ohlášení porušení zabezpečení do 24 hodin** (čl. 5.1). Je to přísnější než zákon
  vyžaduje po zpracovateli, ale dává Správci prostor stihnout svých 72 hodin.
  Ověřte, že to provozně utáhneme.
- **Přítomnost technika po celou dobu akce** (Příloha 3). Musí sedět s rozpočtem.
- **Certifikát ISO/IEC 27001** (čl. 1.4). U 27701 a 9001 je ve smlouvě záměrně
  jen „v souladu s normou", ne „certifikováno" — web XLABu formuluje obojí odlišně.
