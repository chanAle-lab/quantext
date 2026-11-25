#!/usr/bin/env python3
"""Ingest AQA A-level Physics Paper 3A (7408/3A) June 2018 into questions.json + img/2018-june-7408-3a/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2018-june-7408-3a"
QP_PDF = ROOT / "raw_pdfs" / "media_1795609285683_5b76cf6a.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795609285685_1de7f023.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2018,
    "series": "June",
    "date": "2018-06-14",
    "code": "7408/3A",
    "unit": "A-level Paper 3A",
    "level": "A",
    "spec": "current",
    "totalMarks": 45,
    "duration": "2 hours (total Paper 3)",
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-01-fig1-2.jpg", "page": 2, "x0": 48, "y0": 125, "x1": 540, "y1": 700},
    {"filename": "fig-01-fig3.jpg", "page": 4, "x0": 48, "y0": 205, "x1": 540, "y1": 650},
    {"filename": "fig-01-fig4.jpg", "page": 5, "x0": 48, "y0": 60, "x1": 540, "y1": 600},
    {"filename": "fig-01-fig6.jpg", "page": 8, "x0": 100, "y0": 245, "x1": 490, "y1": 665},
    {"filename": "fig-02-fig7.jpg", "page": 10, "x0": 48, "y0": 62, "x1": 540, "y1": 640},
    {"filename": "fig-02-table2.jpg", "page": 11, "x0": 180, "y0": 338, "x1": 410, "y1": 560},
    {"filename": "fig-02-fig8.jpg", "page": 13, "x0": 65, "y0": 55, "x1": 525, "y1": 760},
    {"filename": "fig-03-fig9ab.jpg", "page": 15, "x0": 48, "y0": 62, "x1": 540, "y1": 650},
    {"filename": "fig-03-fig9cd.jpg", "page": 16, "x0": 48, "y0": 62, "x1": 540, "y1": 545},
    {"filename": "fig-03-fig11.jpg", "page": 18, "x0": 95, "y0": 228, "x1": 485, "y1": 755},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 3, "marks": 3, "topic": "3.4", "skills": ["maths", "practical"], "figs": ["fig-01-fig1-2.jpg"], "summary": "Deduce the mass of the pivoted metre ruler from the digital balance reading and state one assumption."},
    {"qnum": "01.2", "page": 4, "marks": 3, "topic": "3.7", "skills": ["practical", "graph"], "figs": ["fig-01-fig4.jpg"], "summary": "State and explain the direction of the horizontal uniform magnetic field using Figure 3 and Figure 4."},
    {"qnum": "01.3", "page": 6, "marks": 3, "topic": "3.7", "skills": ["maths", "graph", "practical"], "figs": ["fig-01-fig3.jpg", "fig-01-fig4.jpg"], "summary": "Determine the magnetic flux density B using B = sigma / (3L) and the gradient of Figure 4."},
    {"qnum": "01.4", "page": 7, "marks": 3, "topic": "3.7", "skills": ["practical", "graph"], "figs": ["fig-01-fig3.jpg", "fig-01-fig4.jpg"], "summary": "Identify the effect of moving the pivot to the 99.0 cm mark on the forces, gradient, and intercept."},
    {"qnum": "01.5", "page": 8, "marks": 2, "topic": "3.5", "skills": ["practical"], "figs": [], "summary": "Complete the circuit diagram in Figure 6 so currents in wires X and Y have equal magnitude and shown directions."},
    {"qnum": "01.6", "page": 9, "marks": 5, "topic": "3.1", "skills": ["practical", "graph"], "figs": ["fig-01-fig6.jpg"], "summary": "Explain an experimental and graphical procedure using Figure 6 to determine the constant k."},
    {"qnum": "02.1", "page": 11, "marks": 2, "topic": "3.1", "skills": ["practical"], "figs": ["fig-02-fig7.jpg"], "summary": "Describe a suitable procedure to measure the vertical displacement y of the overhanging steel tape."},
    {"qnum": "02.2", "page": 11, "marks": 1, "topic": "3.1", "skills": ["practical"], "figs": [], "summary": "Suggest why all measurements of horizontal displacement x were chosen to be greater than 70 cm."},
    {"qnum": "02.3", "page": 12, "marks": 3, "topic": "3.1", "skills": ["graph", "maths", "practical"], "figs": ["fig-02-fig8.jpg"], "summary": "Determine the integer n in y = Ax^n from the log-log graph in Figure 8."},
    {"qnum": "02.4", "page": 14, "marks": 3, "topic": "3.1", "skills": ["graph", "practical"], "figs": ["fig-02-fig8.jpg"], "summary": "Explain how the numerical value of A can be obtained from Figure 8."},
    {"qnum": "02.5", "page": 14, "marks": 3, "topic": "3.1", "skills": ["maths", "practical"], "figs": ["fig-02-table2.jpg"], "summary": "Estimate the order of magnitude of A with an appropriate unit using one row from Table 2."},
    {"qnum": "03.1", "page": 16, "marks": 2, "topic": "3.6", "skills": ["practical"], "figs": ["fig-03-fig9cd.jpg"], "summary": "Explain why the volume of air in the flask in Figure 9c is less than in Figure 9d."},
    {"qnum": "03.2", "page": 17, "marks": 2, "topic": "3.6", "skills": ["practical"], "figs": ["fig-03-fig9ab.jpg", "fig-03-fig9cd.jpg"], "summary": "Explain why Charles's Law can be applied to compare the air in the flask in Figure 9a and Figure 9d."},
    {"qnum": "03.3", "page": 17, "marks": 3, "topic": "3.1", "skills": ["practical"], "figs": [], "summary": "Explain how volumes V1 and V2 can be determined while eliminating possible systematic error."},
    {"qnum": "03.4", "page": 18, "marks": 3, "topic": "3.1", "skills": ["graph", "practical"], "figs": ["fig-03-fig9ab.jpg", "fig-03-fig9cd.jpg"], "summary": "Plot the volume and temperature points for Figure 9a and Figure 9d on Figure 11."},
    {"qnum": "03.5", "page": 19, "marks": 1, "topic": "3.6", "skills": ["graph", "practical"], "figs": ["fig-03-fig11.jpg"], "summary": "Add a best-fit line to Figure 11 showing how volume varies with temperature according to Charles's Law."},
    {"qnum": "03.6", "page": 19, "marks": 3, "topic": "3.6", "skills": ["graph", "maths", "practical"], "figs": ["fig-03-fig11.jpg"], "summary": "Determine the value of absolute zero in degrees Celsius using Figure 11."},
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
