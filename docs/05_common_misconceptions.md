# Common Misconceptions

| Misconception | Reality | How to check |
| --- | --- | --- |
| “The secret beta chain is completely different.” | It differs by exactly one residue at position 6. | Inspect `reports/alignment_summary.md` or `figures/fig05_beta_variant_alignment.png`. |
| “Gap penalties don’t matter for globins.” | Incorrect penalties can fabricate insertions, masking the true point mutation. | Re-run `scripts/run_alignments.py` with low gap penalties and compare the chaos. |
| “BLAST always needs the internet.” | Local BLAST+ works offline, and the repo ships a cached XML for reproducibility. | Use `uv run python scripts/run_blastp.py --offline`. |
| “The structural change is obvious without counting contacts.” | Visual intuition varies; the contact table quantifies hydrophobic vs polar neighbors. | Read `reports/structure_summary.md` and compare counts between 4HHB and 2HBS. |
| “Interaction networks are core evidence.” | They support database literacy but are not directly part of the E6V proof. | See Supporting Notes & Provenance and the `fig02` status entry. |
