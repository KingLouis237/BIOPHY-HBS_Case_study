import argparse
import csv
from pathlib import Path
from typing import Dict, List, Tuple

from Bio import pairwise2
from Bio.Align import substitution_matrices

Matrix = substitution_matrices.load("BLOSUM62")

PAIR_DEFINITIONS: List[Tuple[str, str, str, str]] = [
    ("HBA_canonical", "data/raw/uniprot/P69905_HBA_HUMAN.fasta", "secret_alpha", "data/raw/secret_sequences/TP2_sequences.fasta"),
    ("HBB_canonical", "data/raw/uniprot/P68871_HBB_HUMAN.fasta", "secret_beta", "data/raw/secret_sequences/TP2_sequences.fasta"),
    ("BRCA1", "data/raw/secret_sequences/TP2_sequences.fasta", "53BP1", "data/raw/secret_sequences/TP2_sequences.fasta"),
]

HEADER_KEYS = {
    "HBA_canonical": "HBA_HUMAN",
    "HBB_canonical": "HBB_HUMAN",
    "secret_alpha": "Secret - alpha",
    "secret_beta": "Secret - beta",
    "BRCA1": "BRCA1",
    "53BP1": "53BP1",
}


def read_fasta(path: Path) -> Dict[str, str]:
    sequences: Dict[str, str] = {}
    header = None
    seq_lines: List[str] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header is not None:
                sequences[header] = "".join(seq_lines)
            header = line[1:].strip()
            seq_lines = []
        else:
            seq_lines.append(line)
    if header is not None:
        sequences[header] = "".join(seq_lines)
    return sequences


def match_sequence(records: Dict[str, str], keyword: str) -> Tuple[str, str]:
    for header, seq in records.items():
        if keyword in header:
            return header, seq
    raise KeyError(f"Keyword '{keyword}' not found in FASTA headers: {list(records.keys())}")



def summarize_alignment(name_a: str, seq_a: str, name_b: str, seq_b: str, output_dir: Path, label: str, gap_open: float, gap_extend: float) -> Dict[str, str]:
    alignments = pairwise2.align.globalds(seq_a, seq_b, Matrix, -gap_open, -gap_extend, penalize_end_gaps=False)
    best = alignments[0]
    aligned_a, aligned_b, score, start, end = best
    aln_path = output_dir / f"{label}.txt"
    output_dir.mkdir(parents=True, exist_ok=True)
    with aln_path.open("w", encoding="utf-8") as handle:
        handle.write(pairwise2.format_alignment(*best))
    matches = sum(aa == bb for aa, bb in zip(aligned_a, aligned_b))
    length = len(aligned_a)
    identity = matches / length if length else 0
    gaps = sum(aa == "-" or bb == "-" for aa, bb in zip(aligned_a, aligned_b))
    diffs = [
        str(i + 1)
        for i, (aa, bb) in enumerate(zip(aligned_a, aligned_b))
        if aa != bb and aa != "-" and bb != "-"
    ]
    return {
        "comparison": label,
        "seq_a": name_a,
        "seq_b": name_b,
        "identity": f"{identity * 100:.2f}",
        "alignment_length": str(length),
        "score": f"{score:.1f}",
        "gap_positions": str(gaps),
        "mismatch_positions": ",".join(diffs) or "None",
        "alignment_file": str(aln_path).replace("\\", "/"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run pairwise alignments for canonical vs secret sequences")
    parser.add_argument("--gap-open", type=float, default=10.0)
    parser.add_argument("--gap-extend", type=float, default=0.5)
    parser.add_argument("--output-dir", default="data/processed/alignments")
    parser.add_argument("--summary", default="data/processed/alignment_summary.tsv")
    parser.add_argument("--markdown", default="reports/alignment_summary.md")
    args = parser.parse_args()

    records_cache: Dict[Path, Dict[str, str]] = {}
    summary_rows: List[Dict[str, str]] = []
    output_dir = Path(args.output_dir)

    for label_prefix, path_a, label_suffix, path_b in PAIR_DEFINITIONS:
        fasta_a = Path(path_a)
        fasta_b = Path(path_b)
        if fasta_a not in records_cache:
            records_cache[fasta_a] = read_fasta(fasta_a)
        if fasta_b not in records_cache:
            records_cache[fasta_b] = read_fasta(fasta_b)
        header_a, seq_a = match_sequence(records_cache[fasta_a], HEADER_KEYS[label_prefix])
        header_b, seq_b = match_sequence(records_cache[fasta_b], HEADER_KEYS[label_suffix])
        comparison_label = f"{label_prefix}_vs_{label_suffix}"
        metrics = summarize_alignment(header_a, seq_a, header_b, seq_b, output_dir, comparison_label, args.gap_open, args.gap_extend)
        summary_rows.append(metrics)

    summary_path = Path(args.summary)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(summary_rows[0].keys())
    with summary_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    md_path = Path(args.markdown)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# Alignment Summary\n\n")
        header = "| comparison | identity (%) | alignment_length | score | gap_positions | mismatch_positions | alignment_file |\n"
        handle.write(header)
        handle.write("| --- | ---: | ---: | ---: | ---: | --- | --- |\n")
        for row in summary_rows:
            handle.write(
                f"| {row['comparison']} | {row['identity']} | {row['alignment_length']} | {row['score']} | {row['gap_positions']} | {row['mismatch_positions']} | {row['alignment_file']} |\n"
            )


if __name__ == "__main__":
    main()
