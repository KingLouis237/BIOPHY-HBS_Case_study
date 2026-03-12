# File Naming & Organization Guide

## Archive Layer (read-only provenance)
- `docs/archive/ComputationalBio_Directives.pdf` — verbatim practicum brief provided by the university.
- `docs/archive/ComputationalBio_solutions.pdf` — original January 2026 submission (appendix includes BioGRID/IntAct screenshots).
- `docs/archive/ComputationalBio_secret_sequences_original.fasta` — untouched FASTA bundle exactly as distributed in the source assignment.
- Naming pattern: `ComputationalBio_<layer>.pdf` (or `.fasta`) to keep provenance explicit without resurrecting course codes.

## Portfolio Layer (public-facing derivatives)
- `docs/project_brief.{md,pdf}` — recruiter-facing overview derived from the archive materials (PDF exported from the Markdown).
- `reports/workflow_report.md` — living tracker of automation status and remaining work.
- `reports/analysis_summary.md` (future) — recommended target name for aggregated QC/interpretation summaries.
- `reports/blast_protocol.md`, `reports/blast_summary.md`, `reports/structure_summary.md`, etc. — descriptive names tied to the corresponding scripts.

## Data & Outputs
- `data/raw/secret_sequences/hemoglobin_secret_sequences.fasta` — provided FASTA (copied exactly from the archive).
- `data/raw/uniprot/<accession>.fasta` — canonical sequences fetched from UniProt.
- `data/raw/pdb/{4HHB,2HBS}.pdb` — downloaded structures used by `scripts/analyze_structure.py`.
- `data/processed/sequence_summary.tsv`, `data/processed/alignment_summary.tsv`, `data/processed/structure_contacts.csv` — TSV/CSV outputs aligned with their generating scripts.
- `data/processed/blast/*` — BLAST query/response artifacts (paired with cached XML when offline).

## Figures
- `figures/figNN_description.png` — deterministic outputs from `scripts/make_*` helpers.
- Inventory tracked in `figures/README.md`, including caption, status, and script/notebook provenance.

## Naming Principles
1. **Provenance first:** anything that originated from coursework lives under `docs/archive/` with the original identifier intact.
2. **Role clarity:** public-facing documents use descriptive names (`project_brief`, `workflow_report`, `analysis_summary`) instead of course codes.
3. **1:1 mapping:** every generated file references the script or notebook responsible for it, easing reproducibility checks.
