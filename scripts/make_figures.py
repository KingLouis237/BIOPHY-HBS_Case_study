import csv
from pathlib import Path
from typing import List, Dict

import matplotlib.pyplot as plt
from Bio.Align import substitution_matrices

SUMMARY_PATH = Path("data/processed/sequence_summary.tsv")
OUT_DIR = Path("figures")


def load_sequence_summary(path: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    with path.open() as handle:
        reader = csv.DictReader(handle)
        rows.extend(reader)
    return rows


def short_label(record: str) -> str:
    lower = record.lower()
    if "brca1" in lower:
        return "BRCA1"
    if "53bp1" in lower:
        return "53BP1"
    if "secret - alpha" in lower:
        return "Secret alpha"
    if "secret - beta" in lower:
        return "Secret beta"
    if "hba_human" in lower:
        return "HBA canonical"
    if "hbb_human" in lower:
        return "HBB canonical"
    return record.split()[0]


def plot_sequence_characteristics(rows: List[Dict[str, str]], out_path: Path) -> None:
    labels = [short_label(row["record"]) for row in rows]
    lengths = [int(float(row["length"])) for row in rows]
    hydrophobic = [float(row["hydrophobic_frac"]) for row in rows]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4), constrained_layout=True)
    axes[0].bar(labels, lengths, color="#1f77b4")
    axes[0].set_ylabel("Length (aa)")
    axes[0].set_title("Sequence length comparison")
    axes[0].tick_params(axis="x", rotation=45)
    for label in axes[0].get_xticklabels():
        label.set_ha("right")

    axes[1].bar(labels, hydrophobic, color="#ff7f0e")
    axes[1].set_ylabel("Hydrophobic fraction")
    axes[1].set_ylim(0, 0.8)
    axes[1].set_title("Hydrophobic content")
    axes[1].tick_params(axis="x", rotation=45)
    for label in axes[1].get_xticklabels():
        label.set_ha("right")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def plot_blosum_penalty(out_path: Path) -> None:
    matrix = substitution_matrices.load("BLOSUM62")
    score_native = matrix["E", "E"]
    score_mut = matrix["E", "V"]
    labels = ["E->E\ncanonical", "E->V\nvariant"]
    scores = [score_native, score_mut]

    fig, ax = plt.subplots(figsize=(4.5, 4.2))
    colors = ["#2ca02c", "#d62728"]
    bars = ax.bar(labels, scores, color=colors, width=0.55)
    ax.set_ylabel("BLOSUM62 score")
    ax.set_ylim(min(scores) - 1.5, max(scores) + 1.5)
    ax.set_title("Penalty of beta6 substitution", fontsize=12, pad=8)
    ax.axhline(0, color="#888888", linewidth=0.8)
    ax.tick_params(axis="x", labelsize=10)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for idx, (bar, value) in enumerate(zip(bars, scores)):
        va = "bottom" if value >= 0 else "top"
        offset = 4 if value >= 0 else -6
        ax.annotate(
            f"{value}",
            xy=(bar.get_x() + bar.get_width() / 2, value),
            xytext=(0, offset),
            textcoords="offset points",
            ha="center",
            va=va,
            fontsize=11,
            fontweight="bold",
        )
    fig.tight_layout(pad=1.2)
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def main() -> None:
    rows = load_sequence_summary(SUMMARY_PATH)
    plot_sequence_characteristics(rows, OUT_DIR / "fig01_sequence_characteristics.png")
    plot_blosum_penalty(OUT_DIR / "fig06_blosum_penalty.png")


if __name__ == "__main__":
    main()
