const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  ImageRun, PageBreak, Footer, Header, PageNumber, LevelFormat, convertInchesToTwip,
} = require("docx");

const INK = "1A1A1A";
const GRAY = "4A4A4A";
const GRAY2 = "666666";
const YELLOW = "E3E829";
const RULE = "D6D5CF";
const CARD = "EFEFEF";
const FONT = "Arial";

const LOGO = "/tmp/claude-0/-home-user-XLAB-OFFICE-AUTOMATION/a99ca070-c2a3-531c-a6dc-969708675b21/scratchpad/opt/x_logo_black.png";

/* ---------- helpers ---------- */

const yellowRule = (space = 160) =>
  new Paragraph({
    spacing: { before: 40, after: space },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: YELLOW, space: 1 } },
  });

const thinRule = (space = 160) =>
  new Paragraph({
    spacing: { before: 40, after: space },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 1 } },
  });

// článek nadpis
const h1 = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 320, after: 140 },
    keepNext: true,
    children: [new TextRun({ text, bold: true, size: 24, color: INK, font: FONT })],
  });

const h2 = (text) =>
  new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 260, after: 120 },
    keepNext: true,
    children: [new TextRun({ text, bold: true, size: 21, color: GRAY, font: FONT })],
  });

// číslovaný odstavec "1.1 text"
const cl = (num, runs, opts = {}) =>
  new Paragraph({
    spacing: { after: 120, line: 264 },
    indent: { left: 567, hanging: 567 },
    alignment: AlignmentType.JUSTIFIED,
    children: [
      new TextRun({ text: num + "\t", bold: true, size: 20, color: INK, font: FONT }),
      ...(typeof runs === "string"
        ? [new TextRun({ text: runs, size: 20, color: INK, font: FONT })]
        : runs),
    ],
    ...opts,
  });

const t = (text, o = {}) =>
  new TextRun({ text, size: o.size || 20, bold: !!o.b, italics: !!o.i, color: o.c || INK, font: FONT });

const p = (text, o = {}) =>
  new Paragraph({
    spacing: { after: o.after === undefined ? 120 : o.after, line: 264 },
    alignment: o.align || AlignmentType.LEFT,
    indent: o.indent,
    children: typeof text === "string" ? [t(text, o)] : text,
  });

const bullet = (text) =>
  new Paragraph({
    numbering: { reference: "dash", level: 0 },
    spacing: { after: 80, line: 264 },
    children: typeof text === "string" ? [t(text)] : text,
  });

/* ---------- tabulky ---------- */

const TW = 9026; // šířka obsahu A4 při okrajích 1"

function table(colWidths, rows, opts = {}) {
  return new Table({
    columnWidths: colWidths,
    width: { size: TW, type: WidthType.DXA },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: RULE },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: RULE },
      left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: RULE },
      insideVertical: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
    },
    rows: rows.map((cells, ri) =>
      new TableRow({
        tableHeader: ri === 0 && opts.header !== false,
        children: cells.map((c, ci) =>
          new TableCell({
            width: { size: colWidths[ci], type: WidthType.DXA },
            margins: { top: 90, bottom: 90, left: 110, right: 110 },
            shading: ri === 0 && opts.header !== false
              ? { type: ShadingType.CLEAR, fill: CARD, color: "auto" }
              : undefined,
            children: (Array.isArray(c) ? c : [c]).map((line) =>
              new Paragraph({
                spacing: { after: 0, line: 252 },
                children: [
                  new TextRun({
                    text: line,
                    size: 18,
                    bold: ri === 0 && opts.header !== false,
                    color: ri === 0 && opts.header !== false ? GRAY : INK,
                    font: FONT,
                  }),
                ],
              })
            ),
          })
        ),
      })
    ),
  });
}

/* ---------- obsah ---------- */

