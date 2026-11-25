#!/usr/bin/env python3
"""
Crop official AQA Physics (7407 / 7408) Mark Scheme PDFs into per-question PNGs
under img/<paper-id>/ms/.

Features:
- Skips front-matter / Mark Scheme Instructions pages automatically (or via start_page)
  so specification numbers like 3.1, 3.2 are never mistaken for question numbers.
- Canonical question-number key matching (ignoring leading zeros, e.g. '09.1' == '9.1').
- Uses page.get_drawings() horizontal grid lines to bound each sub-question row.
- Vertically stitches multi-page / Levels-of-Response mark scheme rows into one PNG.
- Handles compact Section B MCQ answer tables near the end of Paper 1 / Paper 2.
"""

from __future__ import annotations

import re
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image


def canonical_qkey(qnum: str) -> str:
    """Normalize question labels so '09.1' == '9.1' and '05' == '5'."""
    parts = [p.lstrip("0") or "0" for p in str(qnum).strip().split(".")]
    return ".".join(parts)


def detect_horizontal_lines(page: fitz.Page, min_width_ratio: float = 0.45) -> list[float]:
    """Return sorted Y coordinates of horizontal table grid lines on a page."""
    min_w = page.rect.width * min_width_ratio
    rot = page.rotation_matrix
    by_y: dict[float, float] = {}
    for d in page.get_drawings():
        rect = d.get("rect")
        if rect:
            r = rect * rot
            if r.height <= 4.0 and r.width >= 30.0:
                y = round(r.y0, 1)
                by_y[y] = by_y.get(y, 0.0) + r.width
    return sorted(y for y, total_w in by_y.items() if total_w >= min_w)


def find_ms_start_page(doc: fitz.Document) -> int:
    """Find the 0-indexed page where the actual Question/Mark table begins."""
    for idx in range(len(doc)):
        txt = doc[idx].get_text("text")
        if "Question" in txt and ("Marking Guidance" in txt or "Answers" in txt or "Mark" in txt):
            if "Mark scheme instructions" not in txt.lower():
                return idx
    return min(2, len(doc) - 1)


def stitch_vertical_png(pixmaps: list[fitz.Pixmap], out_path: Path) -> None:
    """Vertically stitch one or more PyMuPDF pixmaps and save as PNG."""
    imgs = [Image.frombytes("RGB", [p.width, p.height], p.samples) for p in pixmaps]
    width = max(im.width for im in imgs)
    total_h = sum(im.height for im in imgs)
    canvas = Image.new("RGB", (width, total_h), (255, 255, 255))
    y = 0
    for im in imgs:
        canvas.paste(im, (0, y))
        y += im.height
        im.close()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, format="PNG", optimize=True)


def crop_official_markschemes(
    ms_pdf_path: str | Path,
    qnums: list[str],
    out_dir: str | Path,
    start_page: int | None = None,
    dpi: int = 200,
) -> dict[str, Path]:
    """
    Crop each question in `qnums` from `ms_pdf_path` into `out_dir/q<slug>.png`.
    Returns a mapping of canonical qnum -> output PNG Path.
    """
    doc = fitz.open(str(ms_pdf_path))
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    first_page = start_page if start_page is not None else find_ms_start_page(doc)
    wanted = {canonical_qkey(q): q for q in qnums}
    q_pattern = re.compile(r"^(\d{1,2}(?:\.\d{1,2})?)$")

    # Collect (page_idx, y0, y1, canonical_key) spans
    spans: list[tuple[int, float, float, str]] = []
    active_key: str | None = None

    for p_idx in range(first_page, len(doc)):
        page = doc[p_idx]
        rot = page.rotation_matrix
        lines = detect_horizontal_lines(page)
        words = page.get_text("words")
        markers: list[tuple[float, str]] = []
        seen_on_page: set[str] = set()

        for w in words:
            r = fitz.Rect(w[:4]) * rot
            token = w[4].strip()
            if r.x0 > page.rect.width * 0.20:
                continue
            m = q_pattern.match(token)
            if m:
                ck = canonical_qkey(m.group(1))
                if ck in wanted and ck not in seen_on_page:
                    markers.append((r.y0, ck))
                    seen_on_page.add(ck)

        markers.sort(key=lambda t: t[0])
        top_y = lines[0] if lines else 50.0
        bot_y = lines[-1] if lines else page.rect.height - 40.0

        if not markers and active_key:
            spans.append((p_idx, top_y, bot_y, active_key))
            continue

        if markers and active_key and markers[0][0] > top_y + 12:
            snap_end = max([y for y in lines if y <= markers[0][0]], default=markers[0][0] - 2)
            if snap_end > top_y:
                spans.append((p_idx, top_y, snap_end, active_key))

        for i, (my, ck) in enumerate(markers):
            row_start = max([y for y in lines if y <= my + 4], default=my - 8)
            if i + 1 < len(markers):
                next_my = markers[i + 1][0]
                row_end = max([y for y in lines if y <= next_my + 4], default=next_my - 4)
            else:
                below = [y for y in lines if y > my + 12]
                row_end = below[-1] if below else (page.rect.height - 40.0)
            if row_end > row_start:
                spans.append((p_idx, row_start, row_end, ck))
            active_key = ck

    grouped: dict[str, list[fitz.Pixmap]] = {}
    for p_idx, y0, y1, ck in spans:
        page = doc[p_idx]
        clip = fitz.Rect(24.0, max(0.0, y0 - 2), page.rect.width - 24.0, min(page.rect.height, y1 + 2))
        pix = page.get_pixmap(dpi=dpi, clip=clip, alpha=False)
        grouped.setdefault(ck, []).append(pix)

    written: dict[str, Path] = {}
    for ck, orig_q in wanted.items():
        if ck not in grouped:
            continue
        slug = orig_q.replace(".", "-")
        dest = out_path / f"q{slug}.png"
        stitch_vertical_png(grouped[ck], dest)
        written[ck] = dest

    doc.close()
    return written
