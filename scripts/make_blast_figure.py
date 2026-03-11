import argparse
from pathlib import Path
from textwrap import fill
from typing import List, Tuple

import matplotlib.pyplot as plt
from Bio.Blast import NCBIXML


def parse_hits(xml_path: Path, top_n: int) -> List[Tuple[str, float, float, str]]:
    with xml_path.open() as handle:
        record = next(NCBIXML.parse(handle))
    hits: List[Tuple[str, float, float, str]] = []
    for alignment in record.alignments[:top_n]:
        hsp = alignment.hsps[0]
        identity_pct = (hsp.identities / hsp.align_length) * 100 if hsp.align_length else 0.0
        evalue = hsp.expect
        description = alignment.hit_def.split("|")[-1].strip()
        hits.append((description, identity_pct, evalue, alignment.accession))
    return hits


def short_label(description: str, accession: str, width: int = 26) -> str:
    base = description.split(" OS=")[0].strip()
    base = base.replace("Hemoglobin subunit", "Hb")
    base = base.replace("Hemoglobin", "Hb")
    text = f"{accession} · {base}"
    return fill(text, width=width)


def plot_hits(hits: List[Tuple[str, float, float, str]], out_path: Path) -> None:
    if not hits:
        raise SystemExit("No BLAST hits found in XML file.")
    labels = [short_label(hit[0], hit[3]) for hit in hits]
    identities = [hit[1] for hit in hits]
    evalues = [hit[2] for hit in hits]
    fig_height = 1.6 + 0.8 * len(hits)
    fig, ax = plt.subplots(figsize=(8.6, fig_height))
    y_positions = list(range(len(hits)))
    bars = ax.barh(y_positions, identities, color="#1f77b4", height=0.55)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Identity (%)", labelpad=6)
    ax.set_title("Top BLASTP hits for secret beta sequence", fontsize=12, pad=12)
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    max_identity = max(identities)
    ax.set_xlim(0, max_identity + 15)
    text_x = max_identity + 3
    for bar, evalue in zip(bars, evalues):
        ax.text(
            text_x,
            bar.get_y() + bar.get_height() / 2,
            f"E={evalue:.1e}",
            va="center",
            ha="left",
            fontsize=9,
            color="#333333",
        )
    fig.subplots_adjust(left=0.32, right=0.92, top=0.9, bottom=0.08)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot BLAST hit identity percentages from XML output.")
    parser.add_argument("--xml", default="data/processed/blast/secret_beta_blast.xml")
    parser.add_argument("--top-n", type=int, default=5)
    parser.add_argument("--output", default="figures/fig07_blast_hits.png")
    args = parser.parse_args()

    xml_path = Path(args.xml)
    if not xml_path.exists():
        raise SystemExit(f"Missing BLAST XML at {xml_path}. Run scripts/run_blastp.py first.")
    hits = parse_hits(xml_path, args.top_n)
    plot_hits(hits, Path(args.output))


if __name__ == "__main__":
    main()
