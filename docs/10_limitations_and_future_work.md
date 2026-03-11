# Limitations & Future Work

## Honest Limitations
- **Pairwise2 deprecation:** Scripts rely on Biopython’s `pairwise2`, which will be replaced by `Bio.Align.PairwiseAligner`. Migration is planned.
- **Manual interaction note:** BioGRID/IntAct comparisons are still screenshots with citations. Automated API ingestion is pending.
- **BLAST dependency:** Local BLAST+ must be installed for fresh searches; otherwise the repo uses cached XML.
- **No population genetics:** The case study intentionally stops at molecular interpretation; no allele-frequency or clinical penetrance analysis is provided.

## Future Work
1. **Migrate to `Bio.Align.PairwiseAligner`:** eliminate deprecation warnings and enable richer scoring models.
2. **Automated interaction exports:** script BioGRID and IntAct queries so fig02 becomes fully reproducible.
3. **Notebooks for classroom use:** add optional notebooks that walk through dotplot parameter sweeps interactively.
4. **Structural energetics:** integrate simple solvent-accessible surface calculations or MD snapshots for deeper insight.
5. **Extend BLAST coverage:** include non-human beta chains with clear labeling to show evolutionary conservation.

## Educational vs Inferential Boundaries
- **Educational:** BRCA1<->53BP1 calibration, interaction note, dotplot parameter sweeps.
- **Inferential:** QC metrics, alignments, substitution scoring, BLAST confirmation, structural contacts.

