import glob
import os
from docx import Document

base = r"D:\Downloads"
files = glob.glob(os.path.join(base, "*TG16*.docx"))

def read_docx(path):
    doc = Document(path)
    lines = []
    for para in doc.paragraphs:
        t = para.text.strip()
        if t:
            lines.append(t)
    return "\n".join(lines)

for fpath in files:
    fname = os.path.basename(fpath)
    outpath = os.path.join(r"D:\tg-demo2", fname.replace(".docx", ".txt"))
    text = read_docx(fpath)
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"OK: {fname} -> {len(text)} chars")
