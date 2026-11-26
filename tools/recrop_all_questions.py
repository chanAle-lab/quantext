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
    "2017-june-7408-3a": "raw_pdfs/media_1795607555737_bf406981.pdf",
    "2017-june-7407-1": "raw_pdfs/media_1795607555778_3a6c257e.pdf",
    "2017-june-7407-2": "raw_pdfs/media_1795607555734_c7e434c2.pdf",
    "2018-june-7408-3a": "raw_pdfs/media_1795609285683_5b76cf6a.pdf",
    "2018-june-7408-2": "raw_pdfs/media_1795609285686_41750593.pdf",
    "2018-june-7407-1": "raw_pdfs/media_1795609950295_a9b24638.pdf",
    "2018-june-7407-2": "raw_pdfs/media_1795609950291_8c9267fb.pdf",
    "2014-specimen-7408-1": "raw_pdfs/media_1795692434197_e730130f.pdf",
    "2014-specimen-7408-2": "raw_pdfs/media_1795692434151_d4f743aa.pdf",
    "2014-specimen-7408-3ba": "raw_pdfs/media_1795692434187_e425ccfa.pdf",
    "2014-specimen-7408-3a": "raw_pdfs/media_1795692434176_4a52e830.pdf",
    "2016-specimen2-7408-1": "raw_pdfs/media_1795693078614_5ec19d19.pdf",
    "2016-specimen2-7408-2": "raw_pdfs/media_1795693078604_d416da95.pdf",
    "2016-specimen2-7408-3ba": "raw_pdfs/media_1795693078603_f96f5f7b.pdf",
    "2016-specimen2-7408-3a": "raw_pdfs/media_1795693078635_ef734b46.pdf",
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


def trim_redundant_answer_lines(page: fitz.Page, y0: float, y1: float) -> float:
    """
    Trim trailing blank space, redundant empty student answer lines, and
    'Extra space is available...' notices from the bottom of a question crop,
    while preserving any diagrams, tables, mark brackets, or labelled answer prompts.
    """
    last_y = y0
    # 1. Keep all meaningful text (excluding blank/underscore rules, 'Extra space...', 'Turn over')
    for b in page.get_text("blocks"):
        bx0, by0, bx1, by1, text = b[:5]
        if by1 <= y0 or by0 >= y1:
            continue
        clean = re.sub(r"\s+", " ", text).strip()
        if not clean or re.fullmatch(r"[_\.\-—–\s]+", clean):
            continue
        low = clean.lower()
        if "extra space is available" in low or "turn over" in low or "end of questions" in low:
            continue
        last_y = max(last_y, float(by1))

    # 2. Keep any drawings/diagrams/tables (excluding page frame borders and answer rules)
    full_line_w = page.rect.width * 0.55
    for d in page.get_drawings():
        r = d.get("rect")
        if not r or r.y1 <= y0 or r.y0 >= y1:
            continue
        is_page_frame = r.width > page.rect.width * 0.75 or r.height > page.rect.height * 0.45
        is_answer_rule = r.width >= full_line_w and r.height <= 3.5
        if not is_page_frame and not is_answer_rule:
            last_y = max(last_y, float(r.y1))

    # 3. Keep any raster images inside the question region
    for img in page.get_image_info():
        r = fitz.Rect(img["bbox"])
        if r.y1 > y0 and r.y0 < y1:
            last_y = max(last_y, float(r.y1))

    if last_y > y0 + 10.0:
        return min(y1, last_y + 12.0)
    return y1


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
            footer_y = page.rect.height - 62.0

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
                y1 = trim_redundant_answer_lines(page, y0_clamped, y1)

                clip = fitz.Rect(32.0, y0_clamped, page.rect.width - 32.0, y1)
                pix = page.get_pixmap(dpi=dpi, clip=clip, alpha=False)
                out_file = ROOT / q["image"]
                out_file.parent.mkdir(parents=True, exist_ok=True)
                pix.save(str(out_file))
                print(f"[OK] {q['image']}")

        doc.close()


if __name__ == "__main__":
    recrop_all()
