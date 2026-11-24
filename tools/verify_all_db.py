#!/usr/bin/env python3
"""
Verify the entire AQA Physics static database:
- JSON validity for questions.json, cheatsheets.json, flashcards.json, quiz_questions.json
- Every question has a non-empty image file and markscheme file on disk
- Every figure path in figures[] is a string and exists on disk with non-zero size
- Sum of question marks per paper equals paper.totalMarks
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_json(name: str):
    path = ROOT / name
    if not path.exists():
        raise FileNotFoundError(f"Missing {name}")
    return json.loads(path.read_text(encoding="utf-8"))


def check_image(rel_path: object, label: str, errors: list[str]) -> None:
    if not isinstance(rel_path, str) or not rel_path.strip():
        errors.append(f"Invalid {label} path (must be non-empty string): {rel_path!r}")
        return
    p = ROOT / rel_path
    if not p.exists():
        errors.append(f"Missing {label} file: {rel_path}")
        return
    if p.stat().st_size == 0:
        errors.append(f"Empty {label} file: {rel_path}")
        return
    try:
        from PIL import Image
        with Image.open(p) as im:
            w, h = im.size
            if w <= 0 or h <= 0:
                errors.append(f"Zero-dimension {label}: {rel_path}")
    except ImportError:
        pass


def main() -> int:
    errors: list[str] = []

    db = load_json("questions.json")
    cs = load_json("cheatsheets.json")
    fc = load_json("flashcards.json")
    qq = load_json("quiz_questions.json")

    for key in ("topics", "skills", "levels", "papers", "questions"):
        if key not in db:
            errors.append(f"questions.json missing key: {key}")

    topic_ids = {t["id"] for t in db.get("topics", [])}
    for tid in topic_ids:
        if tid not in cs:
            errors.append(f"cheatsheets.json missing topic: {tid}")

    if not isinstance(fc, list) or not fc:
        errors.append("flashcards.json must be a non-empty list")

    if not isinstance(qq, list) or not qq:
        errors.append("quiz_questions.json must be a non-empty list")
    else:
        missing_qq = topic_ids - {q["topic"] for q in qq}
        if missing_qq:
            errors.append(f"quiz_questions.json missing topics: {sorted(missing_qq)}")

    paper_totals = {p["id"]: int(p["totalMarks"]) for p in db.get("papers", [])}
    paper_sums: dict[str, int] = {pid: 0 for pid in paper_totals}

    for q in db.get("questions", []):
        qid = q.get("id", "<unknown>")
        pid = q.get("paper", "")
        if pid not in paper_totals:
            errors.append(f"Question {qid} references unknown paper: {pid}")
        else:
            paper_sums[pid] += int(q.get("marks", 0))

        check_image(q.get("image"), f"question image ({qid})", errors)
        check_image(q.get("markscheme"), f"markscheme ({qid})", errors)

        figs = q.get("figures", [])
        if not isinstance(figs, list):
            errors.append(f"Question {qid} figures must be a list")
        else:
            for fig in figs:
                check_image(fig, f"figure ({qid})", errors)

    for pid, expected in paper_totals.items():
        if paper_sums[pid] != expected:
            errors.append(f"Paper {pid} mark sum {paper_sums[pid]} != totalMarks {expected}")

    if errors:
        print("VERIFICATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(
        f"VERIFIED: {len(db['topics'])} topics, {len(db['papers'])} papers, "
        f"{len(db['questions'])} questions, {len(cs)} cheatsheets, "
        f"{len(fc)} flashcards, {len(qq)} quiz questions."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
