#!/usr/bin/env python3
"""
Shared Question Paper (QP) cropper for AQA Physics (7407 / 7408).
Reads `questions.json` and crops each question from its registered QP PDF in `PDF_MAP`
into `img/<paper-id>/q<slug>.jpg`, stripping page headers, footers, and 'Turn over'.

Register each paper PDF in PDF_MAP before running:
    PDF_MAP = {
        "2023-june-7408-1": "raw_pdfs/AQA-74081-QP-JUN23.pdf",
    }
"""

from __future__ import annotations

import json
import re
from pathlib import Path
import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_JSON = ROOT / "questions.json"

# Register <paper-id>: <path-to-qp-pdf> here
PDF_MAP: dict[str, str] = {
    "2016-june-7407-1": "raw_pdfs/media_1795606549697_d45dbf3f.pdf",
    "2016-june-7407-2": "raw_pdfs/media_1795606549721_5edd2400.pdf",
}


def find_marker_y(page: fitz.Page, qnum: str) -> float | None:
    """Locate the Y coordinate of the AQA question number box/marker on a page."""
    target_compact = re.sub(r"\s+", "", str(qnum))
    for b in page.get_text("blocks"):
        x0, y0, x1, y1, text = b[:5]
        if x0 > page.rect.width * 0.25:
            continue
        compact = re.sub(r"\s+", "", text)
        if compact.startswith(target_compact):
            return float(y0)
    return None


def recrop_all(dpi: int = 200) -> None:
    db = json.loads(QUESTIONS_JSON.read_text(encoding="utf-8"))
    by_paper: dict[str, list[dict]] = {}
    for q in db.get("questions", []):
        by_paper.setdefault(q["paper"], []).append(q)

    for paper_id, qs in by_paper.items():
        if paper_id not in PDF_MAP:
            print(f"[SKIP] {paper_id}: not registered in PDF_MAP")
            continue
        pdf_path = Path(PDF_MAP[paper_id])
        if not pdf_path.is_absolute():
            pdf_path = ROOT / pdf_path
        if not pdf_path.exists():
            print(f"[MISS] {paper_id}: PDF not found at {pdf_path}")
            continue

        doc = fitz.open(str(pdf_path))
        by_page: dict[int, list[dict]] = {}
        for q in qs:
            by_page.setdefault(int(q["page"]), []).append(q)

        for page_1idx, page_qs in sorted(by_page.items()):
            page = doc[page_1idx - 1]
            header_y = 58.0
            footer_y = page.rect.height - 52.0

            located = []
            for q in page_qs:
                qnum = q.get("questionNumber") or q.get("question")
                my = find_marker_y(page, qnum)
                located.append((my if my is not None else header_y, q))
            located.sort(key=lambda item: item[0])

            for idx, (y0, q) in enumerate(located):
                y1 = located[idx + 1][0] - 6.0 if idx + 1 < len(located) else footer_y
                if "crop_exclude_y" in q and q["crop_exclude_y"] is not None:
                    y1 = min(y1, float(q["crop_exclude_y"]))
                y0_clamped = max(header_y, y0 - 6.0)
                if y1 <= y0_clamped:
                    y1 = footer_y

                clip = fitz.Rect(32.0, y0_clamped, page.rect.width - 32.0, y1)
                pix = page.get_pixmap(dpi=dpi, clip=clip, alpha=False)
                out_file = ROOT / q["image"]
                out_file.parent.mkdir(parents=True, exist_ok=True)
                pix.save(str(out_file))
                print(f"[OK] {q['image']}")

        doc.close()


if __name__ == "__main__":
    recrop_all()
