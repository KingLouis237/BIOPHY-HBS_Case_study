import argparse
from pathlib import Path
from fpdf import FPDF

REPLACEMENTS = {
    "\u03b2": "beta",
    "\u2192": "->",
    "\u2013": "-",
    "\u2014": "-",
    "\u03b1": "alpha",
    "\u0394": "Delta",
    "\u03bc": "mu"
}

def sanitize(line: str) -> str:
    text = line
    for src, dst in REPLACEMENTS.items():
        actual = src.encode("utf-8").decode("unicode_escape")
        text = text.replace(actual, dst)
    return text.encode("ascii", "replace").decode("ascii")

def convert(md_path: Path, pdf_path: Path) -> None:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    for raw_line in md_path.read_text(encoding="utf-8").splitlines():
        line = sanitize(raw_line)
        if line.startswith("# "):
            pdf.set_font("Arial", "B", 14)
            pdf.multi_cell(0, 8, line[2:])
            pdf.set_font("Arial", size=11)
        elif line.startswith("## "):
            pdf.set_font("Arial", "B", 12)
            pdf.multi_cell(0, 7, line[3:])
            pdf.set_font("Arial", size=11)
        elif line.startswith("- ") or line.startswith("* "):
            pdf.multi_cell(0, 6, f"- {line[2:]}")
        elif line.strip() == "":
            pdf.ln(4)
        else:
            pdf.multi_cell(0, 6, line)
    pdf.output(str(pdf_path))

def main():
    parser = argparse.ArgumentParser(description="Convert markdown brief to PDF")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    convert(args.input, args.output)

if __name__ == "__main__":
    main()

