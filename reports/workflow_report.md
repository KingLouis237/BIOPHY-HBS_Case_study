# Workflow Report: Hemoglobin beta E6V Variant

## Objective
Document a reproducible case study that links the hemoglobin beta6 Glu->Val substitution from sequence-level evidence to structural interpretation.

## Scientific Workflow (Extracted)
1. **Sequence retrieval:** `scripts/sequence_summary.py` parses UniProt (P69905/P68871) plus secret FASTA sequences and stores QC metrics.
2. **Algorithm calibration:** BRCA1 vs 53BP1 dotplots/global alignments document how parameter sweeps behave on a difficult, low-identity pair before trusting hemoglobin results.
3. **Variant localization:** `scripts/run_alignments.py` compares canonical vs secret alpha/beta chains and BRCA1 vs 53BP1.
4. **Substitution scoring:** `scripts/make_figures.py` visualizes BLOSUM62 penalties; `data/processed/alignment_summary.tsv` records mismatches.
5. **Homology confirmation:** `scripts/run_blastp.py` prepares the query + CLI command (with offline cache support) and populates BLAST summaries.
6. **Structural mapping:** `scripts/analyze_structure.py` inspects PDB 4HHB vs 2HBS contacts within 5 Angstroms of beta6, while `scripts/make_structure_figure.py` visualizes the environment.
7. **Interaction-database caution (appendix):** BioGRID/IntAct screenshots live in `docs/archive/ComputationalBio_solutions.pdf` to flag database-dependent partner counts until a scripted export lands.

## Honest Assessment
- **Strong:** Sequence, alignment, BLAST, and structure layers are reproducible with logged outputs, figures, and scripts.
- **Weak:** BLAST execution still depends on locally installed BLAST+ (though cached XML exists), and interaction/dotplot training exercises remain partially manual.
- **Narrative:** README/brief emphasize the workflow and results; notebooks translating the original reference material are still pending.
- **Action items:** Add scripted interaction exports, dotplot notebooks, BLAST XML regeneration snippets, and CI guards for future notebooks.

## Deliverables Checklist
- [x] Repo structure + environment scaffolding
- [x] Automated sequence/alignment/structure scripts
- [ ] Notebooks for dotplot, Needle parameter sweeps, and BLAST parsing
- [ ] Interaction network exports (BioGRID/IntAct) generated programmatically
- [x] Figures renamed and regenerated programmatically (fig01, fig06, fig07, fig08)
- [x] README + transparency statement
- [x] Project brief + communications pack

## References
- Suhail, M. (2024). *Scientific Reports* 14:52476.
- Donkor, A. K., et al. (2023). *Frontiers in Molecular Biosciences* 10:1136970.

## Provenance
- Historical references: docs/archive/ComputationalBio_Directives.pdf and docs/archive/ComputationalBio_solutions.pdf.
