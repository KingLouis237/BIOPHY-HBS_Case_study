# Biological Interpretation

## Sequence-Level Evidence
- Alpha chains match exactly, ruling out alpha variants.
- Beta chains differ only at residue 6 (canonical glutamate vs valine), matching the classic sickle-cell variant.
- The BLOSUM62 penalty (-2) indicates a non-conservative swap from acidic to hydrophobic.

## BLAST Perspective
- Local BLAST hits rank HbS first (100% identity), canonical HBB second (~99.3%), delta chain third (~77%).
- The restricted taxonomy (Homo sapiens) avoids confusing non-human beta chains.
- Cached XML ensures readers can parse the same hit list even without BLAST installed.

## Structural Context
- PDB 4HHB (oxy) vs 2HBS (deoxy sickle) show distinct contact shells around residue 6.
- Val6 introduces a hydrophobic surface patch that can dock into hydrophobic pockets on neighboring tetramers, promoting the polymeric fibers seen in sickle cells (Donkor et al. 2023).
- Contact counts reveal slightly more hydrophobic neighbors in 2HBS, reinforcing the qualitative story.

## Interaction Note
- BioGRID vs IntAct disagree on the exact number of reported hemoglobin interactions. This is documented as a supporting note to remind readers that database evidence is context-dependent; it is not part of the core proof.

## References
- Donkor, A. K. et al. 2023. “A structural view of sickle hemoglobin polymerization.” *Frontiers in Molecular Biosciences* 10:1136970.
- Suhail, M. 2024. “Hydrophobic surface exposure drives HbS polymerization.” *Scientific Reports* 14:52476.
