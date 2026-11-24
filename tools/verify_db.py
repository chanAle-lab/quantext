#!/usr/bin/env python3
"""
Validate questions.json, cheatsheets.json, flashcards.json, and quiz_questions.json:
- JSON syntax & required top-level keys
- sum(q.marks) == paper.totalMarks for every paper
- Every image, figures[], and markscheme path exists on disk with non-zero dimensions
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_json(name: str):
    path = ROOT / name
    if not path.exists():
        raise FileNotFoundError(f"Missing {name}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_image(rel_path: str, errors: list[str]) -> None:
    p = ROOT / rel_path
    if not p.exists():
        errors.append(f"Missing image: {rel_path}")
        return
    if p.stat().st_size == 0:
        errors.append(f"Empty image file: {rel_path}")
        return
    try:
        from PIL import Image
        with Image.open(p) as im:
            w, h = im.size
            if w <= 0 or h <= 0:
                errors.append(f"Zero-dimension image: {rel_path}")
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

    if not isinstance(fc, list) or len(fc) == 0:
        errors.append("flashcards.json must be a non-empty list")

    if not isinstance(qq, list) or len(qq) == 0:
        errors.append("quiz_questions.json must be a non-empty list")
    else:
        qq_topics = {q["topic"] for q in qq}
        missing_qq = topic_ids - qq_topics
        if missing_qq:
            errors.append(f"quiz_questions.json missing topics: {sorted(missing_qq)}")

    paper_totals = {p["id"]: p["totalMarks"] for p in db.get("papers", [])}
    paper_sums: dict[str, int] = {pid: 0 for pid in paper_totals}

    for q in db.get("questions", []):
        pid = q.get("paper", "")
        if pid not in paper_totals:
            errors.append(f"Question {q.get('id')} references unknown paper: {pid}")
        else:
            paper_sums[pid] += int(q.get("marks", 0))

        if q.get("image"):
            check_image(q["image"], errors)
        if q.get("markscheme"):
            check_image(q["markscheme"], errors)
        for fig in q.get("figures", []):
            check_image(fig, errors)

    for pid, expected in paper_totals.items():
        if paper_sums[pid] != expected:
            errors.append(f"Paper {pid} mark sum {paper_sums[pid]} != totalMarks {expected}")

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(
        f"OK: {len(db['topics'])} topics, {len(db['papers'])} papers, "
        f"{len(db['questions'])} questions, {len(cs)} cheatsheets, "
        f"{len(fc)} flashcards, {len(qq)} quiz questions."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
