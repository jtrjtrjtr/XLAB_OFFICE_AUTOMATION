# Case Study: Moment Factory × Phish at Sphere, Las Vegas

**Zpracováno:** 2026-03-10 | **Track:** T1 + T4 | **Typ:** Live Concert / Real-time Generative

---

## Základní fakta

- **Klient / umělec:** Phish (jam rock)
- **Produkce:** Moment Factory (Montreal, 450 zaměstnanců, 5 kanceláří)
- **Místo:** Sphere, Las Vegas (270° LED, 250 ft výška, 160 000 sq ft obrazovka)
- **Rozsah:** 4 noce, duben 2024. Každý večer unikátní show.
- **Kreativní vedení:** Abigail Rosen Holmes (co-creative & show director), Chris Kuroda (lighting designer), Trey Anastasio (Phish frontman, kreativní input)

---

## Tech Stack

| Vrstva | Nástroj / Vendor | Role |
|--------|-----------------|------|
| Real-time engine | **Notch** | Generativní vizuály reagující na hudbu v reálném čase |
| Real-time engine | **Unreal Engine** | Scenografické elementy, 360° live capture, AI-generované vizuály |
| Media server | **Disguise** (GX 3 předpoklad) | Playback, blending, mapping na Sphere povrch |
| Real-time toolkit | **Myreze** (Norsko) | Custom operátorská konzole pro live improvizaci |
| Pre-visualization | Unreal Engine | Digital twin Sphere pro testování scale a timing |
| Obsah | Mix pre-render + real-time | Původní plán 70/30 → finálně **50/50 split** |

---

## Kreativní koncept

Čtyři večery, čtyři skupenství hmoty: pevné, kapalné, plynné, plazma. Každý večer unikátní vizuální identita odvozená z fyzikálního principu skupenství.

Phish jsou známí improvizací — setlisty se mění každý večer, jam sessions jsou nepředvídatelné. Vizuály musely být stejně improvizační jako hudba.

---

## Klíčové produkční rozhodnutí

### 1. Přechod z pre-renderu na real-time
Původně Moment Factory plánoval 70% pre-renderovaného obsahu a 30% real-time. Během rehearsals zjistili, že pre-render je příliš rigidní pro Phish improvizační styl. Finální split: **50/50**, což je historicky bezprecedentní pro venue této velikosti.

### 2. Operátorská konzole pro neoperátora
Myreze (norský tým "virtual engineers") vyvinuli custom toolkit, který umožňuje vizuálnímu operátorovi improvizovat spolu s kapelou — přepínat scény, blendovat vizuály, reagovat na dynamiku hudby. Klíčová výzva: systém museli navrhnout tak, aby ho mohl ovládat někdo, kdo nezná vnitřní technické fungování — protože finální operátor nebyl z Myreze týmu.

### 3. Pre-visualization jako záchranná síť
Moment Factory roky používá Unreal Engine pro VR pre-visualization: digitální dvojče venue, ve kterém testují scale, timing a potenciální problémy. Na Sphere projektu to bylo klíčové — jakákoliv úprava pre-renderovaného obsahu na 160 000 sq ft obrazovce by byla extrémně nákladná. UE umožnilo tweakovat v kontextu.

### 4. AI jako kreativní nástroj
AI-generované vizuály byly součástí obsahu — Moment Factory popisuje AI jako "transformativní nástroj, který podporuje inovaci, kolaboraci a posouvaní kreativních hranic." Konkrétní implementace nebyla detailně publikována, ale AI bylo integrováno do content pipeline.

---

## Co fungovalo

- **Real-time pipeline odstranil rigiditu.** Kapela mohla improvizovat bez omezení, vizuály sledovaly.
- **Každý večer byl unikátní** — ne jen jiný setlist, ale jiný vizuální svět. Fanoušci měli důvod přijít všechny 4 noce.
- **Myreze toolkit demokratizoval operátorství** — konzole byla dostatečně jednoduchá pro vizuálního operátora bez programátorského backgroundu.
- **VR pre-viz předešla nákladným chybám** na extrémně velkém plátně.

---

## Trade-offs a výzvy

- **Časový tlak:** 4 unikátní show ve 4 dnech = extrémní nároky na přípravu a produkční flexibilitu.
- **Scale jako problém i příležitost:** 160 000 sq ft obrazovka vyžaduje obsah, který funguje v obřím rozlišení. Malé detaily zmizí, velké gesta dominují.
- **Kolaborace přes více studií:** Moment Factory, Myreze, Abigail Rosen Holmes, Chris Kuroda + kapela. Koordinace kreativních vizí vyžadovala jasné role a důvěru.
- **Hranice pre-renderu:** Původní poměr 70/30 se ukázal jako nefunkční. Lesson learned: pro improvizační formát plánujte víc real-time od začátku.

---

## Přenositelné vzorce pro XLAB

### PŘ1: Real-time generativní obsah jako standard pro live eventy
XLAB používá Notch + Disguise — identický stack. Posun od "pouštíme video" k "generujeme vizuály live" je reálný a přináší vyšší hodnotu pro klienta. Na korporátních eventech to znamená: vizuály reagující na obsah prezentace, data z publika, nebo interakci speakera.

### PŘ2: Operátorská konzole pro ne-technického uživatele
Pokud XLAB vytvoří real-time vizuální systém pro event, musí být ovladatelný produkčním týmem na místě, ne jen vývojářem. Myreze přístup (jednoduché rozhraní nad komplexním systémem) je vzor.

### PŘ3: Pre-visualization jako prodejní nástroj
XLAB může nabízet VR/3D pre-viz jako součást proposal fáze — klient vidí event v digitálním dvojčeti před realizací. Moment Factory to dělá rutinně, pro XLAB je to upsell příležitost.

### PŘ4: Tematický rámec dává strukturu improvizaci
"Čtyři skupenství hmoty" = jednoduchý koncept, který dal prostor kreativní volnosti. Pro XLAB korporátní eventy: silný tematický rámec umožňuje variace a adaptaci bez ztráty koherence.

---

## Zdroje

- Notch case study: https://www.notch.one/madewithnotch/phish-sphere-vegas
- Unreal Engine spotlight: unrealengine.com (spotlight Moment Factory Phish)
- postPerspective interview s Danielem Jeanem: https://postperspective.com/moment-factory-goes-phishing-with-vfx-at-las-vegas-sphere/
- blooloop: https://blooloop.com/immersive/news/moment-factory-phish-sphere/
- Moment Factory web: https://momentfactory.com/products/phish-at-sphere-in-las-vegas
