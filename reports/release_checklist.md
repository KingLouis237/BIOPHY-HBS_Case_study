# Release Readiness Checklist

## Must-fix before posting
- [ ] Scripted interaction-network exports (replace the remaining screenshots / manual counts via BioGRID + IntAct APIs).
- [ ] Document the cached BLAST XML provenance inside eports/blast_summary.md once an online BLAST run is available (swap in true NCBI output when possible).

## Optional improvements for later
- [ ] Notebook visualization of the BRCA1?53BP1 gap penalty sweep to complement scripts/run_alignments.py.
- [ ] 3D structural figure (fig08_structure_comparison.png) generated from PyMOL or py3Dmol snapshots.
- [ ] Automated BLAST parser that emits JSON/TSV for downstream notebooks.
- [ ] Expand smoke-test workflow to lint/format notebooks once they land.
