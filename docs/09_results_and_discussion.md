# Results & Discussion

This section ties every reproducible artifact back to a biological takeaway. Think of it as a guided reading exercise: what did each layer show, why is it trustworthy, and what does it still leave unanswered?

## 1. What the data actually showed
| Layer | Evidence | Interpretation | Limits |
| --- | --- | --- | --- |
| Sequence QC | Identical lengths, secret beta slightly more hydrophobic | Only one codon changed; chemistry tilts toward hydrophobicity. | QC alone cannot explain phenotype. |
| Global alignments | 99.32% beta identity with a single mismatch at residue 6 | The glutamate?valine substitution is confirmed and isolated. | Alignment cannot explain why the swap matters. |
| BLOSUM scoring | +5 for E->E vs -2 for E->V | Evolution rarely swaps charged residues for hydrophobes at conserved positions. | BLOSUM is statistical, not clinical. |
| BLAST hits | HbS (100%) > canonical HBB (~99.3%) > delta-chain (~77%) | Confirms hemoglobin beta family membership and proximity to sickle variants. | Homology search does not assess pathogenicity. |
| Structure contacts | Val6 neighborhood becomes hydrophobic in 2HBS | Provides a mechanistic reason for polymerization propensity. | Static structures do not capture kinetics or whole-cell context. |

## 2. Reading the outputs with intent
### Alignment excerpt
```
1  MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVL
   ||||||X|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
1  MVHLTPVEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVL
```
- The lone `X` marks the E6V mismatch. Nothing else differs, so interpretation can focus entirely on residue 6 chemistry.

### BLOSUM figure (fig06)
- Bars quantify the evolutionary log-odds. Treat the negative bar as a “rare in nature” indicator, not a diagnostic score.
- When teaching, ask: *What sort of environment prefers a hydrophobic residue here?* Lead the reader back to the structure layer.

### BLAST plot (fig07)
- X-axis is percent identity; y-axis is -log10(e-value). Hits cluster in the top-right, so we know the secret sequence belongs to the HBB family.
- Note how HbS and canonical HBB sit only a fraction apart on the x-axis even though their phenotypes differ drastically. This is why we need the structure discussion.

### Structure figure (fig08)
- Hydrophobic contacts (orange) wrap more tightly around Val6 in 2HBS than around Glu6 in 4HHB.
- Combine this with the tabular counts in `data/processed/structure_contacts.csv` to argue that the mutation exposes a “sticky” patch.

## 3. Why a single residue can drive a phenotype
1. **Charge removal:** Glu6 contributes a negative charge to the surface. Removing it reduces electrostatic repulsion between neighboring tetramers (Donkor et al. 2023).
2. **Hydrophobic insertion:** Val6 fits into a complementary hydrophobic pocket on a neighboring deoxy tetramer, stabilizing polymer nuclei (Suhail 2024).
3. **Polymer growth:** Once a nucleus forms, additional tetramers add on, distorting red blood cells and impeding oxygen delivery.
4. **Takeaway:** Even though BLAST sees “almost the same” sequence, the physicochemical context changes completely, illustrating why sequence identity must be paired with structural reasoning.

## 4. Honest caveats
- **Educational vs inferential:** This repo reproduces known sickle-cell reasoning; it does not discover a novel variant.
- **Static structures:** 4HHB and 2HBS capture snapshots. They do not encode solvent dynamics, post-translational modifications, or red-cell crowding effects.
- **BLAST cache:** Using a cached XML ensures reproducibility but also freezes the database date. If UniProt/Swiss-Prot adds new hemoglobin variants, rerun BLAST online and document the refresh.
- **Interaction note:** BioGRID/IntAct material remains a supporting caution. It reminds readers that database evidence varies, but it is not part of the causal chain proved here.

## 5. Suggested discussion prompts
- How would you test whether the hydrophobic patch is sufficient for polymerization? (Answer: molecular dynamics, mutational scanning, or wet-lab assays.)
- What alternative alignments could stress-test the mutation call? (Run pairwise alignments with different gap penalties or use EMBOSS `needle`.)
- How might population frequency data change the story? (Out of scope here; would require allele-frequency databases.)

## References
- Donkor, A. K. et al. 2023. "A structural view of sickle hemoglobin polymerization." *Frontiers in Molecular Biosciences* 10:1136970.
- Suhail, M. 2024. "Hydrophobic surface exposure drives HbS polymerization." *Scientific Reports* 14:52476.
- Wilkinson, M. D. et al. 2016. "The FAIR Guiding Principles for scientific data management and stewardship." *Scientific Data* 3:160018.
