# Alignment Summary

The hemoglobin comparisons quantify how close the secret alpha/beta chains are to their canonical counterparts, while the BRCA1 vs 53BP1 row documents the "tool calibration" exercise from the original coursework—proving the alignment parameters were tested on a hard, low-identity pair before applying them to hemoglobin.

| comparison | identity (%) | alignment_length | score | gap_positions | mismatch_positions | alignment_file |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| HBA_canonical_vs_secret_alpha | 100.00 | 142 | 733.0 | 0 | None | data/processed/alignments/HBA_canonical_vs_secret_alpha.txt |
| HBB_canonical_vs_secret_beta | 99.32 | 147 | 773.0 | 0 | 7 | data/processed/alignments/HBB_canonical_vs_secret_beta.txt |
| BRCA1_vs_53BP1 | 6.73 | 223 | 12.5 | 167 | 83,85,103,105,106,107,108,109,110,111,113,114,115,119,120,121,126,128,129,130,131,137,138,139,140,142,144,145,149,150,151,152,153,154,156,158,159,160,161,162,163 | data/processed/alignments/BRCA1_vs_53BP1.txt |
