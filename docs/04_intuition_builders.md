# Intuition Builders

## Sequence-Level Thinking
- **Globins are conserved:** Hemoglobin alpha/beta chains are highly conserved; even a single residue change stands out if alignments are configured correctly.
- **Hydrophobicity shift matters:** Valine introduces a nonpolar patch. Because globins live in a crowded environment, small hydrophobic changes can have macroscopic effects.
- **Substitution matrices are heuristics:** BLOSUM62 encodes empirical substitution probabilities. A -2 score for E->V means the change is disfavored relative to neutral swaps, providing a quantitative anchor.

## Alignment Intuition
- **Gap penalties reflect biology:** Setting a high gap-open penalty encodes the belief that globin sequences rarely insert/delete residues. If you lower the penalty, the aligner may invent spurious gaps to “explain” the mismatch.
- **Calibration first:** Running BRCA1<->53BP1 calibrates expectations—when the sequences truly differ, dotplots and alignments look messy. When the sequences are homologous, diagonals pop immediately.

## BLAST Intuition
- **Taxonomy filter reduces noise:** Restricting BLAST to Homo sapiens (taxid 9606) cuts out similar non-human beta chains, keeping the interpretation simple.
- **Cached XML is your friend:** BLAST is stochastic if e-value thresholds change; version the XML so that figures and summaries remain stable across machines.

## Structure Intuition
- **Contact shells tell stories:** Counting residues within 5 Angstroms highlights the chemical environment faster than opening a GUI. Hydrophobic residues cluster differently in 4HHB vs 2HBS.
- **Val6 polymerization:** A hydrophobic residue on the exterior of deoxyhemoglobin can dock into a hydrophobic pocket on another tetramer, triggering the fiber seen in sickle cells (Donkor et al. 2023).

## Analytical Flow
1. **QC metrics** build trust in the FASTA bundle.
2. **Calibration alignments** set expectations for parameter behavior.
3. **Core alignments** confirm the exact mismatch.
4. **Substitution scoring** quantifies how “bad” the change is.
5. **BLAST confirmation** places the sequence among known variants.
6. **Structure context** explains why the variant matters biologically.
