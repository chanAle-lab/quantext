#!/usr/bin/env python3
"""Ingest AQA A-level Physics Paper 3A (7408/3A) June 2017 into questions.json + img/2017-june-7408-3a/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2017-june-7408-3a"
QP_PDF = ROOT / "raw_pdfs" / "media_1795607555737_bf406981.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795607556484_47db1bfc.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2017,
    "series": "June",
    "date": "2017-06-29",
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
    {"filename": "fig-01-fig1.jpg", "page": 2, "x0": 48, "y0": 124, "x1": 540, "y1": 680},
    {"filename": "fig-01-fig2-3.jpg", "page": 3, "x0": 48, "y0": 62, "x1": 540, "y1": 565},
    {"filename": "fig-01-fig4.jpg", "page": 7, "x0": 60, "y0": 62, "x1": 525, "y1": 650},
    {"filename": "fig-02-fig5-6.jpg", "page": 9, "x0": 48, "y0": 62, "x1": 540, "y1": 620},
    {"filename": "fig-02-fig7-8.jpg", "page": 11, "x0": 85, "y0": 62, "x1": 510, "y1": 725},
    {"filename": "fig-02-fig9-10.jpg", "page": 12, "x0": 48, "y0": 62, "x1": 540, "y1": 755},
    {"filename": "fig-03-fig13.jpg", "page": 18, "x0": 48, "y0": 62, "x1": 540, "y1": 710},
    {"filename": "fig-03-fig14-15.jpg", "page": 19, "x0": 48, "y0": 62, "x1": 540, "y1": 730},
    {"filename": "fig-03-table2.jpg", "page": 20, "x0": 95, "y0": 62, "x1": 495, "y1": 295},
    {"filename": "fig-03-fig16.jpg", "page": 21, "x0": 75, "y0": 62, "x1": 510, "y1": 695},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 3, "marks": 1, "topic": "3.3", "skills": ["practical"], "figs": ["fig-01-fig1.jpg", "fig-01-fig2-3.jpg"], "summary": "State the phase difference between direct and reflected waves at a microwave minimum with a suitable unit."},
    {"qnum": "01.2", "page": 4, "marks": 1, "topic": "3.3", "skills": ["practical"], "figs": ["fig-01-fig2-3.jpg"], "summary": "Explain why the minimum ammeter reading is not zero when distance x is measured."},
    {"qnum": "01.3", "page": 4, "marks": 2, "topic": "3.3", "skills": ["practical"], "figs": ["fig-01-fig2-3.jpg"], "summary": "Describe a procedure to ensure metal sheet M is parallel to the marked line before measuring x."},
    {"qnum": "01.4", "page": 6, "marks": 3, "topic": "3.1", "skills": ["graph", "practical", "maths"], "figs": ["fig-01-fig4.jpg"], "summary": "Determine the maximum and minimum gradients Gmax and Gmin passing through all error bars on Figure 4."},
    {"qnum": "01.5", "page": 6, "marks": 2, "topic": "3.3", "skills": ["graph", "maths"], "figs": ["fig-01-fig4.jpg"], "summary": "Determine the microwave wavelength lambda using Gmax and Gmin."},
    {"qnum": "01.6", "page": 8, "marks": 3, "topic": "3.1", "skills": ["maths", "practical"], "figs": ["fig-01-fig4.jpg"], "summary": "Determine the percentage uncertainty in the value of lambda."},
    {"qnum": "01.7", "page": 8, "marks": 2, "topic": "3.1", "skills": ["graph", "practical"], "figs": ["fig-01-fig4.jpg"], "summary": "Explain how Figure 4 can be used to obtain the distance y."},
    {"qnum": "01.8", "page": 8, "marks": 4, "topic": "3.1", "skills": ["graph", "practical"], "figs": ["fig-01-fig4.jpg"], "summary": "Identify how Gmax, Gmin, lambda, and y would be affected if n = 13 were omitted from Figure 4."},
    {"qnum": "02.1", "page": 10, "marks": 1, "topic": "3.5", "skills": ["practical", "maths"], "figs": ["fig-02-fig5-6.jpg", "fig-02-fig7-8.jpg"], "summary": "Determine the peak-to-peak voltage V of the square-wave oscilloscope trace in Figure 8."},
    {"qnum": "02.2", "page": 10, "marks": 2, "topic": "3.3", "skills": ["practical", "maths"], "figs": ["fig-02-fig5-6.jpg", "fig-02-fig7-8.jpg"], "summary": "Determine the frequency f of the waveform shown in Figure 8."},
    {"qnum": "02.3", "page": 13, "marks": 2, "topic": "3.7", "skills": ["practical", "maths"], "figs": ["fig-02-fig5-6.jpg", "fig-02-fig9-10.jpg"], "summary": "Determine the time constant of the RC circuit from the oscilloscope trace in Figure 10."},
    {"qnum": "02.4", "page": 13, "marks": 3, "topic": "3.1", "skills": ["practical"], "figs": ["fig-02-fig9-10.jpg"], "summary": "State and explain any advantage or disadvantage of changing the time-base to 0.2 ms/div."},
    {"qnum": "02.5", "page": 14, "marks": 2, "topic": "3.7", "skills": ["practical", "graph"], "figs": [], "summary": "Sketch and explain the new capacitor waveform when an identical resistor is connected in parallel with R."},
    {"qnum": "02.6", "page": 15, "marks": 2, "topic": "3.7", "skills": ["graph", "practical"], "figs": [], "summary": "Sketch the voltage-time graph across resistor R when R and C are interchanged."},
    {"qnum": "02.7", "page": 16, "marks": 2, "topic": "3.5", "skills": ["practical"], "figs": ["fig-02-fig5-6.jpg"], "summary": "State and explain changes needed to the oscilloscope settings to display the waveform across R fully."},
    {"qnum": "03.1", "page": 20, "marks": 1, "topic": "3.1", "skills": ["practical"], "figs": ["fig-03-fig13.jpg", "fig-03-fig14-15.jpg", "fig-03-table2.jpg"], "summary": "Deduce the initial position p of the air-track glider at n = 0 using Figure 13 and Figure 15."},
    {"qnum": "03.2", "page": 20, "marks": 1, "topic": "3.1", "skills": ["practical", "maths"], "figs": ["fig-03-fig14-15.jpg", "fig-03-table2.jpg"], "summary": "Deduce the distance x moved by the glider for all values of n using Figure 14."},
    {"qnum": "03.3", "page": 20, "marks": 3, "topic": "3.1", "skills": ["graph", "practical"], "figs": ["fig-03-table2.jpg", "fig-03-fig16.jpg"], "summary": "Calculate ln(x/cm) and plot a graph of ln(x/cm) against n on Figure 16."},
    {"qnum": "03.4", "page": 20, "marks": 1, "topic": "3.6", "skills": ["graph", "practical"], "figs": ["fig-03-fig16.jpg"], "summary": "Explain why the plotted graph confirms that x decreases exponentially with n."},
    {"qnum": "03.5", "page": 22, "marks": 3, "topic": "3.1", "skills": ["graph", "maths", "practical"], "figs": ["fig-03-fig16.jpg"], "summary": "Determine the value of x when n = 20 using the graph in Figure 16."},
    {"qnum": "03.6", "page": 22, "marks": 4, "topic": "3.1", "skills": ["practical"], "figs": ["fig-03-fig13.jpg"], "summary": "Describe and explain two procedures to reduce uncertainty in measurements of p."},
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
