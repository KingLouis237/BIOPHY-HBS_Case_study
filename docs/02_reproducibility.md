# Reproducibility Playbook

## Toolchain Overview
- **Python:** 3.11.x.
- **Package manager (default):** `uv` for deterministic resolution and lockfiles.
- **Alternative environment:** `conda` or `mamba` when GPU packages or system-wide BLAST+ installs are already managed there.
- **Core libraries:** Biopython 1.86 (Cock et al. 2009), Matplotlib 3.10, NumPy 2.4, EMBOSS-style scoring matrices, BLAST+ 2.14.

## Environment Manifests
- `pyproject.toml` &nbsp;— authoritative dependency list for `uv sync`.
- `uv.lock` &nbsp;— generated locally; not committed because offline builds cannot refresh it.
- `environment/environment.yml` &nbsp;— conda recipe (`name: hemoglobin-e6v`) that also installs BLAST/EMBOSS binaries.
- `requirements-smoke.txt` &nbsp;— minimal pip requirements used by CI for the smoke test.

## Why `uv` First?
| Reason | Detail |
| --- | --- |
| Deterministic lockfile | `uv` stores hashes and indexes so the exact wheels are pinned, simplifying CI. |
| Fast resolution | Built on Rust, so dependency solves remain quick even on clean machines. |
| Easy scripting | `uv run python script.py` encapsulates both the environment and the command. |

## When `conda` (or `mamba`) Is Still Useful
- BLAST+ binaries already live in your system-level conda environment.
- You need compiled packages outside PyPI scope (e.g., GPU builds, MPI stacks).
- Teaching settings where conda is already standard and switching tools would distract from the biology.

## Environment Recipes
```bash
# uv workflow (preferred)
uv sync                        # reads pyproject.toml (and a local uv.lock if present)
uv run python scripts/sequence_summary.py

# conda workflow
conda env create -f environment/environment.yml   # builds the 'hemoglobin-e6v' env
conda activate hemoglobin-e6v
python scripts/sequence_summary.py

# pip fallback (matches CI smoke test)
python -m pip install -r requirements-smoke.txt
python scripts/sequence_summary.py
```

## Dependency Table
| Component | Version | Why it matters |
| --- | --- | --- |
| Python | 3.11.x | Stable typing + pattern matching without breaking Biopython. |
| Biopython | 1.86 | Provides pairwise2, substitution matrices, and PDB parsing (Cock et al. 2009). |
| Matplotlib | 3.10 | Generates deterministic figures across OSes. |
| NumPy | 2.4 | Underpins neighbor searches, vector math. |
| BLAST+ | 2.14 | Required for local BLAST runs; repo ships cached XML for offline use. |

## Cached vs Online Assets
| Asset | Location | Notes |
| --- | --- | --- |
| UniProt FASTA | `data/raw/uniprot/` | Pulled once and versioned; re-download only when UniProt updates are required. |
| Secret FASTA bundle | `data/raw/secret_sequences/` | Provided input, stored verbatim for provenance. |
| BLAST XML | `data/processed/blast/secret_beta_blast.xml` | Generated with BLAST+; cached copy enables offline reproducibility. |
| PDB files | `data/raw/pdb/4HHB.pdb`, `data/raw/pdb/2HBS.pdb` | Downloaded from RCSB; keep for offline structure analysis. |

## Offline vs Online
- **Offline-ready:** sequence summary, pairwise alignments, figure generation, structural contacts, cached BLAST interpretation.
- **Online-required:** refreshing UniProt/PDB downloads, regenerating BLAST XML without the cached file, fetching new BioGRID/IntAct interaction lists.

## Environment Validation Checklist
1. `python --version` shows 3.11.x.
2. `uv --version` (or `conda --version`) prints without errors.
3. `blastp -version` works (otherwise rely on cached XML or install BLAST+ from NCBI).
4. `uv run python scripts/sequence_summary.py` completes and writes `data/processed/sequence_summary.tsv`.

## References
- Cock, P. J. A. et al. 2009. “Biopython: freely available Python tools...” *Bioinformatics* 25(11):1422–1423.
- Cocking, D. et al. 2024. uv documentation. https://github.com/astral-sh/uv
- National Center for Biotechnology Information. BLAST+ user manual.
