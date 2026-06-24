---
name: xlab-tenders
description: Analyze tender/RFP/RFQ/RFI documentation and produce structured go/no-go assessment, action plans, and submission checklists for XLAB. Trigger when the user uploads or references zadávací dokumentace, výzva k podání nabídky, výběrové řízení, tender, RFP, RFQ, RFI, poptávka s formálními požadavky, veřejná zakázka, or any procurement document requiring a structured response. Also trigger when user asks to compare tenders, prepare qualification documents, or automate parts of a tender submission. Works alongside xlab-events (creative proposals) and xlab-pricing (kalkulace) but focuses on the administrative, qualification, and strategic layer of procurement response.
---

# XLAB Tenders Skill

Systematic analysis and response preparation for tenders, RFPs, RFQs, RFIs, and formal procurement processes — from initial document intake through go/no-go decision to submission-ready deliverables.

## When to Use

Trigger this skill when:
- User uploads or references tender/RFP/RFQ/RFI documentation
- User mentions výběrové řízení, zadávací dokumentace, veřejná zakázka, nabídka do tenderu
- User wants to analyze qualification requirements or evaluate whether to bid
- User needs a structured action plan for tender response preparation
- User asks to fill in or prepare qualification documents (čestná prohlášení, reference lists, pricing templates)
- User wants to compare multiple tender opportunities

Do NOT trigger for:
- Creative event proposals where no formal procurement structure exists → use xlab-events
- Simple pricing requests → use xlab-pricing
- Internal project briefs without formal submission requirements

## Skill Dependencies

This skill works UPSTREAM of:
- **xlab-events** → creative concept and proposal content (triggered after go/no-go passes)
- **xlab-pricing** → pricing/kalkulace (triggered when pricing template is identified)
- **xlab-proposal** → PPTX output for presentation deliverables

This skill works INDEPENDENTLY for:
- Document analysis and classification
- Go/no-go assessment
- Action plan generation
- Qualification document preparation
- Submission checklist and compliance tracking

## Core Workflow

```
DOCUMENTS IN → CLASSIFY → EXTRACT → GO/NO-GO → ACTION PLAN → PREPARE → CHECK → SUBMIT
     Phase 1        Phase 2    Phase 3      Phase 4       Phase 5    Phase 6   Phase 7
```

---

## Phase 1: Document Classification

When tender documents arrive, first classify every file. Tender packages vary enormously in structure, but documents almost always fall into one of these categories:

### Universal Document Taxonomy

| Category | What it contains | Typical filenames / labels |
|----------|-----------------|---------------------------|
| **A. Cover / Invitation** | Who's asking, what for, deadline, where to submit | Výzva, Standardanschreiben, Cover letter, Inquiry |
| **B. Main specification** | Scope of work, requirements, evaluation criteria, rules | Zadávací dokumentace, RFP brief, Tender document, Scope of Work |
| **C. Pricing template** | Pre-formatted Excel/form where prices go | Cenová nabídka, Pricelist, Event Pricing, Struktura nabídkové ceny |
| **D. Qualification docs** | Forms to prove eligibility (declarations, references) | Čestné prohlášení, Kvalifikační dokumentace, Krycí list |
| **E. Contract draft** | Pre-drafted contract the winner will sign | Rámcová smlouva, Smlouva o realizaci, Framework agreement |
| **F. Compliance / Ethics** | Supplier codes, sanctions declarations, GDPR | Etický kodex, Supplier Code of Conduct, Sankce, GDPR |
| **G. Technical annexes** | Brand manuals, site plans, technical specs, logomanuály | CI guidelines, Logomanual, Situace, Technical rider |
| **H. Evaluation forms** | Scoring sheets, reference templates, assessment criteria | Podklad pro hodnocení, Hodnotící kritéria |

**Action:** List all received documents with their classification letter. Flag any missing categories that would normally be expected.

### Tender Type Detection

Classify the overall tender type, as it determines the response strategy:

| Type | Description | Key signals | Response complexity |
|------|------------|-------------|-------------------|
| **VZMR** | Veřejná zakázka malého rozsahu | §31 ZZVZ, Tender arena, profil zadavatele | High formality, moderate scope |
| **Corporate RFP** | Private-sector formal procurement | VW Group Supply, SAP Ariba, evaluation scoring | Variable formality, often presentation-heavy |
| **Corporate RFQ** | Price-focused request for quotation | Pre-set pricing template, minimal creative scope | Low formality, pricing-focused |
| **RFI** | Information gathering (pre-qualification) | "Request for Information", shortlisting, no pricing yet | Low-medium, self-presentation focused |
| **Direct inquiry** | Informal but structured request | Email with brief + pricing ask, no formal docs | Lowest formality |
| **Framework tender** | Long-term rámcová dohoda / pool selection | Multi-year, multiple suppliers selected, VZMR or above-threshold | Highest complexity, qualification-heavy |

