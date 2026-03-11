# Figure Inventory

| File | Caption | Status | Script / Notebook |
| --- | --- | --- | --- |
| fig01_sequence_characteristics.png | Sequence length and hydrophobic fraction comparison for canonical HBA/HBB, secret alpha/beta, and calibration sequences. | generated | `scripts/make_figures.py` |
| fig02_interaction_networks.png | Supporting database interpretation note: BioGRID vs IntAct partner counts for HBA/HBB illustrating database-dependent evidence (see Supporting Notes & Provenance). | manual evidence archived; scripting deferred | _supporting note_ |
| fig03_dotplots_brca1_53bp1.png | BRCA1 vs 53BP1 dotplots across multiple word/threshold settings to show parameter sensitivity before the hemoglobin runs. | generated | `scripts/make_dotplots.py` |
| fig04a_dotplot_hba_secret.png | Canonical vs secret alpha chain dotplot tuned to emphasize alignment diagonals. | generated | `scripts/make_dotplots.py` |
| fig04b_dotplot_hbb_secret.png | Canonical vs secret beta chain dotplot tuned around the E6V mismatch. | generated | `scripts/make_dotplots.py` |
| fig05_beta_variant_alignment.png | Chunked alignment of canonical HBB vs secret beta highlighting the single E6V substitution with residue numbering. | generated | `scripts/make_alignment_figure.py` |
| fig06_blosum_penalty.png | BLOSUM62 score comparison between the canonical E->E self match and the E->V substitution penalty. | generated | `scripts/make_figures.py` |
| fig07_blast_hits.png | Horizontal bar chart of top BLASTP hits (swissprot, taxid 9606) for the secret beta sequence with percent identity and e-values. | generated | `scripts/make_blast_figure.py` |
| fig08_structure_comparison.png | 3D scatter of beta6-centered contact clouds in 4HHB vs 2HBS (chain B), colored by residue class and centered on residue 6. | generated | `scripts/make_structure_figure.py` |

**Supporting note:** fig02 remains a documentation artifact until scripted BioGRID/IntAct exports are added. It complements the reproducible workflow but is not yet regenerated automatically.
