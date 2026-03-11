# Runbook

Each command assumes you are at the repo root. Use `uv run ...` unless `conda` is explicitly required.

| Step | Command | What it does | Why it matters | Expected outputs | Inspect |
| --- | --- | --- | --- | --- | --- |
| 0 | `uv sync` or `conda env create -f environment/environment.yml` | Creates the Python environment with pinned dependencies. | Ensures all scripts run with consistent versions. | `.venv/` (uv) or `hbb-e6v` conda env. | `uv pip list` or `conda list`. |
| 1 | `uv run python scripts/sequence_summary.py` | Parses FASTA files, computes QC metrics. | Confirms basic sanity before alignment. | `data/processed/sequence_summary.tsv`, `reports/sequence_summary.md`. | Check lengths/hydrophobicity for expected values. |
| 2 | `uv run python scripts/run_alignments.py --gap-open 10 --gap-extend 0.5` | Runs BRCA1 calibration and hemoglobin alignments. | Quantifies identity and mismatch positions. | `data/processed/alignment_summary.tsv`, textual alignments. | Verify beta mismatch at residue 6. |
| 3 | `uv run python scripts/make_figures.py` | Generates QC figure + BLOSUM penalty figure. | Visualizes metrics for presentations. | `figures/fig01_sequence_characteristics.png`, `figures/fig06_blosum_penalty.png`. | Open PNGs to ensure labels render. |
| 4 | `uv run python scripts/make_dotplots.py` | Creates calibration and hemoglobin dotplots. | Builds intuition for scoring parameters. | `figures/fig03_dotplots_brca1_53bp1.png`, `figures/fig04a/b`. | Check diagonals and noise levels. |
| 5 | `uv run python scripts/make_alignment_figure.py` | Produces chunked alignment with mismatch annotation. | Makes the E6V substitution obvious. | `figures/fig05_beta_variant_alignment.png`. | Ensure only residue 6 is highlighted. |
| 6 | `uv run python scripts/analyze_structure.py --radius 5.0` | Counts residue contacts around beta6. | Quantifies chemical environment differences. | `data/processed/structure_contacts.csv`, `reports/structure_summary.md`. | Compare hydrophobic counts between 4HHB and 2HBS. |
| 7 | `uv run python scripts/make_structure_figure.py` | Renders 3D scatter of contact clouds. | Visual aid for presentations and discussions. | `figures/fig08_structure_comparison.png`. | Check legend and axes. |
| 8 | `uv run python scripts/run_blastp.py` | Prepares BLAST query, runs BLAST+ or cached fallback. | Confirms homology to known HBB variants. | `data/processed/blast/secret_beta_query.fasta`, `data/processed/blast/secret_beta_blast.xml`, `reports/blast_summary.md`. | If offline, confirm log message says cached XML was used. |
| 9 | `uv run python scripts/make_blast_figure.py` | Visualizes BLAST hit identities vs e-values. | Communicates homology strength quickly. | `figures/fig07_blast_hits.png`. | Ensure HbS appears with 100% identity. |

## After Running Everything
- Commit regenerated TSV/CSV/PNG/MD files if they changed.
- Update `docs/09_results_and_discussion.md` with any new interpretations.
- If BLAST was re-run online, refresh the cached XML so CI stays deterministic.
