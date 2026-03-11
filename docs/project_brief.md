# Hemoglobin beta E6V Variant — Sequence-to-Structure Interpretation

**Author:** Louis Ashu Abane  
**Origin:** Reframed from an archived graduate bioinformatics practicum brief (see `docs/archive/INFO-F434_assignment_original.pdf`).  
**Date reformatted:** 11 March 2026.

## Context
This professional brief preserves the underlying scientific workflow while removing classroom-specific language. The goal is to communicate a reproducible, inspectable portfolio narrative; novelty or clinical claims are not implied.

## Objective
Diagnose the molecular consequence of the unknown "secret" globin sequence by linking curated sequence evidence, substitution scoring, and structural inspection.

## Data & Inputs
- UniProt reviewed entries P69905 (HBA) and P68871 (HBB).
- Provided secret alpha/beta FASTA files stored under `data/raw/secret_sequences/`.
- Interaction metadata via BioGRID and IntAct cross-references (documented as an appendix caution).
- PDB structures: 4HHB (hemoglobin A) and 2HBS (hemoglobin S).
- Literature: Suhail 2024 (*Scientific Reports* 14:52476) and Donkor et al. 2023 (*Frontiers Mol. Biosci.* 10:1136970).

## Methods
1. **Sequence retrieval** — Python scripts download UniProt sequences, metadata, and provenance logs.
2. **Interaction audit (appendix)** — BioGRID vs IntAct interactors are summarized to emphasize database-specific evidence.
3. **Parameter calibration** — BRCA1 vs 53BP1 dotplots/global alignments illustrate how wordsize, threshold, and gap penalties impact sensitivity.
4. **Variant localization** — Canonical vs secret alpha/beta alignments reveal identical alpha chains and a single beta E6V substitution.
5. **Substitution scoring** — BLOSUM62 (score –2) plus residue chemistry (acidic → hydrophobic) quantify severity.
6. **Homology confirmation** — BLASTP restricted to *Homo sapiens* identifies the secret beta chain as a hemoglobin variant (e.g., Hb Monza/HbS).
7. **Structural mapping** — py3Dmol overlays beta6 in 4HHB vs 2HBS, illustrating the hydrophobic patch that nucleates HbS polymers.

## Key Findings
- Alpha-chain comparison shows 100 % identity; beta-chain comparison yields 99.3 % identity with a single Glu6Val substitution.
- BLOSUM62 and physicochemical reasoning classify E6V as a non-conservative, charge-to-hydrophobe swap.
- BLAST and PDB inspection corroborate the secret sequence as a sickle-cell hemoglobin variant; structural context explains polymerization propensity.

## Limitations
- Interaction-network exports remain screenshot-based and live in the appendix; scripting is ongoing.
- No quantitative structural metrics (RMSD, solvent-accessible surface area) yet—interpretation remains qualitative.
- Clinical translation, population genetics, and experimental validation are out of scope.

## Reproducibility Plan
- Pin Python and tool versions via `environment/environment.yml` and `uv.lock`.
- Store raw FASTA/PDB downloads with metadata manifests.
- Version-control EMBOSS/BLAST parameters (`environment/emboss_params.json`).
- Provide notebooks with deterministic seeds and text-based outputs for CI diffing.

## Transparency Statement
Original academic materials remain untouched in `docs/archive/`. This derivative brief exists for recruiter- and collaborator-facing contexts while explicitly acknowledging those origins.