const cover = [
  new Paragraph({
    spacing: { after: 200 },
    children: [
      new ImageRun({
        type: "png",
        data: fs.readFileSync(LOGO),
        transformation: { width: 150, height: 27 },
      }),
    ],
  }),
  yellowRule(420),
  new Paragraph({
    spacing: { after: 160 },
    children: [t("SMLOUVA O ZPRACOVÁNÍ", { b: true, size: 34 })],
  }),
  new Paragraph({
    spacing: { after: 260 },
    children: [t("OSOBNÍCH ÚDAJŮ", { b: true, size: 34 })],
  }),
  p([t("uzavřená podle čl. 28 odst. 3 nařízení Evropského parlamentu a Rady (EU) 2016/679", { size: 21, c: GRAY })], { after: 60 }),
  p([t("o ochraně fyzických osob v souvislosti se zpracováním osobních údajů (GDPR)", { size: 21, c: GRAY })], { after: 400 }),
  p([t("Konference MEATING 2026", { b: true, size: 22 })], { after: 60 }),
  p([t("20. října 2026, OREA Congress Hotel Brno", { size: 20, c: GRAY2 })], { after: 60 }),
  p([t("Interaktivní technologie: selfie zeď, eventová aplikace s kvízem a hlasováním, digitální avatar", { size: 20, c: GRAY2 })], { after: 700 }),
  thinRule(140),
  p([t("Návrh k právní kontrole. Pole označená [DOPLNIT] je nutné vyplnit před podpisem.", { size: 18, c: GRAY2, i: true })], { after: 0 }),
  new Paragraph({ children: [new PageBreak()] }),
];

const strany = [
  h1("Smluvní strany"),

  p([t("Správce", { b: true, size: 21 })], { after: 100 }),
  ...[
    "Obchodní firma: [DOPLNIT — Český svaz zpracovatelů masa, z. s. / MULTIVAC VERPACKUNGSMASCHINEN ČESKÁ REPUBLIKA s.r.o.]",
    "Sídlo: [DOPLNIT]",
    "IČO: [DOPLNIT]   ·   DIČ: [DOPLNIT]",
    "Zapsán: [DOPLNIT — spolkový / obchodní rejstřík, oddíl a vložka]",
    "Zastoupen: [DOPLNIT]",
    "Kontaktní osoba pro ochranu osobních údajů: [DOPLNIT — jméno, e-mail]",
  ].map((x) => p(x, { after: 40 })),
  p([t("(dále jen ", { c: GRAY }), t("„Správce“", { b: true }), t(")", { c: GRAY })], { after: 240 }),

  p([t("Zpracovatel", { b: true, size: 21 })], { after: 100 }),
  ...[
    "Obchodní firma: XLAB s.r.o.",
    "Sídlo: Výstaviště 67, 170 00 Praha 7",
    "IČO: [DOPLNIT]   ·   DIČ: [DOPLNIT]",
    "Zapsána: [DOPLNIT — obchodní rejstřík, oddíl a vložka]",
    "Zastoupena: Ing. Jindřich Trapl, jednatel",
    "Kontaktní adresa pro ochranu osobních údajů: gdpr@xlab.cz",
  ].map((x) => p(x, { after: 40 })),
  p([t("(dále jen ", { c: GRAY }), t("„Zpracovatel“", { b: true }), t("; společně dále jen ", { c: GRAY }), t("„Smluvní strany“", { b: true }), t(")", { c: GRAY })], { after: 260 }),
];

const cl1 = [
  h1("Článek 1 — Úvodní ustanovení a role Smluvních stran"),
  cl("1.1", "Smluvní strany uzavřely smlouvu o dílo / objednávku č. [DOPLNIT] ze dne [DOPLNIT], jejímž předmětem je dodání a provoz interaktivních technologií na konferenci MEATING 2026 (dále jen „Hlavní smlouva“). Při plnění Hlavní smlouvy dochází ke zpracování osobních údajů."),
  cl("1.2", [
    t("Správce určuje účely a prostředky zpracování osobních údajů a je správcem ve smyslu čl. 4 bodu 7 GDPR. Zpracovatel zpracovává osobní údaje výhradně pro Správce a je zpracovatelem ve smyslu čl. 4 bodu 8 GDPR. "),
    t("Smluvní strany výslovně vylučují, že by byly společnými správci podle čl. 26 GDPR.", { b: true }),
  ]),
  cl("1.3", "Tato smlouva upravuje vzájemná práva a povinnosti Smluvních stran při zpracování osobních údajů a tvoří nedílnou součást Hlavní smlouvy. V případě rozporu mají ustanovení této smlouvy přednost ve věcech ochrany osobních údajů."),
  cl("1.4", "Zpracovatel prohlašuje, že má zaveden systém řízení bezpečnosti informací podle normy ISO/IEC 27001, k níž je držitelem certifikátu, a že své postupy vede rovněž v souladu s normami ISO/IEC 27701 a EN ISO 9001. Zpracovatel má zřízen vlastní Výbor kybernetické bezpečnosti a funkci interního auditora kybernetické bezpečnosti a řídí se vnitřní směrnicí Politika ochrany osobních údajů účinnou od 1. 3. 2021."),
];

