#!/usr/bin/env python3
"""Ingest AQA A-level Physics Paper 3A (7408/3A) Specimen Set 2 into questions.json + img/2016-specimen2-7408-3a/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2016-specimen2-7408-3a"
QP_PDF = ROOT / "raw_pdfs" / "media_1795693078635_ef734b46.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795693078603_008d5abd.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2016,
    "series": "Specimen Set 2",
    "date": "2016-06-01",
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
    {"filename": "fig-01-fig1.jpg", "page": 3, "x0": 110, "y0": 100, "x1": 550, "y1": 715},
    {"filename": "fig-01-fig2.jpg", "page": 4, "x0": 125, "y0": 62, "x1": 480, "y1": 375},
    {"filename": "fig-01-table1.jpg", "page": 6, "x0": 120, "y0": 545, "x1": 540, "y1": 740},
    {"filename": "fig-01-fig6.jpg", "page": 7, "x0": 45, "y0": 62, "x1": 460, "y1": 520},
    {"filename": "fig-01-fig9.jpg", "page": 11, "x0": 45, "y0": 72, "x1": 555, "y1": 720},
    {"filename": "fig-02-fig10.jpg", "page": 12, "x0": 115, "y0": 65, "x1": 540, "y1": 775},
    {"filename": "fig-02-fig11.jpg", "page": 14, "x0": 115, "y0": 65, "x1": 545, "y1": 765},
    {"filename": "fig-02-q02-4-p15.jpg", "page": 15, "x0": 115, "y0": 65, "x1": 550, "y1": 310},
    {"filename": "fig-03-fig13.jpg", "page": 18, "x0": 68, "y0": 65, "x1": 550, "y1": 450},
    {"filename": "fig-03-fig14-tab2.jpg", "page": 18, "x0": 115, "y0": 455, "x1": 555, "y1": 775},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 4, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": ["fig-01-fig1.jpg", "fig-01-fig2.jpg"], "summary": "Determine the frequency of the current in the circular coil using Figure 2."},
    {"qnum": "01.2", "page": 4, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": ["fig-01-fig2.jpg"], "summary": "Determine the rms voltage of the induced emf in the search coil using Figure 2."},
    {"qnum": "01.3", "page": 5, "marks": 2, "topic": "3.1", "skills": ["maths"], "figs": ["fig-01-fig1.jpg"], "summary": "Explain why the magnetic flux linked with the search coil is directly proportional to cos theta."},
    {"qnum": "01.4", "page": 6, "marks": 4, "topic": "3.1", "skills": ["graph", "maths", "practical"], "figs": ["fig-01-fig6.jpg"], "summary": "Calculate cos theta in Table 1 and plot on Figure 6 a graph to test whether l is directly proportional to cos theta."},
    {"qnum": "01.5", "page": 7, "marks": 1, "topic": "3.1", "skills": ["graph", "practical"], "figs": ["fig-01-table1.jpg", "fig-01-fig6.jpg"], "summary": "State and explain whether the plotted graph confirms that l is directly proportional to cos theta."},
    {"qnum": "01.6", "page": 8, "marks": 4, "topic": "3.1", "skills": ["practical"], "figs": [], "summary": "Describe two adjustments to the oscilloscope trace in Figure 7 to reduce the uncertainty in l."},
    {"qnum": "01.7", "page": 9, "marks": 3, "topic": "3.1", "skills": ["practical"], "figs": [], "summary": "State and explain changes to the oscilloscope settings when the signal generator frequency is doubled."},
    {"qnum": "01.8", "page": 10, "marks": 2, "topic": "3.1", "skills": ["graph"], "figs": ["fig-01-fig9.jpg"], "summary": "Explain whether the graph in Figure 9 supports the suggestion that l decreases exponentially as x increases."},
    {"qnum": "02.1", "page": 13, "marks": 1, "topic": "3.1", "skills": ["graph"], "figs": ["fig-02-fig10.jpg"], "summary": "Determine the water temperature theta_1 at t = 190 s from Figure 10."},
    {"qnum": "02.2", "page": 13, "marks": 3, "topic": "3.1", "skills": ["graph", "maths"], "figs": ["fig-02-fig10.jpg"], "summary": "Determine the gradient G1 of the cooling curve in Figure 10 at t = 190 s."},
    {"qnum": "02.3", "page": 13, "marks": 1, "topic": "3.1", "skills": ["maths"], "figs": [], "summary": "Evaluate the room temperature theta_R using G1, G2, theta_1, and theta_2."},
    {"qnum": "02.4", "page": 14, "marks": 4, "topic": "3.1", "skills": ["graph", "maths"], "figs": ["fig-02-fig11.jpg", "fig-02-q02-4-p15.jpg"], "summary": "Estimate the time taken for the water to cool down to room temperature using Figure 11 and time constants."},
    {"qnum": "02.5", "page": 16, "marks": 5, "topic": "3.1", "skills": ["graph", "maths"], "figs": ["fig-02-fig11.jpg"], "summary": "Account quantitatively for the differences between the cooling results in Figure 12 and Figure 11."},
    {"qnum": "03.1", "page": 19, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": ["fig-03-fig13.jpg", "fig-03-fig14-tab2.jpg"], "summary": "Determine the interference fringe spacing w using Figure 14 and Table 2 to an appropriate number of sig figs."},
    {"qnum": "03.2", "page": 19, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": ["fig-03-fig13.jpg", "fig-03-fig14-tab2.jpg"], "summary": "Determine the diameter d of the cylindrical wire using 589.3 nm light."},
    {"qnum": "03.3", "page": 19, "marks": 3, "topic": "3.1", "skills": ["maths", "practical"], "figs": ["fig-03-fig13.jpg", "fig-03-fig14-tab2.jpg"], "summary": "Estimate the number of interference fringes seen between P and Q."},
    {"qnum": "03.4", "page": 20, "marks": 2, "topic": "3.1", "skills": ["practical"], "figs": [], "summary": "Describe a procedure before using a micrometer screw gauge to prevent systematic error."},
    {"qnum": "03.5", "page": 20, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "Use the micrometer measurements in Table 3 to determine the percentage uncertainty in d."},
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
