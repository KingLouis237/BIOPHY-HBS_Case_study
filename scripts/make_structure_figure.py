import argparse
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from Bio.PDB import PDBParser

AA_CLASSES: Dict[str, str] = {
    "ALA": "hydrophobic",
    "VAL": "hydrophobic",
    "ILE": "hydrophobic",
    "LEU": "hydrophobic",
    "MET": "hydrophobic",
    "PHE": "hydrophobic",
    "TRP": "hydrophobic",
    "TYR": "hydrophobic",
    "PRO": "hydrophobic",
    "GLY": "neutral",
    "SER": "polar",
    "THR": "polar",
    "ASN": "polar",
    "GLN": "polar",
    "CYS": "polar",
    "HIS": "positive",
    "LYS": "positive",
    "ARG": "positive",
    "ASP": "negative",
    "GLU": "negative",
}

COLORS = {
    "hydrophobic": "#d62728",
    "polar": "#1f77b4",
    "positive": "#2ca02c",
    "negative": "#9467bd",
    "neutral": "#8c564b",
    "unknown": "#7f7f7f",
}


def classify(resname: str) -> str:
    return AA_CLASSES.get(resname, "unknown")


def collect_contacts(pdb_path: Path, chain_id: str, residue_number: int, radius: float) -> Tuple[np.ndarray, List[str]]:
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(pdb_path.stem, pdb_path)
    model = structure[0]
    chain = model[chain_id]
    target = chain[(" ", residue_number, " ")]
    if "CA" not in target:
        raise SystemExit(f"Residue {residue_number} missing CA atom in {pdb_path}")
    target_coord = target["CA"].coord
    coords: List[np.ndarray] = []
    classes: List[str] = []
    for residue in chain:
        if "CA" not in residue:
            continue
        coord = residue["CA"].coord
        distance = np.linalg.norm(coord - target_coord)
        if distance <= radius:
            coords.append(coord - target_coord)
            classes.append(classify(residue.get_resname()))
    return np.array(coords), classes


def plot_structures(structures: List[Tuple[str, Path]], chain_id: str, residue_number: int, radius: float, out_path: Path) -> None:
    fig = plt.figure(figsize=(12, 5))
    for idx, (label, pdb_path) in enumerate(structures, start=1):
        coords, classes = collect_contacts(pdb_path, chain_id, residue_number, radius)
        ax = fig.add_subplot(1, len(structures), idx, projection="3d")
        for class_name in sorted(set(classes)):
            mask = [cls == class_name for cls in classes]
            points = coords[mask]
            ax.scatter(points[:, 0], points[:, 1], points[:, 2], label=class_name, s=30, color=COLORS.get(class_name, "#333333"))
        ax.scatter([0], [0], [0], color="#ff7f0e", s=120, marker="*", label="beta6")
        ax.set_title(f"{label} (beta6 neighborhood)")
        ax.set_xlabel("x (Å)")
        ax.set_ylabel("y (Å)")
        ax.set_zlabel("z (Å)")
        ax.view_init(elev=20, azim=45)
        if idx == len(structures):
            ax.legend(loc="upper right", fontsize=8)
    fig.suptitle("4HHB vs 2HBS beta6 contact clouds (radius {:.1f} Å)".format(radius))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot neighborhood of beta6 for 4HHB vs 2HBS.")
    parser.add_argument("--radius", type=float, default=6.0)
    parser.add_argument("--output", default="figures/fig08_structure_comparison.png")
    parser.add_argument("--pdb", nargs="+", default=["4HHB", "2HBS"])
    parser.add_argument("--pdb-dir", default="data/raw/pdb")
    parser.add_argument("--chain", default="B")
    parser.add_argument("--residue", type=int, default=6)
    args = parser.parse_args()

    structures: List[Tuple[str, Path]] = []
    for pdb_code in args.pdb:
        path = Path(args.pdb_dir) / f"{pdb_code}.pdb"
        if not path.exists():
            raise SystemExit(f"Missing PDB file: {path}")
        structures.append((pdb_code, path))
    plot_structures(structures, args.chain, args.residue, args.radius, Path(args.output))


if __name__ == "__main__":
    main()