---

## Phase 2: Structured Extraction

For each document, extract a standardized data set. The extraction must be EXHAUSTIVE — missing a single requirement can mean disqualification.

### 2.1 Header Card (always produce first)

```
TENDER:          [name]
CLIENT:          [organization + department]
CONTACT:         [name, email, phone — for technical and procurement separately]
TYPE:            [VZMR / Corporate RFP / RFQ / RFI / Direct / Framework]
SUBMISSION:      [deadline — date + time + timezone]
FORMAT:          [electronic platform / email / physical]
PLATFORM:        [Tender arena / VW Group Supply / email / other]
LANGUAGE:        [CZ / EN / DE / bilingual]
CURRENCY:        [CZK / EUR]
EST. VALUE:      [stated or implied budget]
DURATION:        [contract period]
LOT STRUCTURE:   [single lot / multiple lots — if multiple, list them]
```

### 2.2 Qualification Requirements (CRITICAL — binary gate)

Extract ALL qualification requirements. These are pass/fail — missing one means automatic exclusion.

**Standard qualification layers (check each):**

1. **Základní způsobilost** — criminal record, tax compliance, no insolvency
   - Usually: čestné prohlášení (sworn statement)
   - Sometimes: actual extracts from registries required

2. **Profesní způsobilost** — business registration, trade license
   - Usually: výpis z OR or živnostenský list
   - Check: does the required scope match XLAB's registration?

3. **Ekonomická kvalifikace** — revenue thresholds, insurance
   - CHECK HARD NUMBERS: annual revenue minimums, consecutive years
   - This is the most common blocker for smaller agencies

4. **Technická kvalifikace** — reference projects, team CVs
   - Reference count and minimum parameters (value, attendee count, sector)
   - Team composition requirements (named roles, years of experience)
   - Certifications (Tissax, ISO, security clearances)

5. **Compliance** — ethics codes, sanctions declarations, NDA
   - Usually sign-and-return documents
   - Check for specific certifications (Tissax for automotive)

**Output format:**
```
QUALIFICATION CHECK:
├── Základní způsobilost:     [YES/NO] — [what's needed]
├── Profesní způsobilost:     [YES/NO] — [what's needed]
├── Ekonomická kvalifikace:   [YES/VERIFY/NO] — [threshold + XLAB status]
├── Technická kvalifikace:    [YES/PARTIAL/NO] — [requirements vs. XLAB capability]
├── Compliance:               [YES/NO] — [what to sign/provide]
└── OVERALL GO/NO-GO:         [GO / CONDITIONAL / NO-GO]
```

**If any item is NO or VERIFY → flag immediately as blocker. Do not proceed to creative work until blockers are resolved.**

### 2.3 Evaluation Criteria (where the points are)

Extract the COMPLETE scoring model with weights:

```
EVALUATION MODEL:
├── Criterion 1: [name] — [weight %] — [scoring method]
├── Criterion 2: [name] — [weight %] — [scoring method]
├── Criterion 3: [name] — [weight %] — [scoring method]
└── TOTAL: 100%

HIGHEST-LEVERAGE AREAS:
1. [criterion with highest weight] — [what maximizes score]
2. [criterion with second highest weight] — [what maximizes score]
```

**Common scoring patterns observed across tenders:**
- Price: 40-60% (lowest price gets max points, others proportional)
- Quality/creative: 30-50% (subjective committee scoring)
- References/experience: 10-40% (count-based or committee-assessed)
- Flexibility/speed: 5-20% (measured in response days)

### 2.4 Deliverables Checklist

List EVERY document/item that must be submitted. Mark each with status:

```
SUBMISSION CHECKLIST:
☐ [Document 1] — [format] — [who prepares] — [status]
☐ [Document 2] — [format] — [who prepares] — [status]
...
⚠️ Missing [X] will result in disqualification!
```

---

## Phase 3: Go/No-Go Assessment

Present a structured decision framework to the user. The go/no-go is NOT Claude's decision — it's a recommendation with clear reasoning.

### Decision Matrix

| Factor | Assessment | Impact |
|--------|-----------|--------|
| Qualification fit | Can we pass all gates? | Binary — if NO, stop |
| Revenue threshold | Do we meet the minimum? | Binary — if NO, stop or find consortium partner |
| Reference match | Do we have matching references? | Score 1-5 |
| Creative opportunity | Is there room to differentiate? | Score 1-5 |
| Pricing competitiveness | Can we win on price? | Score 1-5 |
| Strategic value | Does this client matter long-term? | Score 1-5 |
| Resource availability | Can we staff this in the timeline? | Score 1-5 |
| Competition | Who else is likely bidding? | Assessment |
| Effort/reward ratio | Work to prepare vs. contract value | Assessment |

