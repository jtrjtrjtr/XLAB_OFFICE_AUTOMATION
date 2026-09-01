# Interní poznámky k prezentaci — NEPOSÍLAT KLIENTOVI

Prezentace má 13 slajdů. Slabiny podle zadání nejsou v prezentaci, jsou tady.

## 1. Ověřit před tiskem — reference u avatarů (slajd 2)

Doložené v Notionu: **ŠKODA AUTO** (Laurin, muzeum + Autostadt Wolfsburg),
**HOCHTIEF** (Stavomír), **ČSLH** (Puk / Síň slávy), **MULTIVAC / TVI**.

Nedoložené, do prezentace zapsané podle zadání: **Ernst & Young, Deloitte, Wella,
Decathlon, zdravotnictví (pilot)**. Projít a případně vyškrtnout.
U selfie zdi jsou všechny reference doložené.

## 2. 🔴 Retence fotek — slajdy 5 a 6 slibují TŘI DNY

Podle zadání Sebastiana (1. 9.) je na slajdech napsáno: vstupní fotka se po vygenerování
**okamžitě maže**, hotový stylizovaný obrázek se maže **po třech dnech, jak je uvedeno
v podmínkách**.

⚠️ **Tohle si musí někdo ověřit proti kódu, než to zazní před svazem.** V zápisu z 11. 8.
stojí, že v MEATING verzi (`F:/Vibe-apps/multivac-meating-selfie/`) je **mazání podle
stáří vypnuté** a zůstal jen strop na počet souborů (2000), a že text souhlasu slibuje
„uchování po dobu akce“, žádnou konkrétní lhůtu. Pokud se od té doby nic nezměnilo,
prezentace slibuje víc, než aplikace dělá — a je to slib o mazání osobních údajů,
tedy přesně to, na co se svaz ptá.

**Úkol před akcí:** zapnout automatické mazání po třech dnech a sladit s ním text
souhlasu. Pozor: `MAX_AGE_DAYS = 0` neznamená „nemazat“, ale „smazat všechno“ —
je na to pojistka `if (MAX_AGE_DAYS > 0)`.

## 3. Předání dat mimo EU (slajdy 4 a 6)

Fotka jde ke zpracování ke Googlu (Gemini + Drive). Původní text souhlasu tvrdil, že se
údaje **nepředávají mimo EU** — v MEATING verzi opraveno.
⚠️ **Stejná chybná formulace je pořád v živé aplikaci Peklo Čertovina.** Opravit.

U EU–USA Data Privacy Framework je na slajdu obecná formulace, protože ne každý
poskytovatel je v seznamu DPF; u ostatních stojí přenos na standardních smluvních
doložkách. Obojí je podle GDPR plnohodnotný právní titul. Vlastní pravidla pro přenos
mimo EU má XLAB v čl. 10.1 směrnice SM_GDPR_1.

## 4. Hlasování o špekáček (slajd 9)

Obejití druhým telefonem nebo anonymním oknem se **neřeší** — takhle to bylo odsouhlaseno
se svazem 28. 8. Slajd to podává jako přiměřené a přidává kontrolu součtů proti počtu
účastníků před vyhlášením. Kdyby se někdo ptal víc: dohodnuté řešení, ne opomenutí.

## 5. Certifikace XLABu (slajd 3)

Web říká „designed in line with ISO 27001 and ISO27701“, ale zároveň „According to
Certification ISO27001, XLAB is committed to…“. U **27001** je tedy certifikace,
u **27701** a **9001** soulad s normou. Slajd to tak i formuluje — slovo „certifikát“
je jen u 27001. Pokud existuje certifikát i na ostatní, dá se doplnit.

## 6. Provozní tvrzení (slajd 11)

Slajd slibuje technika na místě po celou dobu akce a vypnutí kteréhokoli prvku na dálku.
Ověřit, že to sedí s nabídkou a rozpočtem (must have / optional, který Julius čeká od 27. 8.).

## 7. Ukázkové obrázky a argument o deepfake (slajd 7)

Slajd se jmenuje „Není to deepfake“ a nese argument: podoba se schválně nezachovává
přesně, výstup je stylizovaný, deepfake je oproti tomu realistická fotka/video vydávané
za skutečné.

⚠️ **Chybí referenční vstupní fotografie** vedle výstupů. Klient ji chce vidět, aby bylo
poznat, jak moc se podoba změnila. Nemám žádnou vstupní fotku — aplikace ukládá na Drive
jen hotové obrázky. Stačí poslat jednu fotku (vlastní nebo od kolegy se souhlasem)
a doplním layout „vstup → výstupy“.


⚠️ **Motiv Řezník Krkovička ze slajdu vyřazen.** Všechny rendery na Drive (12.–24. 8.)
jsou loutková varianta. Podle deníku z 18. 8. je motiv **neuzavřený spor**: klient chce
hosty tlusté, plešaté a zrzavé jako v předloze, my jsme poslali věcný argument proti
a nabídku střední cesty; Sebastian navíc nabídl, že Krkovičku může nahradit Hrdina
(kategorie mají zůstat čtyři kvůli sudému počtu). Do prezentace pro svaz proto nešel —
ukazovat motiv, který klient odmítl, by v jednání o bezpečnosti otevřelo úplně jinou
debatu. Až bude schválená verze, doplní se zpět jako čtvrtá dlaždice.

Tři motivy staženy z Drive složky `MEATING 2026 — Selfie Wall`
(id 1QcBbuTeD_Rbt2EQIgumE9up8bHWVCoQ6), vzniklé 17.–24. 8. 2026 při vývoji, tedy po
přestylizování motivů do kresby a na tvářích našeho týmu. Starší snímek z 13. 8.
(motiv Hrdina, před přestylizováním) byl vyřazen.

⚠️ **Chybí `Ukazky_motivu_SelfieWall.png`** ze složky `PRO_KLIENTA_2026-08-17` na disku F:
— to je ta srovnávací tabulka 12 snímků (muž / žena / dvojice × 4 motivy), kterou dostal
klient. Na Google Drive ani v Gmailu není a na F: se odsud nedostanu. Stejně tak chybí
**vstupní fotka** pro dvojici vstup → výstup. Obojí stačí poslat a vyměním to za jednu
mřížku.

⚠️ **Do prezentace vědomě nešly reálné selfie z Visy, hokeje ani 4FIN**, přestože na
Drive jsou. Jsou to výstupy skutečných návštěvníků a jejich použití k propagaci by bylo
v rozporu se souhlasem, který odklikli — a v prezentaci slibující mazání fotek po akci
obzvlášť. Záběry prostoru, kiosku a instalace jsou bez problému.

## 8. Odkazy (slajd 13)

Ověřené: `xlab.cz/avatars` (z Notionu), GDPR 2016/679, AI Act 2024/1689. Sekce
Privacy / Terms / Code of Conduct jsou uvedené názvem podle menu webu, ne přímou URL —
přesné adresy jsem z tohoto prostředí nemohl ověřit (blokovaný egress). Projít.
