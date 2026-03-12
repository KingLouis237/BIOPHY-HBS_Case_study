import argparse
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
from Bio.Align import substitution_matrices

matrix = substitution_matrices.load("BLOSUM62")


def read_fasta(path: Path) -> Dict[str, str]:
    records: Dict[str, str] = {}
    header = None
    seq_lines: List[str] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header is not None:
                records[header] = "".join(seq_lines)
            header = line[1:].strip()
            seq_lines = []
        else:
            seq_lines.append(line)
    if header is not None:
        records[header] = "".join(seq_lines)
    return records


def slide_scores(seq_a: str, seq_b: str, word: int, threshold: int) -> Tuple[List[int], List[int]]:
    xs, ys = [], []
    for i in range(len(seq_a) - word + 1):
        for j in range(len(seq_b) - word + 1):
            score = 0
            for k in range(word):
                aa = seq_a[i + k]
                bb = seq_b[j + k]
                try:
                    score += matrix[aa, bb]
                except KeyError:
                    score -= 4
            if score >= threshold:
                xs.append(j)
                ys.append(i)
    return xs, ys


def plot_panel(seq_a: str, seq_b: str, params: List[Tuple[int, int]], title: str, outfile: Path) -> None:
    fig, axes = plt.subplots(1, len(params), figsize=(5 * len(params), 4), constrained_layout=True)
    if len(params) == 1:
        axes = [axes]
    for ax, (word, threshold) in zip(axes, params):
        xs, ys = slide_scores(seq_a, seq_b, word, threshold)
        ax.scatter(xs, ys, s=5, color="#1f77b4")
        ax.set_title(f"word={word}, threshold={threshold}")
        ax.set_xlabel("Sequence B position")
        ax.set_ylabel("Sequence A position")
        ax.set_xlim(0, len(seq_b))
        ax.set_ylim(len(seq_a), 0)
    fig.suptitle(title)
    outfile.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outfile, dpi=300)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate dotplot figures for calibration and hemoglobin sequences")
    parser.add_argument("--secret-fasta", default="data/raw/secret_sequences/hemoglobin_secret_sequences.fasta")
    parser.add_argument("--uniprot-dir", default="data/raw/uniprot")
    parser.add_argument("--output-brca", default="figures/fig03_dotplots_brca1_53bp1.png")
    parser.add_argument("--output-hemo", default="figures/fig04_dotplots_hemoglobin.png")
    args = parser.parse_args()

    secret_records = read_fasta(Path(args.secret_fasta))
    brca = next(seq for header, seq in secret_records.items() if "brca1" in header.lower())
    t53 = next(seq for header, seq in secret_records.items() if "53bp1" in header.lower())
    secret_alpha = next(seq for header, seq in secret_records.items() if "secret - alpha" in header.lower())
    secret_beta = next(seq for header, seq in secret_records.items() if "secret - beta" in header.lower())

    uniprot_records = {}
    for fasta in Path(args.uniprot_dir).glob("*.fasta"):
        uniprot_records.update(read_fasta(fasta))
    hba_canonical = next(seq for header, seq in uniprot_records.items() if "HBA_HUMAN" in header)
    hbb_canonical = next(seq for header, seq in uniprot_records.items() if "HBB_HUMAN" in header)

    plot_panel(
        brca,
        t53,
        params=[(7, 20), (10, 30), (20, 50)],
        title="BRCA1 vs 53BP1 dotplots",
        outfile=Path(args.output_brca),
    )

    plot_panel(
        hba_canonical,
        secret_alpha,
        params=[(10, 30)],
        title="HBA canonical vs secret alpha",
        outfile=Path(args.output_hemo).with_name("fig04a_dotplot_hba_secret.png"),
    )

    plot_panel(
        hbb_canonical,
        secret_beta,
        params=[(10, 30)],
        title="HBB canonical vs secret beta",
        outfile=Path(args.output_hemo).with_name("fig04b_dotplot_hbb_secret.png"),
    )


if __name__ == "__main__":
    main()
