import sys
from pathlib import Path
from pypdf import PdfReader

if len(sys.argv) < 2:
    print('Usage: python extract_pdf.py <pdf_path>', file=sys.stderr)
    sys.exit(1)

path = Path(sys.argv[1])
reader = PdfReader(str(path))
for i, page in enumerate(reader.pages, 1):
    print(f"--- PAGE {i} ---")
    text = page.extract_text() or "[NO TEXT FOUND]"
    safe_text = text.encode('ascii', 'replace').decode('ascii')
    print(safe_text)