import argparse
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List

from Bio.Blast import NCBIWWW, NCBIXML


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Run BLASTP (local if available, otherwise remote/cached) for the secret beta sequence")
    parser.add_argument("--secrets", default="data/raw/secret_sequences/TP2_sequences.fasta", help="FASTA containing secret sequences")
    parser.add_argument("--target-header", default="Secret - beta", help="Header keyword to extract")
    parser.add_argument("--workdir", default="data/processed/blast", help="Directory for BLAST inputs/outputs")
    parser.add_argument("--db", default="swissprot", help="BLAST database name")
    parser.add_argument("--taxids", default="9606", help="NCBI taxids filter")
    parser.add_argument("--outfmt", default="5", help="NCBI BLAST output format")
    parser.add_argument("--max-target-seqs", default="5")
    parser.add_argument("--evalue", default="1e-20")
    parser.add_argument("--offline", action="store_true", help="Use cached BLAST XML and skip local/remote BLAST.")
    args = parser.parse_args()

    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    fasta_records = read_fasta(Path(args.secrets))
    query_sequence = None
    for header, seq in fasta_records.items():
        if args.target_header.lower() in header.lower():
            query_sequence = (header, seq)
            break
    if query_sequence is None:
        raise SystemExit(f"Could not find header containing '{args.target_header}' in {args.secrets}")

    query_path = workdir / "secret_beta_query.fasta"
    with query_path.open("w", encoding="utf-8") as handle:
        handle.write(f">{query_sequence[0]}\n")
        for i in range(0, len(query_sequence[1]), 70):
            handle.write(query_sequence[1][i : i + 70] + "\n")

    out_path = workdir / "secret_beta_blast.xml"
    cached_xml = Path("data/raw/reference/blast/secret_beta_blast_cached.xml")
    command = [
        "blastp",
        "-query",
        str(query_path),
        "-db",
        args.db,
        "-taxids",
        args.taxids,
        "-outfmt",
        args.outfmt,
        "-max_target_seqs",
        args.max_target_seqs,
        "-evalue",
        args.evalue,
        "-out",
        str(out_path),
    ]
    command_pretty = " ".join(command).replace("\\", "/")

    protocol_path = Path("reports/blast_protocol.md")
    protocol_path.parent.mkdir(parents=True, exist_ok=True)
    with protocol_path.open("w", encoding="utf-8") as handle:
        handle.write("# BLAST Workflow\n\n")
        handle.write("~~~\n" + command_pretty + "\n~~~\n\n")
        handle.write("- Requires NCBI BLAST+ to be installed locally or available in the PATH.\n")
        handle.write("- Restricts the search to Homo sapiens (taxid 9606).\n")
        handle.write("- Expect top hits corresponding to hemoglobin beta variants (e.g., Hb Monza, HbS).\n")
        handle.write("- Copy the resulting XML/Tabular output into data/processed/blast/ for version control.\n")

    if args.offline:
        copy_cached_xml(cached_xml, out_path, "offline mode requested")
    else:
        blastp_exe = shutil.which("blastp")
        if blastp_exe:
            subprocess.run(command, check=True)
            print(f"Local BLAST output written to {out_path}")
        else:
            print("blastp executable not found; falling back to NCBIWWW.qblast (remote BLAST).")
            try:
                result_handle = NCBIWWW.qblast(
                    program="blastp",
                    database=args.db,
                    sequence=query_sequence[1],
                    hitlist_size=int(args.max_target_seqs),
                    expect=float(args.evalue),
                    entrez_query=f"txid{args.taxids}[ORGN]" if args.taxids else None,
                )
            except Exception as exc:
                copy_cached_xml(cached_xml, out_path, f"remote BLAST failed ({exc})")
            else:
                out_path.write_text(result_handle.read())
                print(f"Remote BLAST output written to {out_path}")

    summary_path = Path("reports/blast_summary.md")
    create_summary(out_path, summary_path)
    print(f"BLAST summary written to {summary_path}")


def create_summary(xml_path: Path, summary_path: Path, top_n: int = 3) -> None:
    with xml_path.open() as handle:
        blast_record = next(NCBIXML.parse(handle))
    rows = []
    for alignment in blast_record.alignments[:top_n]:
        hsp = alignment.hsps[0]
        identity_pct = (hsp.identities / hsp.align_length) * 100 if hsp.align_length else 0
        rows.append(
            {
                "hit": alignment.hit_def.split("|")[-1].strip(),
                "length": alignment.length,
                "evalue": f"{hsp.expect:.2e}",
                "identity_pct": f"{identity_pct:.2f}",
                "accession": alignment.accession,
            }
        )

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with summary_path.open("w", encoding="utf-8") as handle:
        handle.write("# BLAST Summary\n\n")
        handle.write(f"Parsed from `{xml_path.as_posix()}`\n\n")
        if not rows:
            handle.write("No BLAST hits were returned.\n")
            return
        handle.write("| rank | accession | description | length | identity (%) | e-value |\n")
        handle.write("| ---: | --- | --- | ---: | ---: | ---: |\n")
        for idx, row in enumerate(rows, start=1):
            handle.write(
                f"| {idx} | {row['accession']} | {row['hit']} | {row['length']} | {row['identity_pct']} | {row['evalue']} |\n"
            )


def copy_cached_xml(cached_xml: Path, out_path: Path, reason: str) -> None:
    if not cached_xml.exists():
        raise SystemExit(f"{reason}; cached XML missing at {cached_xml}")
    shutil.copyfile(cached_xml, out_path)
    print(f"{reason.capitalize()}: cached result copied from {cached_xml}.")


if __name__ == "__main__":
    main()
