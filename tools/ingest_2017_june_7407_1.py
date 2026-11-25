#!/usr/bin/env python3
"""Ingest AQA AS Physics Paper 1 (7407/1) June 2017 into questions.json + img/2017-june-7407-1/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2017-june-7407-1"
QP_PDF = ROOT / "raw_pdfs" / "media_1795607555778_3a6c257e.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795607556251_c9c819b3.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2017,
    "series": "June",
    "date": "2017-05-23",
    "code": "7407/1",
    "unit": "AS Paper 1",
    "level": "AS",
    "spec": "current",
    "totalMarks": 70,
    "duration": "1 hour 30 minutes",
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-01-fig1.jpg", "page": 2, "x0": 48, "y0": 120, "x1": 540, "y1": 410},
    {"filename": "fig-02-fig2.jpg", "page": 4, "x0": 48, "y0": 62, "x1": 540, "y1": 420},
    {"filename": "fig-03-stem.jpg", "page": 7, "x0": 48, "y0": 62, "x1": 540, "y1": 200},
    {"filename": "fig-03-fig3.jpg", "page": 8, "x0": 48, "y0": 62, "x1": 540, "y1": 230},
    {"filename": "fig-04-fig4-5.jpg", "page": 10, "x0": 48, "y0": 62, "x1": 540, "y1": 740},
    {"filename": "fig-05-fig6.jpg", "page": 14, "x0": 48, "y0": 62, "x1": 540, "y1": 405},
    {"filename": "fig-07-fig8-9.jpg", "page": 20, "x0": 48, "y0": 62, "x1": 540, "y1": 700},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 1, "topic": "3.2", "skills": [], "figs": ["fig-01-fig1.jpg"], "summary": "Deduce the name of particle X from the Feynman decay diagram."},
    {"qnum": "01.2", "page": 2, "marks": 1, "topic": "3.2", "skills": [], "figs": ["fig-01-fig1.jpg"], "summary": "State the type of interaction that occurs in this decay."},
    {"qnum": "01.3", "page": 2, "marks": 1, "topic": "3.2", "skills": [], "figs": ["fig-01-fig1.jpg"], "summary": "State the class of particles to which the W- belongs."},
    {"qnum": "01.4", "page": 3, "marks": 2, "topic": "3.2", "skills": [], "figs": ["fig-01-fig1.jpg"], "summary": "Show clearly how charge and baryon number are conserved in the interaction, including quarks."},
    {"qnum": "01.5", "page": 3, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "Name the only stable baryon."},
    {"qnum": "01.6", "page": 3, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "State the names of the particles produced when a muon decays."},
    {"qnum": "02.1", "page": 4, "marks": 4, "topic": "3.5", "skills": ["graph"], "figs": ["fig-02-fig2.jpg"], "summary": "Explain in terms of electron motion why the I-V characteristic for the filament lamp is a curve."},
    {"qnum": "02.2", "page": 5, "marks": 1, "topic": "3.5", "skills": ["graph", "maths"], "figs": ["fig-02-fig2.jpg"], "summary": "Determine the resistance of the ohmic resistor from Figure 2."},
    {"qnum": "02.3", "page": 5, "marks": 3, "topic": "3.5", "skills": ["graph", "maths"], "figs": ["fig-02-fig2.jpg"], "summary": "Determine the emf that produces a current of 0.18 A when the resistor and lamp are in series."},
    {"qnum": "02.4", "page": 5, "marks": 3, "topic": "3.5", "skills": ["graph", "maths"], "figs": ["fig-02-fig2.jpg"], "summary": "Determine the resistance of the parallel combination of resistor and lamp at 4.0 V."},
    {"qnum": "02.5", "page": 6, "marks": 3, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "Calculate the resistivity of the filament metal at its working temperature with an appropriate unit."},
    {"qnum": "03.1", "page": 7, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": ["fig-03-stem.jpg"], "summary": "Show that the average power output of the electric wheelchair battery is about 100 W."},
    {"qnum": "03.2", "page": 7, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": ["fig-03-stem.jpg"], "summary": "Calculate the total mean resistive force acting on the wheelchair and its user."},
    {"qnum": "03.3", "page": 8, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": ["fig-03-stem.jpg", "fig-03-fig3.jpg"], "summary": "Calculate the component of gravity parallel to the 4.5 degree slope."},
    {"qnum": "03.4", "page": 8, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": ["fig-03-fig3.jpg"], "summary": "Calculate the maximum speed of the wheelchair up the hill at 100 W output power."},
    {"qnum": "03.5", "page": 9, "marks": 4, "topic": "3.4", "skills": [], "figs": [], "summary": "Explain how and why the maximum range on level ground depends on user mass and travel speed."},
    {"qnum": "04.1", "page": 11, "marks": 3, "topic": "3.3", "skills": ["practical"], "figs": ["fig-04-fig4-5.jpg"], "summary": "Explain why microwave signal strength falls to a minimum between B and C, and between C and D."},
    {"qnum": "04.2", "page": 11, "marks": 3, "topic": "3.3", "skills": ["maths", "practical"], "figs": ["fig-04-fig4-5.jpg"], "summary": "Determine the frequency of the transmitted microwaves from path distances at D."},
    {"qnum": "04.3", "page": 12, "marks": 2, "topic": "3.3", "skills": ["practical"], "figs": ["fig-04-fig4-5.jpg"], "summary": "Explain why the minimum intensity between C and D is not zero even though slit intensities are equal."},
    {"qnum": "04.4", "page": 12, "marks": 3, "topic": "3.3", "skills": ["practical"], "figs": ["fig-04-fig4-5.jpg"], "summary": "State and explain the effect on signal strength when the vertical receiving aerial is rotated by 90 degrees."},
    {"qnum": "05.1", "page": 14, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": ["fig-05-fig6.jpg"], "summary": "Show that the extension of a 12 m copper aerial wire under 500 N tension is less than 4 mm."},
    {"qnum": "05.2", "page": 15, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": ["fig-05-fig6.jpg"], "summary": "Calculate the tension in each supporting cable at 65 degrees for horizontal equilibrium."},
    {"qnum": "05.3", "page": 15, "marks": 4, "topic": "3.3", "skills": [], "figs": [], "summary": "Explain how stationary waves form on the aerial wire and why only specific frequencies can occur."},
    {"qnum": "05.4", "page": 16, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": ["fig-05-fig6.jpg"], "summary": "Calculate the mass per unit length of the copper aerial wire."},
    {"qnum": "05.5", "page": 16, "marks": 2, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "Calculate the frequency of the third harmonic on the aerial wire."},
    {"qnum": "05.6", "page": 16, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "Sketch the third harmonic standing wave on Figure 7."},
    {"qnum": "05.7", "page": 17, "marks": 2, "topic": "3.4", "skills": [], "figs": [], "summary": "Explain why the aerial wire may sag after high winds produce large-amplitude vibrations."},
    {"qnum": "06", "page": 19, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "Identify the statement that suggests electrons have wave properties."},
    {"qnum": "07.1", "page": 21, "marks": 3, "topic": "3.2", "skills": ["maths"], "figs": ["fig-07-fig8-9.jpg"], "summary": "Calculate the energy in eV of the lowest-frequency photon in the visible hydrogen spectrum."},
    {"qnum": "07.2", "page": 21, "marks": 1, "topic": "3.2", "skills": [], "figs": ["fig-07-fig8-9.jpg"], "summary": "Identify the state of an electron in the energy level labelled 0."},
    {"qnum": "07.3", "page": 21, "marks": 1, "topic": "3.2", "skills": [], "figs": ["fig-07-fig8-9.jpg"], "summary": "Identify the state of an electron in the energy level labelled -13.6 eV."},
    {"qnum": "07.4", "page": 21, "marks": 1, "topic": "3.2", "skills": [], "figs": ["fig-07-fig8-9.jpg"], "summary": "Explain why atomic energy levels are negative."},
    {"qnum": "07.5", "page": 22, "marks": 6, "topic": "3.2", "skills": ["maths"], "figs": ["fig-07-fig8-9.jpg"], "summary": "Discuss how the hydrogen discharge tube emits specific frequencies and relate one wavelength to Figure 9."},
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
