# Interní poznámky k prezentaci — NEPOSÍLAT KLIENTOVI

Podle zadání nejsou slabiny v prezentaci. Tady je jejich seznam, aby se daly
v klidu dořešit po prezentaci.

## 1. Ověřit před tiskem — reference u avatarů

V Notionu jsou doložené: **ŠKODA AUTO** (Laurin, muzeum + Autostadt Wolfsburg),
**HOCHTIEF** (Stavomír), **ČSLH** (Puk / Síň slávy), **MULTIVAC / TVI**.

Nedoložené v Notionu, do prezentace zapsané podle zadání:
**Ernst & Young, Deloitte, Wella, Decathlon, zdravotnictví (pilot)**.
Před prezentací projít a případně vyškrtnout, co nemá oporu — jde o slajd 14.
U selfie zdi jsou naopak všechny uvedené reference doložené
(Visa, Wflow, ČSLH, 4FIN Kongres 2026, Peklo Čertovina, MULTIVAC/TVI).

## 2. Retence fotek — ve slajdech úmyslně NENÍ „30 dní“

Zadání znělo „mažou se po 30 dnech“. V MEATING verzi selfie aplikace
(`F:/Vibe-apps/multivac-meating-selfie/`) je ale **mazání podle stáří vypnuté**
a zůstal jen strop na počet souborů (2000). Text souhlasu je proto psaný jako
„uchování po dobu akce“, žádný slib 30 dnů. Slajd 9 říká „uchování jen po dobu akce,
po skončení konference se mažou“ — což je pravda a zároveň víc, než slibuje souhlas.

**Úkol:** před akcí buď zapnout automatické mazání s konkrétní lhůtou a slíbit ji
v souhlasu, nebo po akci složku ručně vyprázdnit a mít o tom záznam.
Pozor na past zapsanou v Notionu: `MAX_AGE_DAYS = 0` neznamená „nemazat“, ale
„smazat všechno“ — je na to pojistka `if (MAX_AGE_DAYS > 0)`.

## 3. Předání dat mimo EU

Fotka jde ke zpracování ke Googlu (Gemini + Drive). Původní text souhlasu tvrdil,
že se údaje **nepředávají mimo EU** — v MEATING verzi opraveno.
⚠️ **Stejná chybná formulace je pořád v živé aplikaci Peklo Čertovina.** Opravit.
Ve slajdu 9 je proto formulace „prověření dodavatelé, smluvní režim GDPR“,
ne „všechno zůstává v EU“.

## 4. Hlasování o špekáček — jeden telefon, jeden hlas

Obejití druhým telefonem nebo anonymním oknem se **neřeší** — takhle to bylo
odsouhlaseno se svazem 28. 8. Slajd 16 to podává jako přiměřené (je to anketa,
ne volby) a přidává kontrolu součtů proti počtu účastníků před vyhlášením.
Kdyby se někdo ptal víc, tohle je odpověď: dohodnuté řešení, ne opomenutí.

## 5. Certifikace na webu

Web `xlab.cz` nebyl z tohoto prostředí dostupný (blokovaný egress), takže
**konkrétní certifikáty a jejich odkazy nejsou v prezentaci vypsané** — nechtěl
jsem si je vymýšlet. Slajd 4 stojí na tom, co je doložitelné (GDPR, AI Act čl. 50,
smlouvy po právní kontrole) a odkazuje obecně na xlab.cz.

**Úkol před prezentací:** doplnit do slajdu 4 konkrétní názvy certifikací XLABu a přímé
odkazy z webu. V HTML je to sekce `<!-- 4 — CERTIFIKACE -->`, stačí přidat
odrážky do karty „Ochrana údajů“ a upravit poslední řádek `.note`.

Certifikace **poskytovatelů technologií** (slajdy 5–6) v prezentaci naopak jsou a jsou ověřené:
ISO/IEC 27001 / 27017 / 27018 / 27701 a SOC 2 Type II. Záměrně tam nejsou jména konkrétních
služeb — mluví se o „velkých amerických poskytovatelích“. U EU–USA Data Privacy Framework je
formulace obecná („certifikovaní poskytovatelé“), protože ne každý z použitých poskytovatelů
je v seznamu DPF; u těch ostatních stojí přenos na standardních smluvních doložkách. Obojí je
podle GDPR plnohodnotný právní titul, takže tvrzení na slajdu platí tak jako tak.

## 6. Provozní tvrzení, která musí platit

Slajd 20 slibuje technika na místě po celou dobu akce a vypnutí kteréhokoli prvku
na dálku. Ověřit, že to sedí s nabídkou a rozpočtem (must have / optional, který
Julius čeká od 27. 8.).
