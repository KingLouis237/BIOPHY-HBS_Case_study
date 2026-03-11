# Project At A Glance

## What This Repository Does
- Tracks the hemoglobin beta (HBB) Glu6Val mutation from raw sequence data through structural context.
- Rebuilds the analysis into a reproducible case study with transparent scripts, cached artifacts, and workflow notes.
- Separates the core computational workflow from supporting educational notes and archived provenance.

## Why It Matters
- HBB E6V causes the sickle-cell phenotype by replacing a charged glutamate with a hydrophobic valine, enabling abnormal polymerization (Donkor et al. 2023).
- Reproducing the analysis builds trust in the data pipeline and demonstrates how to argue from sequence to structure without hidden steps.

## Core Ingredients
- **Sequences:** UniProt reviewed entries P69905 (HBA) and P68871 (HBB) plus the provided "secret" alpha/beta FASTA bundle.
- **Structures:** 4HHB (oxyhemoglobin) and 2HBS (deoxy sickle hemoglobin).
- **Software:** Python 3.11, Biopython, Matplotlib, EMBOSS-style alignment parameters, BLAST+, uv, and conda.

## Immediate Takeaways
- Alpha chains match perfectly; beta chains differ only at residue 6, confirming the E6V substitution.
- BLOSUM62 scoring shows the canonical E->E self-match (+5) versus the E->V penalty (-2), quantifying the functional cost.
- Structural contact analysis demonstrates how Val6 introduces a hydrophobic patch that favors the insoluble sickle polymer (Suhail 2024).

## Reading Order
1. **02_reproducibility.md** for environments, caching, and offline rules.
2. **03_pipeline_logic.md** to understand how each script answers a specific question.
3. **06_runbook.md** when you are ready to execute commands.
4. **08_biological_interpretation.md** and **09_results_and_discussion.md** for the biological meaning.
5. **10_limitations_and_future_work.md** for what is still partial or educational.