const cl2 = [
  h1("Článek 2 — Předmět, povaha, účel a doba zpracování"),
  cl("2.1", "Předmětem zpracování jsou osobní údaje účastníků konference MEATING 2026 v rozsahu nezbytném pro provoz interaktivních prvků konference. Podrobný popis jednotlivých zpracování, kategorií subjektů údajů, kategorií osobních údajů a dob uložení je uveden v Příloze č. 1, která tvoří nedílnou součást této smlouvy."),
  cl("2.2", [
    t("Smluvní strany se shodly, že "),
    t("při zpracování nedochází ke zpracování zvláštních kategorií osobních údajů podle čl. 9 GDPR", { b: true }),
    t(". Stylizovaná podobizna vytvořená aplikací selfie zdi není biometrickým údajem ve smyslu čl. 4 bodu 14 GDPR, neboť nedochází ke specifickému technickému zpracování za účelem jedinečné identifikace fyzické osoby (srov. recitál 51 GDPR, Guidelines EDPB 3/2019, body 74–82, a stanovisko Úřadu pro ochranu osobních údajů)."),
  ]),
  cl("2.3", "Zpracovatel nezpracovává jména, adresy, e-mailové adresy, telefonní čísla, platební údaje ani jiné identifikační údaje účastníků. Aplikace nevyžadují registraci ani přihlášení a nevyužívají soubory cookies pro analytické ani marketingové účely."),
  cl("2.4", "Zpracování probíhá po dobu přípravy, konání a bezprostředního vyhodnocení konference, nejdéle však do [DOPLNIT — např. 30. 11. 2026], není-li v Příloze č. 1 u konkrétního zpracování stanovena kratší doba."),
];

const cl3 = [
  h1("Článek 3 — Pokyny Správce"),
  cl("3.1", "Zpracovatel zpracovává osobní údaje pouze na základě doložených pokynů Správce, včetně pokynů týkajících se předání osobních údajů do třetí země, ledaže mu takové zpracování ukládá právo Evropské unie nebo členského státu; v takovém případě Zpracovatel Správce o tomto právním požadavku před zpracováním informuje, pokud to dané právo nezakazuje."),
  cl("3.2", "Tato smlouva a její přílohy představují úplný a doložený pokyn Správce ke zpracování ke dni jejího podpisu. Změny pokynů se provádějí písemně, postačí formou e-mailu na kontaktní adresy uvedené v záhlaví."),
  cl("3.3", "Zpracovatel neprodleně informuje Správce, má-li za to, že pokyn Správce porušuje GDPR nebo jiné právní předpisy o ochraně osobních údajů."),
  cl("3.4", "Zpracovatel nepoužívá osobní údaje pro vlastní účely, zejména je nepoužívá k propagaci, k tvorbě referencí ani k trénování modelů umělé inteligence, a nepředává je třetím osobám s výjimkou dalších zpracovatelů podle článku 6."),
];

