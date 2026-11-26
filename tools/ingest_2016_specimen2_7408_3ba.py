#!/usr/bin/env python3
"""Ingest AQA A-level Physics Paper 3BA Astrophysics (7408/3BA) Specimen Set 2 into questions.json + img/2016-specimen2-7408-3ba/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2016-specimen2-7408-3ba"
QP_PDF = ROOT / "raw_pdfs" / "media_1795693078603_f96f5f7b.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795693078621_19d13f56.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2016,
    "series": "Specimen Set 2",
    "date": "2016-06-01",
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
    {"filename": "fig-02-fig1.jpg", "page": 4, "x0": 120, "y0": 115, "x1": 555, "y1": 420},
    {"filename": "fig-02-table1.jpg", "page": 5, "x0": 115, "y0": 75, "x1": 540, "y1": 295},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 2, "topic": "3.9", "skills": [], "figs": [], "summary": "Draw a ray diagram for an astronomical refracting telescope in normal adjustment showing three non-axial rays and principal foci."},
    {"qnum": "01.2", "page": 2, "marks": 4, "topic": "3.9", "skills": [], "figs": [], "summary": "Discuss the principal optical advantages of reflecting telescopes over refracting telescopes."},
    {"qnum": "01.3", "page": 3, "marks": 6, "topic": "3.9", "skills": [], "figs": [], "summary": "Explain what is meant by apparent magnitude and describe the main features of the Hipparcos scale."},
    {"qnum": "02.1", "page": 4, "marks": 3, "topic": "3.9", "skills": ["graph"], "figs": [], "summary": "Sketch a Hertzsprung-Russell diagram on Figure 1 and label main sequence, white dwarf, and giant stars."},
    {"qnum": "02.2", "page": 4, "marks": 2, "topic": "3.9", "skills": ["graph"], "figs": ["fig-02-fig1.jpg"], "summary": "Label the minimum and maximum values on the scale of each axis in Figure 1."},
    {"qnum": "02.3", "page": 5, "marks": 1, "topic": "3.9", "skills": [], "figs": ["fig-02-table1.jpg"], "summary": "Identify the spectral class to which Rigel, Omicron 2 Eridani, and Regulus A all belong."},
    {"qnum": "02.4", "page": 5, "marks": 2, "topic": "3.9", "skills": [], "figs": ["fig-02-table1.jpg"], "summary": "Explain your choice of spectral class for the three stars in Table 1."},
    {"qnum": "02.5", "page": 6, "marks": 3, "topic": "3.9", "skills": ["maths"], "figs": ["fig-02-table1.jpg"], "summary": "Deduce which star in Table 1 is a white dwarf using distance and apparent magnitude."},
    {"qnum": "03.1", "page": 7, "marks": 1, "topic": "3.9", "skills": [], "figs": [], "summary": "State the likely cause of the 2013 gamma-ray burst detected between Leo and Ursa Major."},
    {"qnum": "03.2", "page": 7, "marks": 4, "topic": "3.9", "skills": ["maths"], "figs": [], "summary": "Calculate, ignoring relativistic effects, the distance in light years to an object with redshift z = 0.34."},
    {"qnum": "03.3", "page": 7, "marks": 2, "topic": "3.9", "skills": ["maths"], "figs": [], "summary": "Show that 10^47 J is similar to the energy released if the mass of the Sun were all converted to energy."},
    {"qnum": "04.1", "page": 8, "marks": 3, "topic": "3.9", "skills": [], "figs": [], "summary": "Explain what is meant by the transit method of detecting exoplanets."},
    {"qnum": "04.2", "page": 8, "marks": 2, "topic": "3.9", "skills": [], "figs": [], "summary": "Explain why it is important to have more than one method of detecting exoplanets."},
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
