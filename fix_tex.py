#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exact-match find & replace in a LaTeX file (body only).
- For each (wrong -> right) pair, search exact substring occurrences in the body.
- Replace all occurrences.
- Print a per-rule match count report.

Usage:
  python3 exact_fix_tex.py diff.tex
  python3 exact_fix_tex.py diff.tex --inplace
"""

from __future__ import annotations
import argparse
from pathlib import Path

# -------------------------
# Hardcoded exact mappings
# -------------------------
RULES: list[tuple[str, str]] = [
    (r"\cmidrule\DIFaddFL{(l)}{\DIFaddFL{2-9}}",
     r"\cmidrule[\cmidrulewidth](l){2-9}"),

    # NOTE: your "wrong" example has a trailing space in the message.
    # We include both variants to be safe while still "exact match".
    (r"\cmidrule\DIFaddFL{(l)}{\DIFaddFL{2-15}} ",
     r"\cmidrule[\cmidrulewidth](lr){2-15}"),
    (r"\cmidrule\DIFaddFL{(l)}{\DIFaddFL{2-15}}",
     r"\cmidrule[\cmidrulewidth](lr){2-15}"),

    (r"\cmidrule\DIFaddFL{(lr)}{\DIFaddFL{2-3}}",
     r"\cmidrule[\cmidrulewidth](lr){2-3}"),
    (r"\cmidrule\DIFaddFL{(lr)}{\DIFaddFL{4-5}}",
     r"\cmidrule[\cmidrulewidth](lr){4-5}"),
    (r"\cmidrule\DIFaddFL{(lr)}{\DIFaddFL{6-7}}",
     r"\cmidrule[\cmidrulewidth](lr){6-7}"),
    (r"\cmidrule\DIFaddFL{(l)}{\DIFaddFL{4-15}}",
     r"\cmidrule[\cmidrulewidth](l){4-15}"),

    (r"\DIFadd{ida_pro}", r"ida_pro"),
    (r"\DIFadd{vs}", r"vs"),
    (r"\DIFadd{dong2022did}", r"dong2022did"),
    (r"\DIFadd{duan2018things}", r"duan2018things"),
    (r"\DIFadd{grace2012riskranker}", r"grace2012riskranker"),
    (r"\DIFadd{souri2018state}", r"souri2018state"),
    (r"\DIFadd{sun2011pathsim}", r"sun2011pathsim"),
    (r"\DIFadd{zhou2012dissecting}", r"zhou2012dissecting"),

    # Exact 2-line block (keep the newline + spaces exactly!)
    (
        "\\DIFdelend \\DIFaddbegin \\bibitem[Le and Mikolov(2014)]\\DIFaddend %\n"
        "        {\\DIFdelbegin \\DIFdel{lei2019evedroid}\\DIFdelend \\DIFaddbegin \\DIFadd{le2014distributed}\\DIFaddend }",
        "\\bibitem[Le and Mikolov(2014)]{le2014distributed}",
    ),
]

BEGIN_DOC = r"\begin{document}"

def split_tex(tex: str) -> tuple[str, str]:
    """Return (preamble_including_begin_document, body_after_begin_document)."""
    idx = tex.find(BEGIN_DOC)
    if idx == -1:
        return tex, ""
    cut = idx + len(BEGIN_DOC)
    return tex[:cut], tex[cut:]

def apply_rules_exact(body: str) -> tuple[str, list[int]]:
    """
    Apply exact substring replacements over the body.
    Returns (new_body, counts_per_rule).
    """
    counts: list[int] = []
    new_body = body
    for wrong, right in RULES:
        c = new_body.count(wrong)
        if c:
            new_body = new_body.replace(wrong, right)
        counts.append(c)
    return new_body, counts

def main() -> None:
    ap = argparse.ArgumentParser(description="Exact-match fix for latexdiff-broken diff.tex (body only).")
    ap.add_argument("tex_file", help="Path to the .tex file to fix")
    ap.add_argument("--inplace", action="store_true", help="Overwrite input file (creates .bak backup)")
    ap.add_argument("--no-backup", action="store_true", help="No .bak when using --inplace")
    args = ap.parse_args()

    p = Path(args.tex_file)
    if not p.exists():
        raise SystemExit(f"File not found: {p}")

    tex = p.read_text(encoding="utf-8", errors="ignore")
    pre, body = split_tex(tex)

    if body == "":
        raise SystemExit(f"Did not find '{BEGIN_DOC}' in {p}. Refusing to modify (safety).")

    fixed_body, counts = apply_rules_exact(body)
    fixed = pre + fixed_body

    # Report
    total = sum(counts)
    print(f"[report] total replacements: {total}")
    for i, ((wrong, right), c) in enumerate(zip(RULES, counts), start=1):
        status = "OK" if c > 0 else "MISS"
        # Print a short preview of the wrong pattern (single line)
        preview = wrong.replace("\n", "\\n")
        if len(preview) > 100:
            preview = preview[:100] + "..."
        print(f"  {i:02d}. {status}  matches={c}  wrong='{preview}'")

    if args.inplace:
        if fixed != tex:
            if not args.no_backup:
                bak = p.with_suffix(p.suffix + ".bak")
                bak.write_text(tex, encoding="utf-8")
                print(f"[backup] {bak}")
            p.write_text(fixed, encoding="utf-8")
            print(f"[fixed ] wrote in-place: {p}")
        else:
            print("[ok    ] no changes made")
    else:
        out = p.with_suffix(".fixed.tex")
        out.write_text(fixed, encoding="utf-8")
        print(f"[wrote ] {out}")

if __name__ == "__main__":
    main()