const cl4 = [
  h1("Článek 4 — Povinnosti Zpracovatele"),
  cl("4.1", "Zpracovatel zajistí, aby se osoby oprávněné zpracovávat osobní údaje zavázaly k mlčenlivosti nebo aby se na ně vztahovala zákonná povinnost mlčenlivosti. Mlčenlivost trvá i po skončení této smlouvy a po skončení pracovněprávního či obdobného vztahu těchto osob ke Zpracovateli."),
  cl("4.2", "Zpracovatel své pracovníky pravidelně školí v oblasti ochrany osobních údajů a bezpečnosti informací a přístup k osobním údajům uděluje výhradně podle rolí, v rozsahu nezbytném pro plnění pracovních úkolů."),
  cl("4.3", "Zpracovatel přijal a udržuje technická a organizační opatření podle čl. 32 GDPR, jejichž přehled tvoří Přílohu č. 3 této smlouvy."),
  cl("4.4", "Zpracovatel je Správci nápomocen prostřednictvím vhodných technických a organizačních opatření při plnění povinnosti Správce reagovat na žádosti o výkon práv subjektů údajů podle kapitoly III GDPR, a to bez zbytečného odkladu po obdržení žádosti Správce."),
  cl("4.5", "Zpracovatel je Správci nápomocen při zajišťování souladu s povinnostmi podle čl. 32 až 36 GDPR, zejména při ohlašování případů porušení zabezpečení a při případném posouzení vlivu na ochranu osobních údajů."),
  cl("4.6", "Obdrží-li Zpracovatel žádost subjektu údajů týkající se zpracování prováděného pro Správce, nevyřizuje ji sám a bez zbytečného odkladu ji předá Správci."),
  cl("4.7", "Zpracovatel poskytne Správci veškeré informace nezbytné k doložení, že byly splněny povinnosti stanovené v čl. 28 GDPR, a umožní audity, včetně inspekcí, prováděné Správcem nebo jiným auditorem, kterého Správce pověřil. Audit se ohlašuje nejméně 15 dnů předem, koná se v pracovní době a nesmí nepřiměřeně zasahovat do provozu Zpracovatele."),
];

const cl5 = [
  h1("Článek 5 — Porušení zabezpečení osobních údajů"),
  cl("5.1", [
    t("Zpracovatel ohlásí Správci jakékoli porušení zabezpečení osobních údajů "),
    t("bez zbytečného odkladu, nejpozději do 24 hodin", { b: true }),
    t(" od okamžiku, kdy se o něm dozvěděl, aby Správce mohl dostát své lhůtě podle čl. 33 odst. 1 GDPR."),
  ]),
  cl("5.2", "Ohlášení obsahuje popis povahy porušení, kategorie a přibližný počet dotčených subjektů údajů a záznamů, pravděpodobné důsledky, přijatá či navrhovaná opatření k nápravě a kontaktní údaje osoby, u které lze získat další informace. Nelze-li poskytnout všechny informace současně, poskytne je Zpracovatel postupně bez dalšího zbytečného odkladu."),
  cl("5.3", "Zpracovatel vede evidenci případů porušení zabezpečení a na žádost ji Správci zpřístupní."),
];

const cl6 = [
  h1("Článek 6 — Další zpracovatelé"),
  cl("6.1", "Správce uděluje Zpracovateli obecné povolení zapojit do zpracování další zpracovatele. Seznam dalších zpracovatelů schválených ke dni podpisu této smlouvy tvoří Přílohu č. 2."),
  cl("6.2", "Zpracovatel informuje Správce o zamýšlené změně spočívající v přijetí dalších zpracovatelů nebo jejich nahrazení nejméně 15 dnů předem. Správce může proti změně vznést odůvodněnou námitku ve lhůtě 10 dnů od oznámení; v takovém případě se Smluvní strany pokusí najít náhradní řešení. Nebude-li nalezeno, je Správce oprávněn dotčenou část plnění vypovědět."),
  cl("6.3", "Zpracovatel uloží dalšímu zpracovateli stejné povinnosti na ochranu osobních údajů, jaké jsou uvedeny v této smlouvě, a odpovídá Správci za plnění povinností dalšího zpracovatele v plném rozsahu."),
];

