# -*- coding: utf-8 -*-
"""اسکریپت ۴۵ — افزودن import React به همه فایل‌های .jsx که ندارند."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "frontend" / "src"

fixed, skipped = 0, 0
for jsx in SRC.rglob("*.jsx"):
    content = jsx.read_text(encoding="utf-8")
    if "import React" in content.split("\\n")[0] or "import React" in content[:200]:
        skipped += 1
        continue
    jsx.write_text("import React from 'react';\\n" + content, encoding="utf-8")
    fixed += 1
    print(f"  + {jsx.relative_to(ROOT)}")

print(f"\\n✅ Done. Fixed: {fixed}, Already had import: {skipped}")
