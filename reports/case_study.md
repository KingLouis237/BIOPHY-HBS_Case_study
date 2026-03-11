# Case Study Summary: Hemoglobin beta E6V

## Biological Framing
- Unknown beta-globin sequence suspected to be the sickle-cell variant.
- Evidence stack: curated canonical sequences (P69905/P68871), provided "secret" FASTA bundle, BLAST/EMBOSS tooling, and 4HHB/2HBS structures.

## Workflow Recap
1. **QC & retrieval:** `scripts/sequence_summary.py` logs length, hydrophobic content, and charge across canonical and secret sequences.
2. **Calibration:** BRCA1<->53BP1 dotplots/alignment runs demonstrate gap penalty behavior before applying the final parameters to hemoglobin.
3. **Variant localization:** `scripts/run_alignments.py` confirms 100% identity for alpha, 99.32% with a single E6V mismatch for beta.
4. **Substitution scoring:** `scripts/make_figures.py` visualizes the BLOSUM62 cost of E->V alongside the canonical self-match.
5. **Homology confirmation:** `scripts/run_blastp.py` (with offline cache) plus `scripts/make_blast_figure.py` document the top hits (HbS, Hb Monza, Hb delta).
6. **Structure context:** `scripts/analyze_structure.py` and `scripts/make_structure_figure.py` map the beta6 contact cloud difference between 4HHB and 2HBS.
7. **Interaction caution:** manual BioGRID/IntAct comparison documented as a supporting database-interpretation note (see Provenance Note).

## Highlights
- Hemoglobin beta chains differ at residue 6 only; the secret chain matches the sickle-cell variant.
- BLOSUM62 penalty (-2) plus hydrophobic chemistry explains the functional impact of E->V.
- Structure panel shows Val6 introducing a hydrophobic patch consistent with polymerization propensity.

## Provenance Note
Source materials (briefing + early report) are archived verbatim under `docs/archive/`. This summary reflects the reproducible case-study implementation tracked in `reports/workflow_report.md`.