const cl7 = [
  h1("Článek 7 — Předávání osobních údajů do třetích zemí"),
  cl("7.1", "K předání osobních údajů do třetí země dochází pouze v rozsahu uvedeném v Příloze č. 2 a pouze při splnění podmínek kapitoly V GDPR."),
  cl("7.2", "U příjemců se sídlem ve Spojených státech amerických je předání založeno na rozhodnutí Evropské komise o odpovídající úrovni ochrany ze dne 10. 7. 2023 (rámec EU — USA pro ochranu osobních údajů, Data Privacy Framework), je-li příjemce v příslušném seznamu certifikován, jinak na standardních smluvních doložkách přijatých Evropskou komisí."),
  cl("7.3", "Zpracovatel prohlašuje, že u každého dalšího zpracovatele uvedeného v Příloze č. 2 ověřil existenci právního titulu podle odstavce 7.2 a že tento titul doloží Správci na jeho žádost. Přestane-li být titul platný, Zpracovatel o tom Správce neprodleně informuje a zpracování u dotčeného příjemce pozastaví."),
  cl("7.4", "Zpracovatel prohlašuje, že u služeb určených pro firemní zákazníky a vývojářské rozhraní je smluvně vyloučeno použití předávaných údajů k trénování modelů umělé inteligence poskytovatele."),
];

const cl8 = [
  h1("Článek 8 — Výmaz a vrácení osobních údajů"),
  cl("8.1", "Osobní údaje se vymazávají ve lhůtách uvedených v Příloze č. 1. Vstupní fotografie pořízená účastníkem se v aplikaci selfie zdi vymazává bezprostředně po vytvoření stylizovaného obrázku."),
  cl("8.2", "Po ukončení poskytování služeb spojených se zpracováním Zpracovatel podle rozhodnutí Správce všechny osobní údaje vymaže nebo je Správci vrátí a vymaže existující kopie, ledaže právo Evropské unie nebo členského státu ukládá jejich uložení."),
  cl("8.3", "Provedení výmazu Zpracovatel Správci na jeho žádost písemně potvrdí, a to nejpozději do 15 dnů od ukončení zpracování."),
];

const cl9 = [
  h1("Článek 9 — Umělá inteligence a transparentnost"),
  cl("9.1", [
    t("Při plnění se používají systémy umělé inteligence. Zpracovatel zajistí, aby obsah vytvořený umělou inteligencí byl jako takový "),
    t("viditelně označen", { b: true }),
    t(" a aby účastníci byli přiměřeným způsobem informováni, že komunikují se systémem umělé inteligence, v souladu s čl. 50 nařízení Evropského parlamentu a Rady (EU) 2024/1689 (akt o umělé inteligenci)."),
  ]),
  cl("9.2", "Digitální avatar se v úvodu interakce představí jako digitální postava vytvořená umělou inteligencí. Informace o použití umělé inteligence je rovněž součástí textu souhlasu v aplikaci selfie zdi."),
  cl("9.3", "Je-li při plnění použit hlas nebo podoba konkrétní fyzické osoby, uzavře se k tomu samostatná smlouva o souhlasu s užitím hlasu a podoby mezi mluvčím, Správcem a Zpracovatelem. Bez podepsaného souhlasu nesmí být hlas ani podoba užity."),
  cl("9.4", "Zpracovatel prohlašuje, že k předmětům duševního vlastnictví užitým při plnění má potřebná oprávnění a že k nim nejsou uplatňována práva třetích osob, která by bránila užití sjednanému v Hlavní smlouvě."),
];

const cl10 = [
  h1("Článek 10 — Odpovědnost"),
  cl("10.1", "Každá ze Smluvních stran odpovídá za újmu způsobenou porušením svých povinností podle GDPR a této smlouvy. Zpracovatel odpovídá za újmu způsobenou zpracováním pouze v rozsahu podle čl. 82 odst. 2 GDPR."),
  cl("10.2", "Uloží-li dozorový úřad Správci pokutu výlučně z důvodu porušení povinností Zpracovatele podle této smlouvy, má Správce právo na náhradu takto vzniklé újmy. Limitace náhrady újmy sjednaná v Hlavní smlouvě se použije obdobně, nestanoví-li kogentní právní úprava jinak."),
];

const cl11 = [
  h1("Článek 11 — Doba trvání a ukončení"),
  cl("11.1", "Tato smlouva se uzavírá na dobu trvání Hlavní smlouvy a trvá po dobu, po kterou Zpracovatel zpracovává osobní údaje pro Správce."),
  cl("11.2", "Ustanovení o mlčenlivosti, o výmazu údajů a o odpovědnosti trvají i po ukončení této smlouvy."),
];

