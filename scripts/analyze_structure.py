import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from Bio.PDB import NeighborSearch, PDBParser

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


def classify(resname: str) -> str:
    return AA_CLASSES.get(resname, "unknown")


def residue_contacts(structure_id: str, pdb_path: Path, chain_id: str, residue_number: int, radius: float) -> Tuple[List[Dict[str, str]], Counter, Dict[str, List[float]]]:
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(structure_id, pdb_path)
    model = structure[0]
    target = model[chain_id][(" ", residue_number, " ")]
    ns = NeighborSearch(list(structure.get_atoms()))
    contacts: Dict[Tuple[str, int, str], Dict[str, str]] = {}
    for atom in target:
        neighbors = ns.search(atom.coord, radius)
        for neighbor in neighbors:
            parent = neighbor.get_parent()
            if parent is target:
                continue
            resid = parent.get_id()
            if resid[0].strip():
                continue
            key = (parent.get_parent().id, resid[1], parent.get_resname())
            classification = classify(key[2])
            dist_value = float(np.linalg.norm(atom.coord - neighbor.coord))
            if key not in contacts or dist_value < float(contacts[key]["min_distance"]):
                contacts[key] = {
                    "structure": structure_id,
                    "chain": key[0],
                    "residue_number": str(key[1]),
                    "residue_name": key[2],
                    "classification": classification,
                    "min_distance": dist_value,
                }
    class_counter = Counter()
    class_distances: Dict[str, List[float]] = defaultdict(list)
    rows: List[Dict[str, str]] = []
    for info in contacts.values():
        class_counter[info["classification"]] += 1
        class_distances[info["classification"]].append(float(info["min_distance"]))
        info["min_distance"] = f"{info['min_distance']:.2f}"
        rows.append(info)
    return rows, class_counter, class_distances


def format_distance_stats(distances: Dict[str, List[float]]) -> List[str]:
    lines: List[str] = []
    for class_name in sorted(distances):
        values = distances[class_name]
        if values:
            lines.append(
                f"  - closest {class_name} contact: {min(values):.2f} Angstroms (median ~{median(values):.2f})"
            )
    return lines


def median(values: List[float]) -> float:
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    mid = n // 2
    if n == 0:
        return 0.0
    if n % 2 == 0:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
    return sorted_vals[mid]


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize contacts around residue beta6 in hemoglobin structures")
    parser.add_argument("--radius", type=float, default=5.0, help="contact search radius in Angstroms")
    parser.add_argument("--output", default="data/processed/structure_contacts.csv")
    parser.add_argument("--summary", default="reports/structure_summary.md")
    args = parser.parse_args()

    configs = [
        ("4HHB", Path("data/raw/pdb/4HHB.pdb")),
        ("2HBS", Path("data/raw/pdb/2HBS.pdb")),
    ]
    all_rows: List[Dict[str, str]] = []
    summary_lines: List[str] = []
    for struct_id, pdb_path in configs:
        contacts, counter, distances = residue_contacts(struct_id, pdb_path, "B", 6, args.radius)
        for row in contacts:
            row["structure"] = struct_id
        all_rows.extend(contacts)
        total_contacts = sum(counter.values())
        summary_lines.append(f"### {struct_id}\n")
        summary_lines.append(f"- Contacts within {args.radius} Angstroms: {total_contacts}\n")
        for class_name in sorted(counter):
            summary_lines.append(f"  - {class_name}: {counter[class_name]}\n")
        summary_lines.extend(format_distance_stats(distances))
        summary_lines.append("")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if all_rows:
        fieldnames = ["structure", "chain", "residue_number", "residue_name", "classification", "min_distance"]
        with output_path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_rows)

    summary_path = Path(args.summary)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with summary_path.open("w", encoding="utf-8") as handle:
        handle.write("# Structural Neighborhood of beta6\n\n")
        handle.write("Residues classified using a coarse-grained scheme (hydrophobic, polar, positive, negative, unknown).\n\n")
        handle.write("\n".join(summary_lines))
        handle.write("\n> Contacts computed with Bio.PDB NeighborSearch on chains B (beta subunits) of 4HHB and 2HBS.\n")


if __name__ == "__main__":
    main()