### Recommendation Format

```
RECOMMENDATION: [GO / CONDITIONAL GO / NO-GO]
CONFIDENCE: [HIGH / MEDIUM / LOW]
KEY RISK: [single biggest risk factor]
CONDITION: [if conditional, what must be resolved]
```

---

## Phase 4: Action Plan Generation

Once GO is confirmed, produce a role-assigned, prioritized action plan.

### Priority Framework

| Priority | Color | Meaning |
|----------|-------|---------|
| P0 — BLOCKER | 🔴 | Must resolve before anything else (qualification gates) |
| P1 — CRITICAL | 🟠 | Direct impact on scoring, disqualification risk if missing |
| P2 — IMPORTANT | 🟡 | Required for submission but straightforward |
| P3 — NICE-TO-HAVE | 🟢 | Enhances bid quality but not mandatory |

### Standard Role Assignments

| Role | Typical responsibilities |
|------|------------------------|
| **Management / BD** | Go/no-go decision, strategic positioning, final review |
| **Finance** | Revenue verification, pricing strategy, cost calculations |
| **Legal** | Contract review, compliance docs, čestná prohlášení |
| **Creative** | Concept, presentation, visual materials |
| **Project Management** | Reference list compilation, team CVs, timeline |
| **Administration** | Document formatting, platform registration, submission |

### Action Plan Template

For each document identified in Phase 2:

```
DOCUMENT: [name]
PRIORITY: [P0-P3]
OWNER: [role]
ACTION: [specific step-by-step instructions]
DEADLINE: [internal deadline, before submission date]
DEPENDENCIES: [what must be done first]
TEMPLATE: [if a template/form exists, reference it]
AUTOMATION: [what Claude can help with — see Phase 5]
```

---

## Phase 5: Preparation Assistance

### What Claude CAN automate or significantly accelerate:

1. **Čestné prohlášení / Sworn declarations**
   - Fill in company data into provided templates (DOCX)
   - Generate declarations from scratch when no template provided
   - Adapt standard text to specific tender requirements

2. **Reference lists / Seznam významných zakázek**
   - Read `references/xlab-reference-events.xlsx` (Sheet "Zakazky") via openpyxl
   - Columns: Poř.Č., Předmět plnění, Místo, Poskytovatel, Období, Objednatel (firma+osoba+tel), Finanční objem, Poznámka, Bod 6.2.1., Bod 6.2.2.
   - Match references to specific qualification criteria (filter by value, sector, date)
   - Structure into required format per tender template
   - Generate reference descriptions that emphasize relevant parameters

3. **Team composition / Seznam realizačního týmu**
   - Read `references/xlab-project-team.xlsx` (Sheet "Sheet1") via openpyxl
   - Columns: Pozice, Osoba, Praxe
   - Match team members to required roles in tender
   - Structure team member information into required format
   - Highlight relevant experience per tender requirements

4. **Pricing template analysis**
   - Read and explain pricing template structure
   - Calculate totals and cross-check formulas
   - Suggest pricing strategy based on evaluation criteria weights
   - Delegate to xlab-pricing for actual kalkulace

5. **Krycí list / Cover sheet**
   - Fill in identification data
   - Calculate price summaries

6. **Contract review highlights**
   - Flag unusual or risky clauses in draft contracts
   - Highlight areas that need legal attention
   - Note payment terms, liability, cancellation conditions

7. **Presentation structure**
   - Outline proposal presentation based on evaluation criteria
   - Delegate to xlab-events for creative content
   - Delegate to xlab-proposal for PPTX generation

8. **Compliance document processing**
   - Identify which ethics codes/declarations need signing
   - Summarize key obligations from supplier codes
   - Flag any commitments that need internal discussion

### What Claude CANNOT do (human required):

- Sign documents or make legally binding commitments
- Verify actual financial figures (revenue, insurance)
- Make final go/no-go decisions
- Contact clients for clarification
- Upload to submission platforms
- Provide legal advice on contract terms

---

## Phase 6: Submission Compliance Check

Before submission, run a final compliance check:

```
FINAL COMPLIANCE CHECK:
━━━━━━━━━━━━━━━━━━━━━━━━━
☐ All required documents present
☐ All forms signed (or marked for signature)
☐ Pricing template complete — all cells filled, formulas correct
☐ Language requirement met (CZ/EN/both)
☐ File format requirements met (PDF/DOCX/XLSX)
☐ File size limits respected
☐ Platform registration complete (if electronic submission)
☐ Submission deadline confirmed (date + time + timezone)
☐ Internal review completed
☐ Backup submission plan (if platform issues)
━━━━━━━━━━━━━━━━━━━━━━━━━
READY TO SUBMIT: [YES / NO — with list of open items]
```