const cl12 = [
  h1("Článek 12 — Závěrečná ustanovení"),
  cl("12.1", "Tato smlouva se řídí právním řádem České republiky, zejména GDPR a zákonem č. 110/2019 Sb., o zpracování osobních údajů. Dozorovým úřadem je Úřad pro ochranu osobních údajů."),
  cl("12.2", "Změny této smlouvy se provádějí písemnými číslovanými dodatky podepsanými oběma Smluvními stranami. Změnu příloh č. 2 a 3 lze provést postupem podle článku 6, resp. písemným oznámením Zpracovatele."),
  cl("12.3", "Je-li některé ustanovení této smlouvy neplatné nebo neúčinné, nemá to vliv na platnost ostatních ustanovení. Smluvní strany nahradí takové ustanovení ustanovením, které se svým účelem nejvíce blíží ustanovení nahrazovanému."),
  cl("12.4", "Tato smlouva je vyhotovena ve dvou stejnopisech, z nichž každá Smluvní strana obdrží po jednom, nebo je uzavřena elektronicky s uznávanými elektronickými podpisy."),
  cl("12.5", "Nedílnou součástí této smlouvy jsou přílohy: Příloha č. 1 — Popis zpracování; Příloha č. 2 — Další zpracovatelé; Příloha č. 3 — Technická a organizační opatření."),
  cl("12.6", "Smluvní strany prohlašují, že si smlouvu přečetly, že vyjadřuje jejich pravou a svobodnou vůli, a na důkaz toho připojují své podpisy."),
];

const podpisy = [
  new Paragraph({ spacing: { before: 520, after: 0 }, children: [t("V [DOPLNIT] dne [DOPLNIT]", { c: GRAY })] }),
  new Paragraph({ spacing: { before: 560, after: 0 }, children: [] }),
  table([4513, 4513], [
    ["", ""],
    ["Za Správce", "Za Zpracovatele"],
    ["[DOPLNIT — jméno, funkce]", "Ing. Jindřich Trapl, jednatel"],
    ["[DOPLNIT — název organizace]", "XLAB s.r.o."],
  ], { header: false }),
];

/* ---------- přílohy ---------- */

