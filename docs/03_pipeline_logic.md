# Pipeline Logic (First Principles)

Every script in `scripts/` exists for a reason. The sections below spell out the question being asked, why the method was chosen, how to run sanity checks, and what biological story each output supports.

## scripts/sequence_summary.py
- **Purpose / Question** – Establish basic QC: Are the canonical and secret chains comparable in length, hydrophobicity, and acid/base balance?
- **Inputs** – All `*.fasta` files under `data/raw/uniprot/` plus `data/raw/secret_sequences/hemoglobin_secret_sequences.fasta`.
- **Outputs** – `data/processed/sequence_summary.tsv` (machine-readable) and `reports/sequence_summary.md` (human-readable).
- **Why this method** – A tiny Biopython parser keeps QC logic close to the rest of the case study without adding CLI dependencies.
- **Key parameters** – None; determinism comes entirely from the versioned FASTA bundle.
- **Alternatives** – `seqkit fx2tab` or EMBOSS `pepstats`, but they increase the binary footprint for minimal gain.
- **Common failure modes** – Missing FASTA headers, stray carriage returns from copy/paste, or an empty `secret_sequences` folder.
- **Validation checks** – Canonical and secret beta lengths should match, and the secret beta hydrophobic fraction should be marginally higher because Val replaces Glu6.
- **Biological interpretation** – Provides the coarse QC proving we are comparing like with like before alignment.

## scripts/run_alignments.py
- **Purpose / Question** – Do the secret alpha/beta chains align globally to HBA/HBB, and exactly where is the mismatch?
- **Inputs** – FASTA pairs listed in the `ALIGNMENT_TASKS` tuple (canonical UniProt sequences plus the secret FASTA bundle).
- **Outputs** – `data/processed/alignment_summary.tsv` and plain-text alignments under `data/processed/alignments/`.
- **Why this method** – Biopython’s `pairwise2` gives deterministic Needleman–Wunsch alignments with BLOSUM62 scoring without leaving Python.
- **Key parameters** – Gap open (`10`) and gap extend (`0.5`) penalties tuned for closely related globins; change only if you intentionally want to test indel sensitivity.
- **Alternatives** – EMBOSS `needle` or the newer `Bio.Align.PairwiseAligner` once `pairwise2` fully deprecates.
- **Common failure modes** – Setting gap penalties too low (spurious indels) or letting deprecation warnings hide real errors.
- **Validation checks** – Beta chains should report ~99.3?% identity with a single mismatch near residue 6/7 (1-indexed).
- **Biological interpretation** – Proves that E6V is the only sequence-level difference of interest.

## scripts/make_figures.py
- **Purpose / Question** – How do the QC metrics and the BLOSUM penalty look when visualized?
- **Inputs** – `data/processed/sequence_summary.tsv`.
- **Outputs** – `figures/fig01_sequence_characteristics.png` and `figures/fig06_blosum_penalty.png`.
- **Why this method** – Matplotlib keeps dependencies minimal while allowing explicit annotations.
- **Key parameters** – None; axes and color palettes are prebaked for clarity.
- **Alternatives** – Seaborn or Plotly, but they add weight for marginal benefit.
- **Common failure modes** – Running before `sequence_summary.py` (missing TSV).
- **Validation checks** – Bars should show identical lengths for beta, with a small hydrophobic bump for the secret chain; the BLOSUM plot should display +5 for E?E vs -2 for E?V.
- **Biological interpretation** – Visually quantifies how swapping a charged residue for a hydrophobic one is penalized in evolutionary scoring matrices.

## scripts/make_dotplots.py
- **Purpose / Question** – Can we visualize how alignment parameters behave on both a difficult (BRCA1?53BP1) and an easy (globin) pair?
- **Inputs** – FASTA files for BRCA1, 53BP1, and the hemoglobin/secret sequences.
- **Outputs** – `figures/fig03_dotplots_brca1_53bp1.png`, `figures/fig04a_dotplot_hba_secret.png`, and `figures/fig04b_dotplot_hbb_secret.png`.
- **Why this method** – Custom plotting keeps the parameter sweep under version control and avoids unscripted GUI screenshots.
- **Key parameters** – Word size and score threshold; lowering them increases sensitivity at the cost of noise.
- **Alternatives** – EMBOSS `dotmatcher` or `yass`, but they do not integrate as cleanly into this repo.
- **Common failure modes** – Forgetting to populate `data/raw/secret_sequences/`, or setting the threshold so low the image becomes pure noise.
- **Validation checks** – BRCA1?53BP1 plots should show sparse diagonals; hemoglobin plots should show a crisp diagonal with a tiny gap near residue 6 for beta.
- **Biological interpretation** – Builds intuition for why we trust the globin alignment even though the calibration pair is messy.

