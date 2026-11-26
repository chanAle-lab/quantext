#!/usr/bin/env python3
"""Ingest AQA AS Physics Paper 2 (7407/2) Specimen 2014 into questions.json + img/2014-specimen-7407-2/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2014-specimen-7407-2"
QP_PDF = ROOT / "raw_pdfs" / "media_1795693504262_6e193410.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795693504271_9fc39ded.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2014,
    "series": "Specimen",
    "date": "2014-10-08",
    "code": "7407/2",
    "unit": "AS Paper 2",
    "level": "AS",
    "spec": "current",
    "totalMarks": 70,
    "duration": "1 hour 30 minutes",
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-01-fig1.jpg", "page": 3, "x0": 120, "y0": 100, "x1": 545, "y1": 360},
    {"filename": "fig-02-fig3-4.jpg", "page": 5, "x0": 120, "y0": 85, "x1": 545, "y1": 745},
    {"filename": "fig-03-passage.jpg", "page": 8, "x0": 50, "y0": 140, "x1": 540, "y1": 495},
    {"filename": "fig-04-fig6.jpg", "page": 11, "x0": 115, "y0": 75, "x1": 545, "y1": 350},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 1, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "Calculate the percentage uncertainty in 3.5 x 10^3 lines per m."},
    {"qnum": "01.2", "page": 2, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "Determine the diffraction grating spacing in mm."},
    {"qnum": "01.3", "page": 2, "marks": 1, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "State the absolute uncertainty in the grating spacing."},
    {"qnum": "01.4", "page": 3, "marks": 1, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "Use Figure 2 to determine the spacing between two adjacent interference maxima."},
    {"qnum": "01.5", "page": 4, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": ["fig-01-fig1.jpg"], "summary": "Calculate the number of lines per metre on the diffraction grating."},
    {"qnum": "01.6", "page": 4, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "State and explain whether the experimental lines per metre agrees with the stated marking."},
    {"qnum": "01.7", "page": 4, "marks": 1, "topic": "3.1", "skills": ["practical"], "figs": [], "summary": "State one safety precaution when carrying out the laser diffraction experiment."},
    {"qnum": "02.1", "page": 6, "marks": 1, "topic": "3.1", "skills": ["graph", "practical"], "figs": ["fig-02-fig3-4.jpg"], "summary": "Draw a best-fit straight line for the capillary rise data in Figure 4."},
    {"qnum": "02.2", "page": 6, "marks": 1, "topic": "3.1", "skills": ["graph", "maths"], "figs": ["fig-02-fig3-4.jpg"], "summary": "Determine h0 from the relationship h = h0 - (h0*k)*theta."},
    {"qnum": "02.3", "page": 6, "marks": 3, "topic": "3.1", "skills": ["graph", "maths"], "figs": ["fig-02-fig3-4.jpg"], "summary": "Show that the value of h0*k is about 0.9 mm K^-1."},
    {"qnum": "02.4", "page": 6, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "Determine k and state an appropriate unit."},
    {"qnum": "02.5", "page": 7, "marks": 2, "topic": "3.1", "skills": ["graph", "maths"], "figs": [], "summary": "Calculate the internal tube diameter required to raise water 8.0 m by capillary action using Figure 5."},
    {"qnum": "02.6", "page": 7, "marks": 1, "topic": "3.1", "skills": ["practical"], "figs": [], "summary": "Comment on the accuracy of the internal tube diameter calculated in 2.5."},
    {"qnum": "03.1", "page": 9, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": ["fig-03-passage.jpg"], "summary": "Calculate the magnitude of the Young modulus for glass using Table 1."},
    {"qnum": "03.2", "page": 9, "marks": 1, "topic": "3.1", "skills": [], "figs": [], "summary": "State the answer to 3.1 in terms of SI fundamental units."},
    {"qnum": "03.3", "page": 9, "marks": 2, "topic": "3.3", "skills": [], "figs": [], "summary": "State the difference between longitudinal and transverse waves."},
    {"qnum": "03.4", "page": 9, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": ["fig-03-passage.jpg"], "summary": "Show that for two acoustically matched materials, the ratio of Young moduli equals the ratio of ultrasound speeds."},
    {"qnum": "03.5", "page": 9, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Determine the ratio of densities of acoustically matched materials X and Y when c_X = 2 c_Y."},
    {"qnum": "03.6", "page": 10, "marks": 3, "topic": "3.3", "skills": [], "figs": ["fig-03-passage.jpg"], "summary": "Discuss the conditions for total internal reflection of ultrasound waves between glass and sea water."},
    {"qnum": "04.1", "page": 11, "marks": 3, "topic": "3.5", "skills": ["graph", "maths"], "figs": ["fig-04-fig6.jpg"], "summary": "Use Figure 6 to calculate the current in the load at the peak power of the photovoltaic cell."},
    {"qnum": "04.2", "page": 12, "marks": 3, "topic": "3.5", "skills": ["maths"], "figs": ["fig-04-fig6.jpg"], "summary": "Calculate at peak power the ratio of electrical energy delivered to solar energy arriving at the 60 mm x 60 mm cell."},
    {"qnum": "04.3", "page": 12, "marks": 2, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "Estimate the number of 500 nm photons incident on the active area of the cell every second."},
    {"qnum": "04.4", "page": 13, "marks": 2, "topic": "3.1", "skills": [], "figs": ["fig-04-fig6.jpg"], "summary": "Identify two pieces of information scientists could provide to inform a householder's solar panel system."},
    # Section C MCQs (05 - 34)
    {"qnum": "05", "page": 14, "marks": 1, "topic": "3.1", "skills": [], "figs": [], "summary": "MCQ: Identify the pair of quantities that both have the same unit."},
    {"qnum": "06", "page": 14, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Find the numbers of hadrons, baryons, and mesons in an atom of Li-7."},
    {"qnum": "07", "page": 15, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify products X and Y in electron capture p + e- -> X + Y."},
    {"qnum": "08", "page": 15, "marks": 1, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the specific charge of a Ca^2+ ion formed from Ca-40."},
    {"qnum": "09", "page": 15, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Compare de Broglie wavelengths and diffraction pattern widths of electrons and protons at the same speed."},
    {"qnum": "10", "page": 16, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify how photon energy and photons per second change when monochromatic light intensity increases."},
    {"qnum": "11", "page": 16, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the statement about quarks and hadrons that is not true."},
    {"qnum": "12", "page": 16, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the minimum speed of a 10 Hz progressive wave if points 0.5 m apart are one-eighth of a wavelength apart."},
    {"qnum": "13", "page": 16, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Identify which wave cannot be polarised."},
    {"qnum": "14", "page": 17, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Identify how width and intensity of the central maximum change when single-slit width is reduced."},
    {"qnum": "15", "page": 17, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Find wavelength lambda_2 whose 4th order coincides with the 5th order of 480 nm light."},
    {"qnum": "16", "page": 17, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Identify the correct statement for a stationary wave."},
    {"qnum": "17", "page": 18, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Find frequency and wavelength in medium Y when 400 Hz sound crosses from 330 m s^-1 to 1320 m s^-1."},
    {"qnum": "18", "page": 18, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Identify which quantity is a scalar."},
    {"qnum": "19", "page": 19, "marks": 1, "topic": "3.4", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify graphs of kinetic energy and momentum against time for a constant force from rest."},
    {"qnum": "20", "page": 19, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate how far a freely falling object falls in the third second."},
    {"qnum": "21", "page": 20, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Identify which quantity of a freely falling body equals its rate of change of momentum."},
    {"qnum": "22", "page": 20, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Identify changes to total kinetic energy and total momentum when a firework explodes at its highest point."},
    {"qnum": "23", "page": 20, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate cable tension for a 500 kg lift accelerating upwards at 2 m s^-2."},
    {"qnum": "24", "page": 21, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Identify which expression is not a unit of power."},
    {"qnum": "25", "page": 21, "marks": 1, "topic": "3.4", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the displacement-time graph for a car accelerating uniformly from rest."},
    {"qnum": "26", "page": 22, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Identify which law indicates that normal reaction N and weight W on a resting ball are equal."},
    {"qnum": "27", "page": 22, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the energy stored in a 15 N m^-1 spring stretched by a 3.0 N load."},
    {"qnum": "28", "page": 23, "marks": 1, "topic": "3.4", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the incorrect statement from stress-strain graphs of metals X and Y."},
    {"qnum": "29", "page": 23, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the new current when one of three identical cells in series is reversed."},
    {"qnum": "30", "page": 24, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the current represented by 7.5 x 10^15 electrons striking a screen in 40 s."},
    {"qnum": "31", "page": 24, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the resistance of a wire of the same length and resistivity but half the diameter."},
    {"qnum": "32", "page": 24, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the terminal pd of a 2.0 V cell when external resistance increases from 4.0 ohm to 12 ohm."},
    {"qnum": "33", "page": 25, "marks": 1, "topic": "3.5", "skills": ["graph", "maths"], "figs": [], "summary": "MCQ: Determine the resistance of a filament lamp at 4.0 V from its I-V graph."},
    {"qnum": "34", "page": 25, "marks": 1, "topic": "3.5", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the graph of resistance per unit length r against wire diameter D."},
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

    ab_qnums = [q["qnum"] for q in QUESTIONS if "." in q["qnum"]]
    ms_written = crop_official_markschemes(MS_PDF, ab_qnums, IMG_DIR / "ms")
    print(f"Cropped {len(ms_written)} / {len(ab_qnums)} Section A/B mark schemes for {PAPER_ID}")

    ms_doc = fitz.open(str(MS_PDF))
    p11 = ms_doc[10]
    mcq_clip = fitz.Rect(225, 86, 590, 260)
    mcq_pix = p11.get_pixmap(clip=mcq_clip, matrix=fitz.Matrix(2.5, 2.5), alpha=False)
    mcq_key_rel = f"img/{PAPER_ID}/ms/mcq-key.png"
    mcq_pix.save(str(ROOT / mcq_key_rel))
    ms_doc.close()

    db_path = ROOT / "questions.json"
    db = json.loads(db_path.read_text(encoding="utf-8"))
    db["papers"] = [p for p in db["papers"] if p["id"] != PAPER_ID] + [PAPER_META]
    db["questions"] = [q for q in db["questions"] if q["paper"] != PAPER_ID]

    for q in QUESTIONS:
        slug = q["qnum"].replace(".", "-")
        ms_path = f"img/{PAPER_ID}/ms/q{slug}.png" if "." in q["qnum"] else mcq_key_rel
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
            "markscheme": ms_path,
        })

    db_path.write_text(json.dumps(db, indent=2) + "\n", encoding="utf-8")
    print(f"Updated questions.json with {len(QUESTIONS)} questions for {PAPER_ID}")


if __name__ == "__main__":
    main()