---

## Tender Pattern Library

### Patterns observed across Czech/Central European tenders:

**Public sector (VZMR and above):**
- Always references §134/2016 Sb. (ZZVZ)
- Qualification via čestná prohlášení (can be verified post-selection)
- Electronic submission via certified platforms (Tender arena, E-ZAK, NEN)
- Strict format requirements — often Word with tracked changes for contracts
- Revenue/reference thresholds are hard blockers
- Price weight typically 40-60%

**Automotive (Škoda / VW Group):**
- Submission via VW Group Supply / SAP-based platform
- Confidentiality strict — NDA + Tissax certification often required
- Pricing in EUR, structured as day-rates × days per phase
- Team structure and org chart mandatory
- Previous automotive experience heavily weighted
- Cancellation terms favor the client

**Pharma (Roche):**
- Supplier Code of Conduct acknowledgment mandatory
- PSCI compliance expected
- Confidentiality obligations extensive
- Payment terms typically 60 days
- RfP validity period 90 days standard

**Energy / Utilities (ČEZ, E.ON):**
- Framework agreements (rámcové dohody) common — multi-year
- Revenue thresholds can be very high (50M+ CZK/year)
- Social enterprise participation sometimes required
- Sanctions declarations (Russia/Belarus) now standard
- RFI → RFP → Selection is typical multi-stage process

**Media / Public institutions (ČT, PDS):**
- VZMR regime but with detailed scoring
- Quality/creative evaluation alongside price (40% quality common)
- Visualization/design proposals required
- Reference projects with client confirmation letters
- Register smluv publication required for contracts above threshold

---

## Output Formats

Claude should adapt output format to what the user needs:

| User request | Output format |
|-------------|--------------|
| "Analyzuj tenhle tender" | Structured analysis in chat (Header Card → Qualification → Evaluation → Deliverables) |
| "Udělej akční plán" | Formatted DOCX with role assignments and priorities |
| "Vyplň čestné prohlášení" | Filled DOCX template |
| "Připrav reference list" | Filled Excel or structured text matching required format |
| "Porovnej tyto dva tendery" | Side-by-side comparison table |
| "Řekni mi jestli do toho jít" | Go/No-Go assessment with decision matrix |

**For DOCX outputs:** Use the `docx` skill for professional formatting.
**For XLSX outputs:** Use the `xlsx` skill for spreadsheet work.

---

## References & Templates

This skill uses a `references/` directory with pre-built templates and data sources.

**Read `references/README.md` first** when preparing any qualification documents.

| File | Read when... |
|------|-------------|
| `references/README.md` | Starting any document preparation work |
| `references/company-data.md` | Filling in ANY form or template with XLAB data |
| `references/xlab-reference-events.xlsx` | Selecting references for technical qualification (Excel — read via openpyxl) |
| `references/xlab-project-team.xlsx` | Selecting team members for qualification (Excel — read via openpyxl) |
| `references/templates/cestne-prohlaseni.md` | Preparing sworn declarations |
| `references/templates/kryci-list.md` | Preparing cover sheets |
| `references/templates/seznam-referenci.md` | Preparing reference lists |
| `references/templates/seznam-tymu.md` | Preparing team lists |
| `references/templates/sankce-prohlaseni.md` | Preparing sanctions declarations |
| `references/patterns/fill-logic.md` | Understanding how to fill templates (decision tree, placeholder mapping) |

**Key rule:** If the tender provides its own template → ALWAYS use that, not ours. Our templates are fallback only.

---

## Language

- Analysis and action plans: match user's language (typically informal Czech)
- Filled-in documents: match the language required by the tender
- When user speaks informal Czech, respond in kind — avoid formal or corporate tone in discussion
- Document outputs should be professional and formal

---

## Important Rules

1. **Never skip qualification analysis.** It's the single most common reason for wasted effort.
2. **Always extract deadlines first.** Everything else is contingent on time.
3. **Flag blockers immediately.** Don't bury a revenue shortfall in paragraph 15.
4. **Be specific about what's missing.** "Some documents may be needed" is useless. "Příloha č. 3 — Čestné prohlášení — template not found in uploads" is useful.
5. **Pricing strategy follows evaluation weights.** If price is 40%, don't optimize for lowest price at the expense of quality criteria worth 60%.
6. **Track document versions.** Tenders get amended. Note version numbers and dates.
7. **Respect confidentiality markings.** Many tender documents are marked INTERNAL or CONFIDENTIAL.
8. **When in doubt about a requirement, flag it as a question for the client** rather than assuming.
