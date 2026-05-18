# -*- coding: utf-8 -*-
"""اسکریپت ۴۶ — اصلاح خط اول فایل‌های .jsx که با \\n literal خراب شده."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "frontend" / "src"

fixed = 0
for jsx in SRC.rglob("*.jsx"):
    content = jsx.read_text(encoding="utf-8")
    bad = "import React from 'react';\\\\nimport"
    if bad in content:
        content = content.replace(bad, "import React from 'react';\\nimport")
        jsx.write_text(content, encoding="utf-8")
        fixed += 1
        print(f"  fixed: {jsx.relative_to(ROOT)}")

print(f"\\nDone. Fixed {fixed} files.")