const priloha1 = [
  new Paragraph({ children: [new PageBreak()] }),
  h1("Příloha č. 1 — Popis zpracování"),
  p("Popis odpovídá požadavkům čl. 28 odst. 3 GDPR. Uvedené doby uložení jsou nejzazší; údaje se vymazávají dříve, jakmile pomine účel.", { c: GRAY, after: 220 }),

  h2("A. Selfie zeď — stylizovaný portrét"),
  table([2000, 7026], [
    ["Položka", "Popis"],
    ["Účel zpracování", "Vytvoření stylizovaného obrázku (kresby) z fotografie účastníka jako zábavního prvku konference a jeho zobrazení na obrazovce v místě konání."],
    ["Povaha zpracování", "Automatizované zpracování obrazu generativním modelem umělé inteligence, dočasné uložení výstupu, zobrazení, stažení účastníkem."],
    ["Kategorie subjektů údajů", "Účastníci konference, kteří se dobrovolně a na základě souhlasu vyfotí."],
    ["Kategorie osobních údajů", "Podobizna účastníka ve vstupní fotografii; stylizovaný obrázek vytvořený umělou inteligencí. Žádné identifikační ani kontaktní údaje."],
    ["Právní základ na straně Správce", "Souhlas subjektu údajů podle čl. 6 odst. 1 písm. a) GDPR, udělený v aplikaci před pořízením fotografie."],
    ["Doba uložení — vstupní fotografie", "Vymazána bezprostředně po vytvoření stylizovaného obrázku; neukládá se trvale."],
    ["Doba uložení — stylizovaný obrázek", "Nejdéle 3 dny od vytvoření, poté automatický výmaz."],
    ["Zvláštní kategorie údajů", "Nezpracovávají se. Nedochází k biometrické identifikaci; systém nemá databázi podobizen a neprovádí porovnávání."],
  ]),

  h2("B. Eventová aplikace, kvíz a hlasování"),
  table([2000, 7026], [
    ["Položka", "Popis"],
    ["Účel zpracování", "Zpřístupnění programu a informací o konferenci, provoz vědomostního kvízu a anketního hlasování o nejlepší výrobek."],
    ["Povaha zpracování", "Webová aplikace bez registrace. Ukládání stavu výhradně v prohlížeči zařízení účastníka; na straně Zpracovatele pouze anonymní součty hlasů."],
    ["Kategorie subjektů údajů", "Účastníci konference."],
    ["Kategorie osobních údajů", "Žádné identifikační údaje. V zařízení účastníka se ukládá pouze údaj o odehraném kvízu a údaj o tom, že ze zařízení již bylo hlasováno."],
    ["Právní základ na straně Správce", "Oprávněný zájem Správce na organizaci konference podle čl. 6 odst. 1 písm. f) GDPR."],
    ["Doba uložení", "Údaje v prohlížeči do jejich smazání uživatelem. Anonymní součty hlasů po dobu konání konference a jejího vyhodnocení."],
    ["Soubory cookies", "Aplikace nepoužívá cookies pro analytické ani marketingové účely a nepředává údaje třetím stranám za účelem reklamy."],
  ]),

  h2("C. Digitální avatar (kiosek)"),
  table([2000, 7026], [
    ["Položka", "Popis"],
    ["Účel zpracování", "Informační a navigační průvodce konferencí formou hlasové interakce s digitální postavou."],
    ["Povaha zpracování", "Provoz aplikace na zařízení umístěném v místě konání. Obrazový signál z kamery slouží výhradně k detekci přítomnosti osoby před kioskem."],
    ["Kategorie subjektů údajů", "Návštěvníci, kteří přistoupí ke kiosku."],
    ["Kategorie osobních údajů", "Obrazový signál zpracovávaný pouze v operační paměti zařízení; obsah dotazu položeného návštěvníkem."],
    ["Právní základ na straně Správce", "Oprávněný zájem Správce podle čl. 6 odst. 1 písm. f) GDPR."],
    ["Doba uložení", "Žádná. Obrazový signál se neukládá na datové úložiště ani neopouští zařízení. Obsah interakce se po jejím skončení neuchovává."],
    ["Zvláštní kategorie údajů", "Nezpracovávají se. Systém neprovádí rozpoznávání osob ani nemá databázi podobizen."],
  ]),
];

const priloha2 = [
  new Paragraph({ children: [new PageBreak()] }),
  h1("Příloha č. 2 — Další zpracovatelé"),
  p("Seznam dalších zpracovatelů schválených Správcem ke dni podpisu této smlouvy podle článku 6 této smlouvy.", { c: GRAY, after: 220 }),
  table([2100, 2400, 1500, 3026], [
    ["Další zpracovatel", "Předmět zpracování", "Umístění", "Právní titul pro předání"],
    ["Google Ireland Limited / Google LLC", "Generativní zpracování obrazu a dočasné úložiště výstupů selfie zdi", "EU / USA", "Rámec EU — USA pro ochranu osobních údajů; standardní smluvní doložky ve smlouvě o zpracování údajů"],
    ["[DOPLNIT — poskytovatel hostingu webových aplikací]", "Provoz a doručování webových aplikací", "[DOPLNIT]", "[DOPLNIT — DPF / standardní smluvní doložky]"],
    ["[DOPLNIT — poskytovatel syntézy hlasu, pouze je-li využita]", "Syntéza hlasu digitálního avatara", "[DOPLNIT]", "[DOPLNIT]"],
  ]),
  p("Zpracovatel prohlašuje, že u každého z uvedených příjemců ověřil platnost uvedeného právního titulu a že tuto skutečnost Správci na žádost doloží.", { c: GRAY, after: 0 }),
];

