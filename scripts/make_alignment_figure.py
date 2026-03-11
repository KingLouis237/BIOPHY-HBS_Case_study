import argparse
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt


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


def chunk_seq(seq: str, size: int = 30) -> List[str]:
    return [seq[i : i + size] for i in range(0, len(seq), size)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot canonical vs secret beta alignment highlighting the E6V substitution")
    parser.add_argument("--uniprot", default="data/raw/uniprot/P68871_HBB_HUMAN.fasta")
    parser.add_argument("--secret", default="data/raw/secret_sequences/TP2_sequences.fasta")
    parser.add_argument("--target-header", default="Secret - beta")
    parser.add_argument("--output", default="figures/fig05_beta_variant_alignment.png")
    args = parser.parse_args()

    canonical = next(iter(read_fasta(Path(args.uniprot)).values()))
    secret_records = read_fasta(Path(args.secret))
    secret_seq = next(seq for header, seq in secret_records.items() if args.target_header.lower() in header.lower())

    assert len(canonical) == len(secret_seq), "Sequences should align without gaps"

    mismatch_positions = [i for i, (a, b) in enumerate(zip(canonical, secret_seq)) if a != b]
    chunks_a = chunk_seq(canonical)
    chunks_b = chunk_seq(secret_seq)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis("off")
    y = 0.9
    for idx, (chunk_a, chunk_b) in enumerate(zip(chunks_a, chunks_b)):
        start = idx * 30 + 1
        end = start + len(chunk_a) - 1
        ax.text(0.01, y, f"{start:03d}-{end:03d} Canonical", fontfamily="monospace", fontsize=10, color="#1f77b4")
        ax.text(0.25, y, chunk_a, fontfamily="monospace", fontsize=10, color="#1f77b4")
        y -= 0.045
        ax.text(0.01, y, f"{start:03d}-{end:03d} Secret", fontfamily="monospace", fontsize=10, color="#d62728")
        ax.text(0.25, y, chunk_b, fontfamily="monospace", fontsize=10, color="#d62728")
        y -= 0.06

    for pos in mismatch_positions:
        chunk_idx = pos // 30
        within_chunk = pos % 30
        y_base = 0.9 - chunk_idx * (0.045 * 2 + 0.06 * 0)
        y_canonical = 0.9 - chunk_idx * 0.105
        y_secret = y_canonical - 0.045
        x = 0.25 + within_chunk * (1 / 30) * 0.68
        ax.scatter([x], [y_secret + 0.005], color="#ff7f0e", zorder=5)
        ax.annotate(
            f"E{pos+1}V",
            xy=(x, y_secret + 0.005),
            xytext=(x + 0.05, y_secret + 0.05),
            arrowprops=dict(arrowstyle="->", color="#ff7f0e"),
            fontsize=10,
            color="#ff7f0e",
        )

    ax.set_title("Canonical HBB vs Secret Beta Alignment (E6V highlighted)")
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=300, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
