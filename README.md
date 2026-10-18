# Shoulder Complex — Master Clinical Dossier & Companion Test Atlas

**Live Atlas:** https://azhry-x.github.io/shoulder-atlas/  
**Dossier PDF:** [`master_shoulder_dossier.pdf`](./master_shoulder_dossier.pdf) — 9 pages, A4 portrait, built for Apple Pencil in Notability / GoodNotes.

Sister projects:
- [Knee Complex dossier + atlas](https://github.com/Azhry-X/knee-atlas) — same design system, same page architecture.
- [Ankle & Foot dossier + atlas](https://github.com/Azhry-X/ankle-atlas) — same design system, same page architecture.
- [Lumbar Spine dossier + atlas](https://github.com/Azhry-X/lumbar-atlas) — same design system, same page architecture.

## What is in the dossier
| Page | Content | Accent |
|---|---|---|
| 1 | Triage, red flags (BESS/BOA quotes, septic arthritis synovial WBC, posterior dislocation, traumatic anterior dislocation associated injuries & EMG at 6 weeks, Pancoast, PMR EULAR/ACR 2012, cardiac/visceral referral, cervical radiculopathy Wainner cluster & ULTT A), pathway router, subjective, pain map | red |
| 2 | Differential matrix (RCRSP/subacromial pain, full-thickness tear, frozen shoulder, GH OA, traumatic instability, atraumatic Stanmore II/III, AC joint, SLAP/biceps, calcific tendinopathy, cervical/TOS), Kelley frozen shoulder prevalence/stages/definition, Cadogan full passive ER rule & subacromial cluster, Hanchard Cochrane caution, Brownson recurrence | blue |
| 3 | ROM table (write-in, active/passive, ER at 0° and 90°, IR, total arc; Kolber goniometer vs inclinometer note), scapular dyskinesis test (McClure & Singh), scapular assistance & retraction tests, SSMP, strength/HHD write-in, CKCUEST (Tucci), YBT-UQ, C5–T1 neurological grid | blue |
| 4 | Special tests & clusters: impingement/RCRSP (Neer, Hawkins-Kennedy, painful arc, empty can, ER resistance, Michener ≥ 3/5 cluster, Park clusters), cuff tear (drop-arm, ER lag sign, IR lag sign, Hornblower, Murrell cluster), subscapularis (bear-hug, belly-press, Napoleon, lift-off), instability (apprehension, relocation, surprise, load-and-shift, sulcus), AC (cross-body, O'Brien, Paxinos, AC tenderness), SLAP/biceps (biceps load II, Speed, Yergason, compression-rotation), PROM dashboard (SPADI, QuickDASH, DASH, ASES, Constant, Oxford, WOSI, NPRS, PSFS) | blue |
| 5 | Post-op: surgeon-directed restrictions, cuff repair early vs delayed PROM (Kluczynski), pre-op injection infection risk (Forsythe), Bankart vs Latarjet (Hossein Zadeh) & Bankart RTS (Memon), subacromial decompression trials (CSAW, FIMPACT, Ketola 12-year), frozen shoulder surgical trials (UK FROST, Kivimäki), Kanto MID/PASS, wound/neuro/infection re-check, operative log | purple |
| 6 | Electrophysical agents & injections: ESWT (Bannuru, Surace Cochrane, BESS quote), barbotage RCT (Moosmayer 2023), electrotherapy Cochrane (Page 2016), corticosteroid injections (Mohamadi, Challoumas NMA, Carette, Kelley CPG quote), hydrodilatation (Buchbinder Cochrane), Lafrance 2022 CPG quotes, parameter log | orange |
| 7 | Manual therapy: Page Cochranes (cuff 2016, frozen 2014), Desjardins-Charbonneau MA, Vermeulen HGMT vs LGMT, Diercks supervised neglect, thoracic SMT (Kardouni sham = real, Peek SR), Mintken CPR (unvalidated), dry needling (Navarro-Santana), kinesio taping (Celik), cross-body vs sleeper stretch (McClure 2007), safety screen & consent box | teal |
| 8 | Exercise & RTS: GRASP (Hopewell), Holmgren specific exercise, SELF (Littlewood), Ingwersen load RCT, Smith painful vs pain-free MA, Saito scapular-focused MA, non-traumatic cuff tears (Kukkonen) & 10-year small/medium tears (Moosmayer 2019), MDI Watson vs Rockwood (Warby), throwers GIRD/TRM/ER (Wilk 2011, 2015), frozen shoulder education (Kelley), 12-week loading log | green |
| 9 | 12-visit flowsheet, discharge milestones (SPADI / QuickDASH / ASES / Oxford / NPRS / PSFS change vs verified MCIDs), discharge summary | slate |

Every statistic carries an evidence marker: **H** high · **M** moderate · **L** low · **E** expert opinion.
Underlined test names open the matching Atlas card; **▸** marks cards with a verified video.

## Repository layout
```
index.html                    Atlas (GitHub Pages entry point) — generated
master_shoulder_dossier.html  Dossier (generated, self-contained CSS)
master_shoulder_dossier.pdf   Dossier PDF (generated)
src/pages/p1.html … p9.html   Dossier page bodies  ← edit content here
src/dossier.css               Design system
atlas/data/tests.yaml         Atlas cards: steps, criteria, accuracy, evidence, videos, calculators  ← single source of truth
atlas/build_atlas.py          Builds index.html from tests.yaml (page badges/filters = every dossier page that links the card)
atlas/config.py               Atlas base URL
tools/build_dossier.py        Assembles HTML → PDF → runs every check
tools/render_and_check.py     Page count, overflow, overlap, fonts, required safety strings, previews
tools/check_links.py          Verifies every PDF link, Atlas anchor, card source (DOIs via the DOI registry) and video
tools/required_strings.txt    Safety-critical text that must never disappear
fonts/                        Source Sans 3 (OFL)
```

## Rebuild after an edit
One-time setup (Python 3.10+ and Node.js):
```bash
pip install -r requirements.txt
python -m playwright install chromium
npm install
```
Windows, one command (stops at the first failure):
```powershell
powershell -ExecutionPolicy Bypass -File build.ps1            # Atlas + PDF + all checks + link audit
powershell -ExecutionPolicy Bypass -File build.ps1 -SkipLinks # same, without the network link audit
```
Or step by step on any OS:
```bash
python atlas/build_atlas.py                # Atlas
python tools/build_dossier.py              # Dossier PDF + all checks (exit 1 on any problem)
python tools/check_links.py                # links (add --live after the site is published)
```
The dossier build fails on: page count ≠ 9, content overflowing a page / card / cell, overlapping glyphs,
a character missing from Source Sans 3 (font fallback), malformed tables, leaked markup, internal link targets
under 4 mm, or a missing safety string from `tools/required_strings.txt`.
Page previews are written to `preview/` when poppler (`pdftoppm`) or `pip install pypdfium2 pillow` is available.
Authoring shortcuts in `src/pages/*.html` (expanded at build time):
`<a class="test-link" data-atlas="neer-test">Neer</a>` · `<a class="info-icon" data-atlas="bess-boa-red-flags"></a>` ·
`<a class="calc-badge" data-atlas="spadi">Calc</a>` · `<a class="guide-badge" href="https://…">BESS/BOA</a>`.
An unknown `data-atlas` id stops the build.

## Status
Draft cards under clinical review with open-access citations and video demonstrations.
