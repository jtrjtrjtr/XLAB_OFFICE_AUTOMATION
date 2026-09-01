# Interní poznámky k prezentaci — NEPOSÍLAT KLIENTOVI

Podle zadání nejsou slabiny v prezentaci. Tady je jejich seznam, aby se daly
v klidu dořešit po prezentaci.

## 1. Ověřit před tiskem — reference u avatarů

V Notionu jsou doložené: **ŠKODA AUTO** (Laurin, muzeum + Autostadt Wolfsburg),
**HOCHTIEF** (Stavomír), **ČSLH** (Puk / Síň slávy), **MULTIVAC / TVI**.

Nedoložené v Notionu, do prezentace zapsané podle zadání:
**Ernst & Young, Deloitte, Wella, Decathlon, zdravotnictví (pilot)**.
Před prezentací projít a případně vyškrtnout, co nemá oporu — jde o slajd 15.
U selfie zdi jsou naopak všechny uvedené reference doložené
(Visa, Wflow, ČSLH, 4FIN Kongres 2026, Peklo Čertovina, MULTIVAC/TVI).

## 2. Retence fotek — ve slajdech úmyslně NENÍ „30 dní“

Zadání znělo „mažou se po 30 dnech“. V MEATING verzi selfie aplikace
(`F:/Vibe-apps/multivac-meating-selfie/`) je ale **mazání podle stáří vypnuté**
a zůstal jen strop na počet souborů (2000). Text souhlasu je proto psaný jako
„uchování po dobu akce“, žádný slib 30 dnů. Slajd 10 říká „uchování jen po dobu akce,
po skončení konference se mažou“ — což je pravda a zároveň víc, než slibuje souhlas.

**Úkol:** před akcí buď zapnout automatické mazání s konkrétní lhůtou a slíbit ji
v souhlasu, nebo po akci složku ručně vyprázdnit a mít o tom záznam.
Pozor na past zapsanou v Notionu: `MAX_AGE_DAYS = 0` neznamená „nemazat“, ale
„smazat všechno“ — je na to pojistka `if (MAX_AGE_DAYS > 0)`.

## 3. Předání dat mimo EU

Fotka jde ke zpracování ke Googlu (Gemini + Drive). Původní text souhlasu tvrdil,
že se údaje **nepředávají mimo EU** — v MEATING verzi opraveno.
⚠️ **Stejná chybná formulace je pořád v živé aplikaci Peklo Čertovina.** Opravit.
Ve slajdu 10 je proto formulace „prověření dodavatelé, smluvní režim GDPR“,
ne „všechno zůstává v EU“.

## 4. Hlasování o špekáček — jeden telefon, jeden hlas

Obejití druhým telefonem nebo anonymním oknem se **neřeší** — takhle to bylo
odsouhlaseno se svazem 28. 8. Slajd 17 to podává jako přiměřené (je to anketa,
ne volby) a přidává kontrolu součtů proti počtu účastníků před vyhlášením.
Kdyby se někdo ptal víc, tohle je odpověď: dohodnuté řešení, ne opomenutí.

## 5. Certifikace — doplněno, jeden detail k hlídání

Slajd 4 je vyplněný z webu xlab.cz, etického kodexu a interní směrnice SM_GDPR_1:
ISO/IEC 27001, ISO/IEC 27701, EN ISO 9001, Výbor kybernetické bezpečnosti, interní
auditor, směrnice ochrany osobních údajů účinná od 1. 3. 2021, kontakt gdpr@xlab.cz,
mlčenlivost z VOP (čl. Mlčenlivost a ochrana důvěrných informací), povinnost vypořádat
práva třetích stran (VOP, „Souhlas s užitím“).

⚠️ Web říká doslova „designed in line with ISO 27001 and ISO27701“, ale zároveň
„According to Certification ISO27001, XLAB is committed to…“ — u **27001** je tedy
certifikace, u **27701** a **9001** je to soulad s normou. Slajd to tak i formuluje:
„ISO/IEC 27001 — certifikované řízení bezpečnosti informací“, u zbylých dvou jen název
normy bez slova certifikace. Kdyby se někdo doptal, tohle je přesná odpověď.
Pokud existuje i certifikát na 9001 nebo 27701, dá se slovo doplnit.

Certifikace **poskytovatelů technologií** (slajdy 5–6) jsou ověřené: ISO/IEC 27001 /
27017 / 27018 / 27701 a SOC 2 Type II. Záměrně tam nejsou jména konkrétních služeb —
mluví se o „velkých amerických poskytovatelích“. U EU–USA Data Privacy Framework je
formulace obecná („certifikovaní poskytovatelé“), protože ne každý z použitých
poskytovatelů je v seznamu DPF; u těch ostatních stojí přenos na standardních smluvních
doložkách. Obojí je podle GDPR plnohodnotný právní titul, takže tvrzení platí tak jako tak.
Vlastní pravidla pro přenos mimo EU má XLAB navíc v čl. 10.1 směrnice SM_GDPR_1.

## 6. Provozní tvrzení, která musí platit

Slajd 21 slibuje technika na místě po celou dobu akce a vypnutí kteréhokoli prvku
na dálku. Ověřit, že to sedí s nabídkou a rozpočtem (must have / optional, který
Julius čeká od 27. 8.).

## 7. Ukázkové obrázky na slajdu 9

Tři motivy (Hrdina oboru, Komiks, Řezník Krkovička) jsou staženy z Drive složky
`MEATING 2026 — Selfie Wall` (id 1QcBbuTeD_Rbt2EQIgumE9up8bHWVCoQ6), vznikly
11.–24. 8. 2026 při vývoji aplikace, tedy před akcí a na tvářích našeho týmu.
Uloženy zmenšené v `img/`.

⚠️ **Do prezentace vědomě nešly reálné selfie z Visy, hokeje ani 4FIN**, přestože
na Drive jsou. Jsou to výstupy skutečných návštěvníků a jejich použití k propagaci
by bylo v rozporu se souhlasem, který ti lidé odklikli — a v prezentaci, která slibuje
mazání fotek po akci, by to bylo obzvlášť nešťastné. Pokud chceš na slajd fotky
z reálné akce (kiosek, LED stěna, lidé u zdi zezadu), pošli je a doplním je;
záběry prostoru a instalace jsou bez problému.

## 8. Odkazy použité na slajdu 23

Ověřené: `xlab.cz/avatars` (z Notionu), `dataprivacyframework.gov`, GDPR 2016/679,
AI Act 2024/1689. Sekce Privacy / Terms / Code of Conduct / Technical Background jsou
uvedené názvem podle menu webu, ne přímou URL — přesné adresy jsem z tohoto prostředí
nemohl ověřit (blokovaný egress). Než to půjde ven jako PDF s prokliky, projdi je.
