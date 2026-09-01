# MEATING 2026 — Bezpečnost a ochrana osobních údajů

Prezentace pro Český svaz zpracovatelů masa (kontakt Julius Maindl, MULTIVAC CZ).
Odpovídá na obavy svazu ohledně QR kódů, GDPR u selfie aplikace a bezpečnosti
technologií nasazovaných na MEATING 2026 (20. 10. 2026, OREA Congress Hotel Brno).

- Formát: 22 slajdů, na šířku, 16:9 (960 × 540 pt)
- Brand: XLAB WHITE theme (podle skillu `xlab-brand`)
- Jazyk: čeština, srozumitelná i pro publikum, které s technologiemi nepracuje

## Soubory

| Soubor | Popis |
|--------|-------|
| `prezentace.html` | Zdroj. Obsahuje zástupné značky `__LOGO_BLACK__` a `__XMARK__` pro brandové assety. |
| `XLAB_MEATING_2026_Bezpecnost.pdf` | Výstup k prezentování. |
| `POZNAMKY_INTERNI.md` | **Neposílat klientovi.** Co v prezentaci vědomě není a proč. |

## Jak přegenerovat PDF

```bash
# 1) rozbalit brandové assety
python3 skills/xlab-brand/scripts/extract_assets.py /tmp/xlab-assets

# 2) doplnit assety do HTML (base64 data URI) → build.html
python3 - <<'EOF'
import base64, pathlib
A = pathlib.Path("/tmp/xlab-assets")
u = lambda p: "data:image/png;base64," + base64.b64encode((A/p).read_bytes()).decode()
h = pathlib.Path("prezentace.html").read_text(encoding="utf-8")
h = h.replace("__LOGO_BLACK__", u("x_logo_black.png")).replace("__XMARK__", u("x_symbol_black.png"))
pathlib.Path("build.html").write_text(h, encoding="utf-8")
EOF

# 3) vytisknout do PDF (Chromium headless)
chromium --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=XLAB_MEATING_2026_Bezpecnost.pdf file://$PWD/build.html
```

Rozměr stránky drží `@page { size: 338.667mm 190.5mm; }` v CSS.

## Zdroje obsahu

- Notion: `Avatar Mark Meatman — MULTIVAC / TVI` (PM Hub / Projekty)
- Notion: `MEATING 2026 — rozhodnutí z telefonátu se svazem (28. 8. 2026)` — tři druhy QR kódů, mechanika hlasování, kvízy
- Notion: `MEATING Selfie Wall — demo postaveno a nasazeno` — retence fotek, text souhlasu, obsahová pravidla
- Notion: `Avatar Laurin — vazby a návaznosti`, kap. 8 Kamera — kamera neukládá ani neodesílá snímky
- Notion: `MEATING 2026 — kiosek Marka v1 hotový a otestovaný` — offline/záložní režim, 17 guardrailů
- Certifikace poskytovatelů (slajdy 5–6) ověřeno u zdroje: ISO/IEC 27001 / 27017 / 27018 / 27701
  a SOC 2 Type II u Google i OpenAI; EU–USA Data Privacy Framework (rozhodnutí Evropské komise,
  červenec 2023); data z firemních a API služeb se standardně nepoužívají k trénování modelů.
