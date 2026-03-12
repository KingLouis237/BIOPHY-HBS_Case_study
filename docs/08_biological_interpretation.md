# Biological Interpretation

This case study follows one inference chain: **curated sequence -> global alignment -> substitution scoring -> BLAST confirmation -> structural context**. Each layer answers a different question, and none of them alone proves phenotype. Together, they explain why a single Glu->Val substitution produces the sickle-cell phenotype.

## 1. Sequence-Level Facts
- **Alpha chains** match perfectly across canonical and secret FASTA records, so the phenotype is not alpha-driven in this dataset.
- **Beta chains** diverge at exactly one codon: canonical HBB has glutamate at position 6 (E6), the secret chain has valine (V6). This mirrors the historical HbS mutation described by Ingram and confirmed in modern reviews (Donkor et al. 2023).
- **Chemical meaning:** glutamate is acidic and negatively charged at physiological pH, while valine is hydrophobic and uncharged. Replacing E with V removes a surface charge and exposes a hydrophobic patch that can dock into another hydrophobic pocket.

### Worked example: reading the alignment
Open `figures/fig05_beta_variant_alignment.png` or the text file `data/processed/alignments/HBB_canonical_vs_secret_beta.txt`:
1. Numbering is 1-indexed like UniProt, so the highlighted mismatch at column 6 corresponds to the N-terminal region.
2. Alpha chains are absent because they are identical—keeping the plot focused on the only informative mismatch.
3. The lack of additional mismatches or gaps means downstream interpretations can focus on residue-level chemistry rather than indels or splice variants.

## 2. BLOSUM Scores - Evolutionary warning labels
- BLOSUM62 is an empirical log-odds matrix derived from conserved blocks of related proteins (Henikoff & Henikoff 1992). It encodes how often one residue replaces another across evolution.
- **E->E self-match:** score +5 (strongly favored).
- **E->V substitution:** score -2 (disfavored but not catastrophic like introducing a stop codon).
- **Interpretation:** A negative score simply flags that evolution rarely swaps a charged residue for a hydrophobic one at conserved sites. It is an evolutionary warning label, not a clinical verdict. We still need structural reasoning to argue pathogenicity.

### Worked example: interpreting the BLOSUM figure
1. `figures/fig06_blosum_penalty.png` shows the +5 vs -2 bars side by side.
2. The y-axis is the raw BLOSUM62 score; any negative bar implies an unfavorable substitution given the context.
3. Use this as a conversation starter: "We replaced a charged residue with a hydrophobic one, and the evolutionary odds ratio says that is uncommon."

## 3. BLAST - Family identity, not phenotype
- Restricting BLASTP to *Homo sapiens* ensures we compare only against human hemoglobin variants.
- The top hit is HbS (100% identity), the next hit is canonical HBB (~99.3%), followed by delta-chain hits around 77%.
- **Interpretation:** BLAST confirms the sequence sits in the hemoglobin beta family and that the specific one-residue difference matches known sickle variants. It does **not** tell us whether the sequence is pathogenic or benign; BLAST is about homology, not clinical consequence.
- **Why the cached XML matters:** Everyone sees the same hit ordering, enabling discussion about why a high-identity hit can still mask a severe phenotype.

### Worked example: reading the BLAST figure
1. `figures/fig07_blast_hits.png` plots percent identity on the x-axis and -log10(e-value) on the y-axis (higher is more significant).
2. HbS sits at the far right with the highest -log10(e-value); canonical HBB is slightly left but still near-perfect.
3. When explaining this to a reader, emphasize: "These hits prove we have a hemoglobin beta variant; we still need chemistry and structure to argue how it behaves."

## 4. Structural context - Why residue 6 matters
- Comparing 4HHB (oxyhemoglobin) and 2HBS (deoxy sickle hemoglobin) isolates the structural effect of swapping Glu6 for Val6.
- **Contact counts:** `reports/structure_summary.md` shows a shift toward hydrophobic neighbors in 2HBS near Val6, while Glu6 in 4HHB retains polar contacts.
- **Mechanistic story:** Val6 can insert into a hydrophobic pocket on an adjacent tetramer, stabilizing the long fibers that distort sickled cells (Suhail 2024; Donkor et al. 2023).
- **Visualization:** `figures/fig08_structure_comparison.png` depicts the contact clouds; the 2HBS panel shows a denser hydrophobic cluster around the mutated residue.

### Worked example: interpreting the structure outputs
1. Start with `data/processed/structure_contacts.csv`. Filter rows where `residue_number == 6` to see the classification counts.
2. Note how the `hydrophobic` column increases for 2HBS compared to 4HHB.
3. Open the figure to point out the same trend visually—hydrophobic dots wrap tightly around Val6.

## 5. Putting the inference chain together
| Layer | Question answered | What it cannot conclude |
| --- | --- | --- |
| Sequence QC & alignment | "Is this the HbS mutation and nothing else?" | Cannot explain phenotype or polymerization on its own. |
| BLOSUM scoring | "Is E->V evolutionarily unusual at this site?" | Does not convert to pathogenic probability. |
| BLAST | "Does the sequence belong to the hemoglobin beta family and match known variants?" | Cannot determine clinical severity. |
| Structure contacts/figure | "Does V6 create a hydrophobic patch consistent with polymerization?" | Cannot quantify kinetics or patient outcome. |

The value lies in chaining them: alignment proves the mutation, BLOSUM shows it is non-conservative, BLAST ties it to the HbS lineage, and structure explains why the physical behavior changes. Each step narrows the hypothesis space without over-claiming.

## 6. Supporting databases (context, not proof)
- BioGRID and IntAct disagree slightly on hemoglobin interaction counts. That inconsistency is documented under Supporting Notes to remind readers that database evidence is context-dependent.
- None of the sickling conclusions rely on network screens; they merely illustrate how database choice can sway ancillary interpretations.

## References
- Donkor, A. K. et al. 2023. "A structural view of sickle hemoglobin polymerization." *Frontiers in Molecular Biosciences* 10:1136970.
- Henikoff, S., & Henikoff, J. G. 1992. "Amino acid substitution matrices from protein blocks." *PNAS* 89(22):10915-10919.
- Ingram, V. M. 1956. "A specific chemical difference between the globins of normal human and sickle-cell anaemia haemoglobin." *Nature* 178:792-794.
- Suhail, M. 2024. "Hydrophobic surface exposure drives HbS polymerization." *Scientific Reports* 14:52476.
