from docx import Document
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
res = root / 'resources'

def load(path: Path) -> str:
    d = Document(str(path))
    parts = []
    for p in d.paragraphs:
        t = p.text.strip()
        if t:
            parts.append(t)
    return "\n\n".join(parts)

files = {
    'about': res / 'Reviewed - first data file_ENG.docx',
    'mission_vision': res / 'Reviwed - Mission and vision Statement 1.docx',
}

out = {}
for key, path in files.items():
    if path.exists():
        out[key] = load(path)
    else:
        out[key] = None

print(json.dumps(out, ensure_ascii=False, indent=2))
