import argparse
import csv
from pathlib import Path
from typing import Dict, List

AMINO_ACID_GROUPS: Dict[str, set[str]] = {
    "hydrophobic": set("AVILMFYWPG"),
    "polar": set("STNQCY"),
    "acidic": set("DE"),
    "basic": set("KRH"),
}


def read_fasta(path: Path) -> List[Dict[str, str]]:
    records: List[Dict[str, str]] = []
    header = None
    seq_lines: List[str] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header is not None:
                records.append({"header": header, "sequence": "".join(seq_lines)})
            header = line[1:].strip()
            seq_lines = []
        else:
            seq_lines.append(line)
    if header is not None:
        records.append({"header": header, "sequence": "".join(seq_lines)})
    return records


def compute_metrics(name: str, sequence: str, source: Path) -> Dict[str, str]:
    length = len(sequence)
    counts = {key: sum(aa in group for aa in sequence) for key, group in AMINO_ACID_GROUPS.items()}
    hydrophobic_frac = counts["hydrophobic"] / length if length else 0
    acidic_basic_ratio = (counts["acidic"] + 1) / (counts["basic"] + 1)
    return {
        "record": name,
        "source_file": str(source).replace("\\", "/"),
        "length": str(length),
        "hydrophobic_frac": f"{hydrophobic_frac:.3f}",
        "acidic_basic_ratio": f"{acidic_basic_ratio:.3f}",
        "acidic_fraction": f"{counts['acidic'] / length:.3f}",
        "basic_fraction": f"{counts['basic'] / length:.3f}",
    }


def summarize(input_dirs: List[Path], tsv_path: Path, md_path: Path) -> None:
    rows: List[Dict[str, str]] = []
    for directory in input_dirs:
        for fasta_path in sorted(directory.glob("*.fasta")):
            for record in read_fasta(fasta_path):
                metrics = compute_metrics(record["header"], record["sequence"], fasta_path)
                rows.append(metrics)
    if not rows:
        raise SystemExit("No FASTA records found. Ensure input directories contain .fasta files.")
    tsv_path.parent.mkdir(parents=True, exist_ok=True)
    with tsv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    header = "| record | length | hydrophobic_frac | acidic_fraction | basic_fraction | acidic_basic_ratio | source_file |\n"
    separator = "| --- | ---: | ---: | ---: | ---: | ---: | --- |\n"
    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# Sequence Metrics\n\n")
        handle.write(header)
        handle.write(separator)
        for row in rows:
            handle.write(
                f"| {row['record']} | {row['length']} | {row['hydrophobic_frac']} | {row['acidic_fraction']} | {row['basic_fraction']} | {row['acidic_basic_ratio']} | {row['source_file']} |\n"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize FASTA sequences across raw directories")
    parser.add_argument("--input-dirs", nargs="+", default=["data/raw/uniprot", "data/raw/secret_sequences"], help="Directories containing FASTA files")
    parser.add_argument("--tsv", default="data/processed/sequence_summary.tsv", help="Path to TSV output")
    parser.add_argument("--markdown", default="reports/sequence_summary.md", help="Path to Markdown summary")
    args = parser.parse_args()
    dirs = [Path(p) for p in args.input_dirs]
    summarize(dirs, Path(args.tsv), Path(args.markdown))


if __name__ == "__main__":
    main()
