# Pipeline Logic

This document explains each script from first principles: what question it answers, how it works, and how to sanity-check the results.

## scripts/sequence_summary.py
- **Question:** How do the canonical and secret chains differ in length, hydrophobicity, and basic charge?
- **Method:** Parses FASTA records, computes metrics with Biopython+custom logic, writes TSV + Markdown summaries.
- **Key parameters:** None beyond file paths—determinism is driven by the input FASTA bundle.
- **Alternative:** Could use `seqkit fx2tab`, but Python keeps the metrics close to downstream scripts.
- **Failure modes:** malformed FASTA headers; missing secret sequences. Check logs for “record not found.”
- **Validation:** `data/processed/sequence_summary.tsv` should show identical lengths for the canonical and secret beta chains; hydrophobicity should spike slightly for the secret beta because Val is hydrophobic.
- **Biological interpretation:** Provides the coarse QC that establishes the baseline before alignment.

## scripts/run_alignments.py
- **Question:** Are the secret sequences truly variants of HBA/HBB, and how big is the mismatch?
- **Method:** Biopython `pairwise2` global alignment with BLOSUM62, gap-open 10, gap-extend 0.5.
- **Key parameters:** Gap penalties; raising them penalizes insertions, which is appropriate for closely related globins.
- **Alternatives:** EMBOSS `needle`, or the newer `Bio.Align.PairwiseAligner` API when pairwise2 fully deprecates.
- **Failure modes:** `Bio.pairwise2` deprecation warnings (harmless), missing FASTA headers, gap penalties set too low (spurious indels).
- **Validation:** `data/processed/alignment_summary.tsv` should report 99.32% identity for beta chains with mismatch at residue 6/7 (1-indexed).
- **Biological interpretation:** Confirms that only the E6V change distinguishes the secret beta chain.

## scripts/make_figures.py
- **Question:** What do the QC metrics look like, and how does the BLOSUM penalty visualize?
- **Method:** Matplotlib bar charts for lengths/hydrophobicity and BLOSUM score comparison.
- **Key parameters:** None besides file paths; figure aesthetics tuned for readability.
- **Alternatives:** Seaborn could provide prettier defaults, but Matplotlib keeps dependency footprint small.
- **Failure modes:** Missing TSV; ensure `sequence_summary.py` ran first.
- **Validation:** `figures/fig01_sequence_characteristics.png` and `figures/fig06_blosum_penalty.png` regenerate without manual edits.
- **Biological interpretation:** Shows the hydrophobic shift and explicit penalty for E->V.

## scripts/make_dotplots.py
- **Question:** Does the alignment behave as expected across parameter sweeps, and can we visualize the single mismatch?
- **Method:** Custom sliding-window scoring with BLOSUM62; generates multi-panel dotplots for BRCA1<->53BP1 calibration and HBA/HBB comparisons.
- **Key parameters:** word size, score threshold. Lower thresholds detect more similarities but increase noise.
- **Alternatives:** EMBOSS `dotmatcher`, but shipping PNGs from a script keeps things reproducible and version-controlled.
- **Failure modes:** Overly low thresholds (noisy plots), or missing sequences.
- **Validation:** Calibration plots should show sparse diagonals for BRCA1<->53BP1; HBA/HBB plots should show clean diagonals with a tiny gap around residue 6 for beta.
- **Biological interpretation:** Builds intuition for how the single mismatch manifests visually.

## scripts/make_alignment_figure.py
- **Question:** Can we show the exact residue difference with numbering intact?
- **Method:** Chunks the canonical vs secret beta alignment into 30-aa blocks and annotates mismatches.
- **Key parameters:** chunk size for readability; mismatch annotation arrow.
- **Alternatives:** `biotite.sequence.graphics` offers similar visuals but needs extra dependencies.
- **Failure modes:** Sequence length mismatch (indicates earlier QC failed).
- **Validation:** `figures/fig05_beta_variant_alignment.png` should highlight only residue 6.
- **Biological interpretation:** Makes the E6V substitution obvious for readers unfamiliar with text alignments.

## scripts/run_blastp.py and scripts/make_blast_figure.py
- **Question:** Do BLAST hits confirm the variant as hemoglobin beta, and how confident are the top hits?
- **Method:** Prepares the secret beta query, runs BLASTP locally if available (or remote via `Bio.Blast.NCBIWWW`), falls back to cached XML, then parses top hits and plots identity vs e-value.
- **Key parameters:** database (SwissProt), taxid=9606, max target sequences (default 5), e-value threshold 1e-20.
- **Alternatives:** HMMER or diamond for faster searches, but BLAST remains canonical for small case studies.
- **Failure modes:** BLAST not installed, network blocked, cache missing. Use `--offline` to force cached XML.
- **Validation:** `reports/blast_summary.md` should list HbS (100% identity) followed by canonical HBB (~99.3%).
- **Biological interpretation:** Confirms the secret beta aligns with known hemoglobin variants such as HbS/Hb Monza.

## scripts/analyze_structure.py and scripts/make_structure_figure.py
- **Question:** What does the residue-6 neighborhood look like in 4HHB vs 2HBS?
- **Method:** Uses `Bio.PDB` NeighborSearch to count residues within a radius (default 5 Angstroms) around residue 6 in chain B, then renders 3D scatter plots colored by residue class.
- **Key parameters:** search radius (adjust to test tighter or broader environments).
- **Alternatives:** PyMOL scripts or MDAnalysis; Biopython suffices for first-order contact counts.
- **Failure modes:** Missing PDB files, chain IDs changing after manual edits, dependencies on `numpy`.
- **Validation:** `data/processed/structure_contacts.csv` should list hydrophobic contacts close to Val6; `figures/fig08_structure_comparison.png` should show a denser hydrophobic cloud for 2HBS.
- **Biological interpretation:** Highlights the hydrophobic patch that drives polymerization in sickled cells (Suhail 2024).