const priloha3 = [
  new Paragraph({ children: [new PageBreak()] }),
  h1("Příloha č. 3 — Technická a organizační opatření"),
  p("Přehled opatření přijatých Zpracovatelem podle čl. 32 GDPR.", { c: GRAY, after: 220 }),

  h2("Řízení bezpečnosti"),
  bullet("Systém řízení bezpečnosti informací podle ISO/IEC 27001, k níž je Zpracovatel držitelem certifikátu; postupy vedené v souladu s ISO/IEC 27701 a EN ISO 9001."),
  bullet("Vlastní Výbor kybernetické bezpečnosti, garant kybernetické bezpečnosti a interní auditor kybernetické bezpečnosti."),
  bullet("Vnitřní směrnice Politika ochrany osobních údajů účinná od 1. 3. 2021, pravidelné interní audity zpracovatelských procesů."),
  bullet("Pravidelná školení pracovníků, závazek mlčenlivosti trvající i po skončení spolupráce."),

  h2("Minimalizace údajů"),
  bullet("Aplikace nevyžadují registraci, přihlášení ani zadání jména, adresy, e-mailu, telefonu či platebních údajů."),
  bullet("Nezpracovávají se zvláštní kategorie osobních údajů ani údaje o dětech pod hranicí stanovenou právními předpisy bez souhlasu zákonného zástupce."),
  bullet("Vstupní fotografie se po vytvoření výstupu bezprostředně maže; ukládá se pouze stylizovaný obrázek."),
  bullet("Aplikace nepoužívají cookies pro analytické ani marketingové účely."),

  h2("Ochrana přístupu a přenosu"),
  bullet("Šifrování při přenosu (TLS) i při uložení."),
  bullet("Řízení přístupu podle rolí, přístup výhradně v rozsahu nezbytném pro plnění pracovních úkolů."),
  bullet("Oddělení prostředí pro vývoj a produkční provoz; správa přístupových údajů mimo zdrojový kód."),

  h2("Odolnost provozu"),
  bullet("Zpracování obrazu z kamery kiosku probíhá výhradně lokálně v zařízení; snímky se neukládají ani neodesílají."),
  bullet("Kiosek je provozuschopný i bez připojení k internetu v režimu s lokálními modely umělé inteligence."),
  bullet("Každý interaktivní prvek lze samostatně a vzdáleně vypnout."),
  bullet("Přítomnost technika Zpracovatele v místě konání po celou dobu akce."),

  h2("Kontrola a doložení"),
  bullet("Evidence případů porušení zabezpečení osobních údajů."),
  bullet("Písemné potvrzení výmazu údajů po ukončení zpracování."),
  bullet("Součinnost při auditu Správce podle článku 4 odst. 7 této smlouvy."),
];

/* ---------- dokument ---------- */

const doc = new Document({
  creator: "XLAB s.r.o.",
  title: "Smlouva o zpracování osobních údajů — MEATING 2026",
  description: "Zpracovatelská smlouva podle čl. 28 GDPR",
  numbering: {
    config: [
      {
        reference: "dash",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "–",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 400, hanging: 220 } },
                     run: { color: GRAY, font: FONT } },
          },
        ],
      },
    ],
  },
  styles: {
    default: {
      document: { run: { font: FONT, size: 20, color: INK } },
    },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 24, bold: true, color: INK } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 21, bold: true, color: GRAY } },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440, header: 720, footer: 720 },
        },
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              border: { top: { style: BorderStyle.SINGLE, size: 4, color: RULE, space: 6 } },
              spacing: { before: 0 },
              children: [
                new TextRun({ text: "Smlouva o zpracování osobních údajů — MEATING 2026", size: 15, color: GRAY2, font: FONT }),
                new TextRun({ text: "\t\t", size: 15, font: FONT }),
                new TextRun({ children: [PageNumber.CURRENT], size: 15, color: GRAY2, font: FONT }),
                new TextRun({ text: " / ", size: 15, color: GRAY2, font: FONT }),
                new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 15, color: GRAY2, font: FONT }),
              ],
            }),
          ],
        }),
      },
      children: [
        ...cover,
        ...strany,
        ...cl1, ...cl2, ...cl3, ...cl4, ...cl5, ...cl6,
        ...cl7, ...cl8, ...cl9, ...cl10, ...cl11, ...cl12,
        ...podpisy,
        ...priloha1, ...priloha2, ...priloha3,
      ],
    },
  ],
});

Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync("/tmp/claude-0/-home-user-XLAB-OFFICE-AUTOMATION/a99ca070-c2a3-531c-a6dc-969708675b21/scratchpad/smlouva/XLAB_MEATING_2026_Smlouva_o_zpracovani_osobnich_udaju.docx", b);
  console.log("ok", b.length);
});
