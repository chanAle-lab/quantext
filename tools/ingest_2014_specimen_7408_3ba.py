#!/usr/bin/env python3
"""Ingest AQA A-level Physics Paper 3B Astrophysics (7408/3BA) Specimen 2014 into questions.json + img/2014-specimen-7408-3ba/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2014-specimen-7408-3ba"
QP_PDF = ROOT / "raw_pdfs" / "media_1795692434187_e425ccfa.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795692434201_8339708a.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2014,
    "series": "Specimen",
    "date": "2014-10-08",
    "code": "7408/3BA",
    "unit": "A-level Paper 3B (Astrophysics)",
    "level": "A",
    "spec": "current",
    "totalMarks": 35,
    "duration": "2 hours (total Paper 3)",
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-02-table2.jpg", "page": 6, "x0": 55, "y0": 75, "x1": 540, "y1": 285},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 2, "topic": "3.9", "skills": [], "figs": [], "summary": "Draw a ray diagram showing spherical aberration produced by a concave mirror."},
    {"qnum": "01.2", "page": 2, "marks": 6, "topic": "3.9", "skills": ["maths"], "figs": [], "summary": "Compare the IUE space telescope and GTC ground telescope in location, collecting power, and angular resolution."},
    {"qnum": "01.3", "page": 4, "marks": 2, "topic": "3.9", "skills": [], "figs": [], "summary": "Explain quantum efficiency and compare the quantum efficiency of a CCD with that of the human eye."},
    {"qnum": "02.1", "page": 6, "marks": 2, "topic": "3.9", "skills": [], "figs": ["fig-02-table2.jpg"], "summary": "State and explain which spectral class Altair, Deneb, and Vega belong to."},
    {"qnum": "02.2", "page": 6, "marks": 2, "topic": "3.9", "skills": [], "figs": ["fig-02-table2.jpg"], "summary": "Deduce which of the three Summer Triangle stars appears brightest from Earth."},
    {"qnum": "02.3", "page": 6, "marks": 3, "topic": "3.9", "skills": ["maths"], "figs": ["fig-02-table2.jpg"], "summary": "Calculate the distance in parsecs from Earth to the closest of the three stars."},
    {"qnum": "02.4", "page": 7, "marks": 3, "topic": "3.9", "skills": [], "figs": ["fig-02-table2.jpg"], "summary": "Deduce which of the three stars has the largest radius."},
    {"qnum": "02.5", "page": 7, "marks": 2, "topic": "3.9", "skills": ["maths"], "figs": ["fig-02-table2.jpg"], "summary": "Calculate the peak black-body radiation wavelength of Altair using Wien's law."},
    {"qnum": "03.1", "page": 8, "marks": 1, "topic": "3.9", "skills": [], "figs": [], "summary": "State what is meant by a supernova."},
    {"qnum": "03.2", "page": 8, "marks": 2, "topic": "3.9", "skills": [], "figs": [], "summary": "State the defining properties of a neutron star."},
    {"qnum": "03.3", "page": 8, "marks": 2, "topic": "3.9", "skills": ["maths"], "figs": [], "summary": "Calculate the Schwarzschild radius of a black hole with twice the mass of the Sun."},
    {"qnum": "03.4", "page": 8, "marks": 2, "topic": "3.9", "skills": [], "figs": [], "summary": "Explain why scientists are concerned about a nearby supernova occurring in our galaxy."},
    {"qnum": "04.1", "page": 9, "marks": 1, "topic": "3.9", "skills": [], "figs": [], "summary": "State one reason why it is difficult to directly observe an exoplanet orbiting a star in Pegasus."},
    {"qnum": "04.2", "page": 9, "marks": 2, "topic": "3.9", "skills": [], "figs": [], "summary": "Explain how an orbiting planet causes a Doppler shift in the spectrum of its host star."},
    {"qnum": "04.3", "page": 9, "marks": 3, "topic": "3.9", "skills": ["graph"], "figs": [], "summary": "Explain how a transiting planet changes a star's apparent magnitude and sketch its light curve."},
]


def main() -> None:
    assert sum(q["marks"] for q in QUESTIONS) == PAPER_META["totalMarks"]
    IMG_DIR.mkdir(parents=True, exist_ok=True)

    qp_doc = fitz.open(str(QP_PDF))
    mat = fitz.Matrix(2.5, 2.5)
    for fig in FIGURES:
        page = qp_doc[fig["page"] - 1]
        clip = fitz.Rect(fig["x0"], fig["y0"], fig["x1"], fig["y1"])
        pix = page.get_pixmap(clip=clip, matrix=mat, alpha=False)
        pix.save(str(IMG_DIR / fig["filename"]))
    qp_doc.close()

    qnums = [q["qnum"] for q in QUESTIONS]
    ms_written = crop_official_markschemes(MS_PDF, qnums, IMG_DIR / "ms")
    print(f"Cropped {len(ms_written)} / {len(qnums)} mark schemes for {PAPER_ID}")

    db_path = ROOT / "questions.json"
    db = json.loads(db_path.read_text(encoding="utf-8"))
    db["papers"] = [p for p in db["papers"] if p["id"] != PAPER_ID] + [PAPER_META]
    db["questions"] = [q for q in db["questions"] if q["paper"] != PAPER_ID]

    for q in QUESTIONS:
        slug = q["qnum"].replace(".", "-")
        db["questions"].append({
            "id": f"{PAPER_ID}-q{q['qnum']}",
            "paper": PAPER_ID,
            "year": PAPER_META["year"],
            "series": PAPER_META["series"],
            "unit": PAPER_META["unit"],
            "level": PAPER_META["level"],
            "question": q["qnum"],
            "questionNumber": q["qnum"],
            "page": q["page"],
            "marks": q["marks"],
            "specRef": q["topic"],
            "topics": [q["topic"]],
            "skills": q["skills"],
            "summary": q["summary"],
            "image": f"img/{PAPER_ID}/q{slug}.jpg",
            "figures": [f"img/{PAPER_ID}/{f}" for f in q["figs"]],
            "markscheme": f"img/{PAPER_ID}/ms/q{slug}.png",
        })

    db_path.write_text(json.dumps(db, indent=2) + "\n", encoding="utf-8")
    print(f"Updated questions.json with {len(QUESTIONS)} questions for {PAPER_ID}")


if __name__ == "__main__":
    main()
