# MEATING 2026 — stav práce (bezpečnost, GDPR, smlouva)

**Poslední aktualizace:** 2. 9. 2026
**Větev:** `claude/security-presentation-client-whsm8m`
**Klient:** Český svaz zpracovatelů masa · kontakt Julius Maindl (MULTIVAC CZ)
**Akce:** MEATING 2026, 20. 10. 2026, OREA Congress Hotel Brno

Tenhle soubor je vstupní bod. Kdo (nebo co) sem přijde po odmlce, ať začne tady.

---

## Odkud to vzniklo

Julius volal 1. 9. večer, že se svaz bojí technologií: že se přes QR kódy „načtou
hackeři“, a GDPR u selfie aplikace. Prezentace vznikla přes noc na ráno 2. 9. v 8:00.
**Odprezentováno bylo.** Navazuje na to zpracovatelská smlouva.

---

## Co je hotové

### 1. Prezentace — `prezentace/meating-2026-bezpecnost/`

13 slajdů na šířku, XLAB white theme, čeština pro netechnické publikum.

| Soubor | Co to je |
|--------|----------|
| `XLAB_MEATING_2026_Bezpecnost.pdf` | Výstup k prezentování (273 kB) |
| `prezentace.html` | Zdroj se zástupnými značkami pro assety |
| `img/` | Tři ukázkové motivy selfie zdi |
| `README.md` | Jak přegenerovat PDF |
| `POZNAMKY_INTERNI.md` | **Neposílat klientovi.** Osm bodů: co v prezentaci vědomě není a proč |

**Struktura:** 1 titul · 2 reference a klienti · 3 naše certifikáty · 4 na čem to běží ·
5 co platí pro všechny aplikace · 6 selfie zeď · 7 není to deepfake · 8 Mark Meatman ·
9 aplikace, kvízy a hlasování · 10 QR kódy · 11 označení AI a záložní plán ·
12 co si z toho odnést · 13 kde si to ověřit + kontakt.

**Veřejný odkaz na PDF** (repozitář je public, funguje bez přihlášení):
`https://github.com/jtrjtrjtr/XLAB_OFFICE_AUTOMATION/blob/claude/security-presentation-client-whsm8m/prezentace/meating-2026-bezpecnost/XLAB_MEATING_2026_Bezpecnost.pdf`

**Webová verze** (soukromá, sdílení se zapíná v menu stránky; Ctrl+P dá PDF):
`https://claude.ai/code/artifact/79a1e195-a43f-4c30-872c-546dae6c227f`

### 2. Smlouva — `smlouvy/meating-2026-gdpr/`

Zpracovatelská smlouva podle čl. 28 GDPR, 12 článků a tři přílohy.
XLAB vystupuje jako **zpracovatel**, ne společný správce.
Detaily a seznam polí k doplnění jsou v `smlouvy/meating-2026-gdpr/README.md`.

---

## Otevřené body

### 🔴 Blokující, než se něco podepíše nebo odprezentuje dál

1. **Retence fotek — tři dny.** Prezentace i smlouva (čl. 8.1, Příloha 1 A) slibují,
   že se vstupní fotka maže hned a výstup do tří dnů. Podle zápisu z 11. 8. je
   v `F:/Vibe-apps/multivac-meating-selfie/` **mazání podle stáří vypnuté**.
   Dokud se nezapne, je ten závazek nesplnitelný.
   Pozor: `MAX_AGE_DAYS = 0` neznamená „nemazat“, ale „smazat všechno“.
2. **Kdo je správce údajů** — svaz, nebo MULTIVAC jako objednatel? Táhne se celou
   smlouvou, obě varianty jsou v dokumentu jako `[DOPLNIT]`.
3. **Reference u avatarů na slajdu 2.** Doložené: Škoda, HOCHTIEF, ČSLH, MULTIVAC.
   Nedoložené a zapsané podle zadání: EY, Deloitte, Wella, Decathlon, zdravotnictví.

### 🟡 Doplnit

4. **Chybí `Ukazky_motivu_SelfieWall.png`** ze složky `PRO_KLIENTA_2026-08-17` na F:
   — srovnávací tabulka 12 snímků (muž / žena / dvojice × 4 motivy).
   Klient chce vidět i **vstupní fotografii** vedle výstupů, aby bylo poznat, že podoba
   není zachovaná a nejde o deepfake. Ani jedno není na Drive ani v Gmailu.
5. **Motiv Řezník Krkovička** ze slajdu 7 vyřazen — všechny rendery na Drive jsou
   loutková varianta a motiv je podle deníku z 18. 8. neuzavřený spor s klientem.
   Až bude schválená verze, vrátí se jako čtvrtá dlaždice.
6. **Příloha 2 smlouvy** — doplnit poskytovatele hostingu a případně syntézy hlasu
   a u obou ověřit právní titul pro předání do USA.
7. **Zápis ze schůzky 2. 9.** — Sebastian ho chtěl poslat, nedorazil.
   Až přijde, projít, jestli svaz něco slíbil nebo si vymínil navíc.
8. **Přesné URL sekcí webu** (Privacy, Terms, Code of Conduct) na slajdu 13 —
   uvedené jen názvem podle menu, z prostředí Claude Code nešly ověřit.

### ⚠️ Nesouvisí s MEATINGem, ale našlo se cestou

9. **Peklo Čertovina** má v živé aplikaci pořád text souhlasu, který tvrdí, že se údaje
   nepředávají mimo EU — přitom fotka jde ke zpracování ke Googlu. Opravit.
10. **Repozitář `XLAB_OFFICE_AUTOMATION` je veřejný** a `POZNAMKY_INTERNI.md` je v něm
    čitelný komukoli. Smazání commitem to nevyřeší, zůstane v historii.
    Řešení: repo na private, nebo přepsat historii. Rozhodnutí na Jindřichovi.

---

## Jak navázat v nové session

1. Přečíst tenhle soubor a `prezentace/meating-2026-bezpecnost/POZNAMKY_INTERNI.md`.
2. Zkontrolovat větev: `git checkout claude/security-presentation-client-whsm8m && git pull`
3. Kontext k projektu je v Notionu:
   - `Avatar Mark Meatman — MULTIVAC / TVI` (PM Hub / Projekty) — hlavní stránka projektu
   - `MEATING 2026 — rozhodnutí z telefonátu se svazem (28. 8. 2026)` — QR kódy, hlasování, kvízy
   - `MEATING Selfie Wall — demo postaveno a nasazeno` — retence fotek, text souhlasu
   - `MEATING 2026 — balíček pro klienta kompletní` (18. 8.) — spor o Krkovičku
   - `XLAB vzor smlouvy — souhlas s užitím hlasu a podoby` — konstrukce zpracovatel vs. správce
4. Prostředí: `soffice` v kontejneru Claude Code nefunguje (nejde konvertovat DOCX na PDF),
   PDF prezentace se generuje přes Chromium headless — postup je v README u prezentace.
   Na `xlab.cz` ani na Netlify se z kontejneru nedostaneš, egress je blokovaný.
