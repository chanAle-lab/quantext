#!/usr/bin/env python3
"""
Coordinate-driven PDF extraction & cropping helpers for AQA Physics (7407 / 7408).
Uses PyMuPDF (fitz) for exact text-block & drawing-grid inspection and Pillow for
vertical stitching across page breaks.
"""

from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image


def stitch_vertical(image_paths: list[Path], out_path: Path) -> None:
    """Vertically stitch multiple cropped page fragments into one JPG."""
    imgs = [Image.open(p).convert("RGB") for p in image_paths]
    width = max(im.width for im in imgs)
    total_h = sum(im.height for im in imgs)
    canvas = Image.new("RGB", (width, total_h), (255, 255, 255))
    y = 0
    for im in imgs:
        canvas.paste(im, (0, y))
        y += im.height
        im.close()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, quality=92)


def detect_ms_horizontal_lines(page: fitz.Page, min_width_ratio: float = 0.6) -> list[float]:
    """Detect horizontal table grid lines in an AQA mark scheme PDF page."""
    min_w = page.rect.width * min_width_ratio
    ys: list[float] = []
    for d in page.get_drawings():
        rect = d.get("rect")
        if rect and rect.width >= min_w and rect.height <= 3.0:
            ys.append(round(rect.y0, 2))
    return sorted(set(ys))


def crop_region(
    page: fitz.Page,
    y0: float,
    y1: float,
    out_path: Path,
    left_m: float = 36.0,
    right_m: float = 36.0,
    dpi: int = 200,
) -> None:
    """Render a clipped PDF region to JPG, stripping examiner margins."""
    clip = fitz.Rect(left_m, y0, page.rect.width - right_m, y1)
    pix = page.get_pixmap(dpi=dpi, clip=clip, alpha=False)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(str(out_path))
