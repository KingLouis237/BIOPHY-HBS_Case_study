# Common Misconceptions

| Misconception | Reality | How to check |
| --- | --- | --- |
| "The secret beta chain is completely different." | It differs by exactly one residue at position 6. | Inspect `reports/alignment_summary.md` or `figures/fig05_beta_variant_alignment.png`. |
| "High BLAST identity means no phenotype." | HbS and canonical HBB differ by <1% yet have opposite clinical outcomes; BLAST measures family membership, not pathogenic impact. | Compare BLAST hits in `figures/fig07_blast_hits.png` with the structural discussion in `docs/08_biological_interpretation.md`. |
| "A negative BLOSUM score proves pathogenicity." | BLOSUM is an evolutionary log-odds matrix. Negative scores flag rarity, not disease. | Read the BLOSUM section in `docs/08_biological_interpretation.md` and the original matrix paper (Henikoff & Henikoff 1992). |
| "Dotplots are final evidence." | They are exploratory visuals for spotting mismatches; quantitative proofs come from alignments and score tables. | Run `scripts/make_dotplots.py` with different thresholds and observe how noise changes. |
| "Gap penalties don't matter for globins." | Incorrect penalties can fabricate insertions, hiding the true point mutation. | Re-run `scripts/run_alignments.py` with very low penalties and compare the chaos. |
| "BLAST always needs the internet." | Local BLAST+ works offline, and the repo ships a cached XML for reproducibility. | Use `uv run python scripts/run_blastp.py --offline`. |
| "The structural change is obvious without counting contacts." | Visual intuition varies; the contact table quantifies hydrophobic vs polar neighbors. | Read `reports/structure_summary.md` and compare counts between 4HHB and 2HBS. |
| "Interaction networks are core evidence." | They support database literacy but are not directly part of the E6V proof. | See Supporting Notes & Provenance and the `fig02` status entry. |