## scripts/make_alignment_figure.py
- **Purpose / Question** – Highlight the exact residue difference with residue numbers intact.
- **Inputs** – Canonical beta FASTA and secret beta FASTA.
- **Outputs** – `figures/fig05_beta_variant_alignment.png`.
- **Why this method** – Chunking and annotating inside Python guarantees a reproducible alignment graphic without manual PowerPoint edits.
- **Key parameters** – `--chunk-size` (default 30) and whether to annotate mismatches with colors/arrows.
- **Alternatives** – `biotite.sequence.graphics` or Jalview exports, but they add heavier dependencies.
- **Common failure modes** – Changing chunk size so large that the mismatch becomes hard to spot, or having mismatched sequences (indicates earlier QC failed).
- **Validation checks** – Only residue 6 should be marked, and numbering should match the UniProt sequence.
- **Biological interpretation** – Gives reviewers a one-glance confirmation that the variant is E6V.

## scripts/run_blastp.py
- **Purpose / Question** – Does BLAST confirm that the secret beta chain is a known HBB variant, and who are the nearest neighbors?
- **Inputs** – `data/raw/secret_sequences/hemoglobin_secret_sequences.fasta` plus cached XML under `data/processed/blast/`.
- **Outputs** – `data/processed/blast/secret_beta_query.fasta`, `data/processed/blast/secret_beta_blast.xml`, `reports/blast_summary.md`, and `reports/blast_protocol.md`.
- **Why this method** – BLASTP remains the most recognizable homology search; wrapping it in a Python script documents the exact command and the offline fallback.
- **Key parameters** – Database (Swiss-Prot), `--taxid 9606`, `--max-target-seqs`, optional `--offline` to skip network calls.
- **Alternatives** – DIAMOND or HMMER for speed/sensitivity, but they add installation hurdles for a teaching repo.
- **Common failure modes** – BLAST+ not installed, network blocks remote searches, cached XML missing.
- **Validation checks** – The top hit should be HbS or Hb Monza at 100?% identity; canonical HBB should appear next with ~99.3?%.
- **Biological interpretation** – Confirms that the secret sequence maps to the sickle-cell lineage described in Donkor et al. (2023).

## scripts/make_blast_figure.py
- **Purpose / Question** – How do BLAST hit identity and e-value distribute at a glance?
- **Inputs** – `data/processed/blast/secret_beta_blast.xml`.
- **Outputs** – `figures/fig07_blast_hits.png`.
- **Why this method** – A compact Matplotlib chart communicates confidence faster than raw BLAST text.
- **Key parameters** – None beyond the XML path; labels are shortened automatically to stay legible.
- **Alternatives** – Plotly for interactive hover details, but static PNGs are better for GitHub rendering.
- **Common failure modes** – Forgetting to run `run_blastp.py` first or using an outdated cached XML.
- **Validation checks** – HbS should sit at 100?% identity with tiny e-values; the rest should fall off quickly.
- **Biological interpretation** – Reinforces that the variant clusters with sickle-cell hemoglobin rather than unrelated proteins.

## scripts/analyze_structure.py
- **Purpose / Question** – What residue classes surround position 6 in the 4HHB and 2HBS structures?
- **Inputs** – `data/raw/pdb/4HHB.pdb` and `data/raw/pdb/2HBS.pdb`.
- **Outputs** – `data/processed/structure_contacts.csv` and `reports/structure_summary.md`.
- **Why this method** – Biopython’s `NeighborSearch` performs fast distance queries without requiring PyMOL or MDAnalysis.
- **Key parameters** – `--radius` (default 5 Å) controls how many neighbors count as “contacts”.
- **Alternatives** – Salt-bridge calculators or solvent-accessible surface tools; useful later but out of scope here.
- **Common failure modes** – Missing PDB files, incorrect chain IDs, or forgetting to strip alternate locations.
- **Validation checks** – The CSV should list more hydrophobic contacts near Val6 in 2HBS than near Glu6 in 4HHB.
- **Biological interpretation** – Quantifies the creation of a hydrophobic patch that nucleates sickle fibers (Suhail 2024).

## scripts/make_structure_figure.py
- **Purpose / Question** – Can we show those contact differences visually?
- **Inputs** – `data/processed/structure_contacts.csv`.
- **Outputs** – `figures/fig08_structure_comparison.png`.
- **Why this method** – A 3D scatter plot rendered via Matplotlib projects well on GitHub while remaining reproducible.
- **Key parameters** – Point colors/sizes linked to residue classification; camera angle chosen for best overlap comparison.
- **Alternatives** – py3Dmol or PyMOL sessions for interactive rotations (future work).
- **Common failure modes** – Running before `analyze_structure.py` (missing CSV) or rendering without a display backend (Agg is already configured).
- **Validation checks** – 2HBS should show a denser cluster of hydrophobic contacts around Val6 compared to the Glu6 scene.
- **Biological interpretation** – Complements the contact counts by giving readers an intuitive sense of the hydrophobic pocket.
