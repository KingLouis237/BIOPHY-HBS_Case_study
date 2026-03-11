# Debugging Guide

## General Strategy
1. Re-run the previous step to ensure inputs exist.
2. Check `data/processed/` timestamps to confirm the script actually wrote outputs.
3. Use `uv run python -m pdb script.py` if a script fails—most files are short and pdb-friendly.

## Common Issues
| Symptom | Root cause | Fix |
| --- | --- | --- |
| `FileNotFoundError` for FASTA | Wrong working directory or missing `data/raw/...` files. | Run commands from repo root; ensure git submodules (if any) are pulled. |
| `KeyError: ('X', 'Y')` in dotplots | Non-standard amino acid encountered. | Update substitution matrix or sanitize FASTA before dotplotting. |
| BLAST command not found | BLAST+ not installed or PATH not set. | Install BLAST+ (NCBI) or use `--offline` to consume cached XML. |
| Figures look empty | Word/threshold settings too strict. | Lower the threshold or reduce the word size; re-run `scripts/make_dotplots.py`. |
| `Bio.pairwise2` deprecation warning | Upstream Biopython warning. | Note it in issues; plan to migrate to `Bio.Align.PairwiseAligner`. |

## Logging Tips
- Most scripts print a short success message with the output path. If you do not see it, assume the script exited early.
- Redirect stdout to a log during CI runs: `uv run python scripts/run_alignments.py > logs/alignments.log`.

## Validation Checks
- **Checksum outputs** if you worry about corruption: `shasum data/processed/sequence_summary.tsv`.
- **Visual spot-checks**: open PNGs to ensure fonts render—matplotlib sometimes falls back to system fonts.
- **Compare TSVs**: `git diff data/processed/alignment_summary.tsv` to ensure changes are intentional.
