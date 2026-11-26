#!/usr/bin/env python3
"""Ingest AQA A-level Physics Paper 3A (7408/3A) Specimen 2014 into questions.json + img/2014-specimen-7408-3a/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2014-specimen-7408-3a"
QP_PDF = ROOT / "raw_pdfs" / "media_1795692434176_4a52e830.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795692434153_abe7e528.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2014,
    "series": "Specimen",
    "date": "2014-10-08",
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
    {"filename": "fig-01-fig1.jpg", "page": 3, "x0": 48, "y0": 145, "x1": 548, "y1": 710},
    {"filename": "fig-01-table1.jpg", "page": 4, "x0": 120, "y0": 382, "x1": 475, "y1": 640},
    {"filename": "fig-02-fig3.jpg", "page": 7, "x0": 48, "y0": 75, "x1": 540, "y1": 510},
    {"filename": "fig-03-fig4.jpg", "page": 12, "x0": 55, "y0": 75, "x1": 550, "y1": 445},
    {"filename": "fig-03-fig5.jpg", "page": 15, "x0": 95, "y0": 110, "x1": 490, "y1": 755},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 4, "marks": 1, "topic": "3.1", "skills": ["practical"], "figs": ["fig-01-fig1.jpg"], "summary": "Mark on Figure 2 the distance d fallen by the steel sphere."},
    {"qnum": "01.2", "page": 4, "marks": 1, "topic": "3.1", "skills": ["maths", "practical"], "figs": ["fig-01-fig1.jpg"], "summary": "Calculate the oscillation period and the time t for the bar to reach the vertical position."},
    {"qnum": "01.3", "page": 5, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "Determine the percentage uncertainty in time t from the stop-clock precision."},
    {"qnum": "01.4", "page": 5, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": ["fig-01-table1.jpg"], "summary": "Calculate a mean value for distance d from Table 1, rejecting any anomaly."},
    {"qnum": "01.5", "page": 5, "marks": 1, "topic": "3.1", "skills": ["maths", "practical"], "figs": ["fig-01-table1.jpg"], "summary": "Calculate the absolute uncertainty in the mean value of d."},
    {"qnum": "01.6", "page": 5, "marks": 3, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "Determine a value for g and its absolute uncertainty."},
    {"qnum": "01.7", "page": 6, "marks": 2, "topic": "3.1", "skills": ["practical"], "figs": ["fig-01-fig1.jpg"], "summary": "Discuss one change that could be made to reduce uncertainty in the free-fall experiment."},
    {"qnum": "01.8", "page": 6, "marks": 3, "topic": "3.1", "skills": ["graph", "practical"], "figs": ["fig-01-fig1.jpg"], "summary": "Suggest how distance s and time t data for a shortened bar should be analysed graphically to find g."},
    {"qnum": "02.1", "page": 7, "marks": 1, "topic": "3.1", "skills": ["practical"], "figs": ["fig-02-fig3.jpg"], "summary": "Explain why it is important to use a digital voltmeter with very high resistance."},
    {"qnum": "02.2", "page": 9, "marks": 1, "topic": "3.1", "skills": ["practical"], "figs": [], "summary": "Suggest one advantage of using an analogue ammeter rather than a digital ammeter in this experiment."},
    {"qnum": "02.3", "page": 9, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": ["fig-02-fig3.jpg"], "summary": "Suggest a suitable full-scale deflection for the analogue ammeter."},
    {"qnum": "02.4", "page": 9, "marks": 1, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "Calculate the absolute uncertainty in a 2.39 V voltmeter reading with 2% manufacturer uncertainty."},
    {"qnum": "02.5", "page": 10, "marks": 3, "topic": "3.1", "skills": ["maths", "practical"], "figs": ["fig-02-fig3.jpg"], "summary": "Determine the number of readings the student can take at 10 s intervals before the capacitor is fully charged."},
    {"qnum": "02.6", "page": 10, "marks": 2, "topic": "3.7", "skills": ["maths", "practical"], "figs": [], "summary": "Calculate the capacitance of the capacitor from a constant 65 uA current and 98 mV s^-1 pd rise."},
    {"qnum": "02.7", "page": 10, "marks": 1, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "Deduce whether the measured capacitance lies within the +/- 5% manufacturer tolerance of 680 uF."},
    {"qnum": "02.8", "page": 11, "marks": 4, "topic": "3.7", "skills": ["practical", "graph"], "figs": [], "summary": "Describe an experiment (circuit, procedure, analysis) to determine the discharge time constant through a fixed resistor."},
    {"qnum": "03.1", "page": 12, "marks": 1, "topic": "3.1", "skills": ["graph", "practical"], "figs": ["fig-03-fig4.jpg"], "summary": "Comment on whether the n vs wavelength curve in Figure 4 shows half-life behaviour."},
    {"qnum": "03.2", "page": 13, "marks": 3, "topic": "3.1", "skills": ["graph", "maths", "practical"], "figs": ["fig-03-fig4.jpg"], "summary": "Determine the dispersion D = delta-n / delta-lambda at 400 nm with an appropriate unit."},
    {"qnum": "03.3", "page": 14, "marks": 3, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "Calculate and tabulate derived data in Table 2 to plot n against 1 / lambda^2."},
    {"qnum": "03.4", "page": 15, "marks": 3, "topic": "3.1", "skills": ["graph", "practical"], "figs": [], "summary": "Plot the linearised graph of n against 1 / lambda^2 on Figure 5."},
    {"qnum": "03.5", "page": 16, "marks": 1, "topic": "3.1", "skills": ["graph", "practical"], "figs": ["fig-03-fig5.jpg"], "summary": "Use the plotted graph to determine the constant a."},
    {"qnum": "03.6", "page": 16, "marks": 1, "topic": "3.1", "skills": ["graph"], "figs": [], "summary": "State the physical significance of the constant a."},
    {"qnum": "03.7", "page": 16, "marks": 3, "topic": "3.1", "skills": ["graph", "practical"], "figs": [], "summary": "Explain how the exponent d in n = c lambda^d can be determined graphically."},
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
