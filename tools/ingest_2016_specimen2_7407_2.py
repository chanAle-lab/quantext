#!/usr/bin/env python3
"""Ingest AQA AS Physics Paper 2 (7407/2) Specimen Set 2 into questions.json + img/2016-specimen2-7407-2/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2016-specimen2-7407-2"
QP_PDF = ROOT / "raw_pdfs" / "media_1795693525050_da8472bd.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795693525048_940d7d40.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2016,
    "series": "Specimen Set 2",
    "date": "2016-06-01",
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
    {"filename": "fig-01-fig1.jpg", "page": 2, "x0": 75, "y0": 115, "x1": 545, "y1": 480},
    {"filename": "fig-02-fig3-4.jpg", "page": 5, "x0": 115, "y0": 75, "x1": 545, "y1": 745},
    {"filename": "fig-02-fig5.jpg", "page": 6, "x0": 115, "y0": 65, "x1": 545, "y1": 555},
    {"filename": "fig-03-fig6.jpg", "page": 8, "x0": 75, "y0": 140, "x1": 535, "y1": 465},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 1, "topic": "3.1", "skills": ["practical"], "figs": ["fig-01-fig1.jpg"], "summary": "State the resolution of the main scale on the micrometer in Figure 1."},
    {"qnum": "01.2", "page": 2, "marks": 2, "topic": "3.1", "skills": ["practical"], "figs": ["fig-01-fig1.jpg"], "summary": "Determine the distance between the anvil and spindle of the micrometer in Figure 1 and state any assumption."},
    {"qnum": "01.3", "page": 3, "marks": 1, "topic": "3.1", "skills": ["practical"], "figs": [], "summary": "Determine the length L of wire between clips P and Q from Figure 2."},
    {"qnum": "01.4", "page": 3, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "Calculate the percentage uncertainty in the measured length L."},
    {"qnum": "01.5", "page": 3, "marks": 1, "topic": "3.1", "skills": ["practical"], "figs": [], "summary": "State and explain how the student could reduce uncertainty in the reading for L."},
    {"qnum": "01.6", "page": 4, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "Calculate R/L in Table 1 and determine the resistance per metre of the wire."},
    {"qnum": "01.7", "page": 4, "marks": 4, "topic": "3.5", "skills": ["maths", "practical"], "figs": [], "summary": "Determine the resistivity of the 0.376 mm diameter wire with a suitable unit."},
    {"qnum": "02.1", "page": 6, "marks": 1, "topic": "3.1", "skills": ["graph", "practical"], "figs": ["fig-02-fig3-4.jpg"], "summary": "Draw a line of best fit on Figure 5 for Newton's rings diameter d against ring number b."},
    {"qnum": "02.2", "page": 7, "marks": 3, "topic": "3.1", "skills": ["graph", "maths"], "figs": ["fig-02-fig5.jpg"], "summary": "Determine the gradient G of Figure 5 corresponding to b = 25."},
    {"qnum": "02.3", "page": 7, "marks": 3, "topic": "3.1", "skills": ["graph", "maths"], "figs": ["fig-02-fig5.jpg"], "summary": "Determine the radius of curvature R of the lens using R = Gd / (2 lambda) with lambda = 589.3 nm."},
    {"qnum": "03.1", "page": 8, "marks": 2, "topic": "3.4", "skills": ["graph", "maths"], "figs": ["fig-03-fig6.jpg"], "summary": "Show from Figure 6 that the change in momentum of the golf ball during collision is about 0.5 N s."},
    {"qnum": "03.2", "page": 8, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Show that speeds of 7.1 m s^-1 before and 3.9 m s^-1 after for a 45 g ball give a momentum change of about 0.5 N s."},
    {"qnum": "03.3", "page": 9, "marks": 4, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Determine the percentage of original gravitational potential energy remaining after three bounces."},
    {"qnum": "03.4", "page": 9, "marks": 3, "topic": "3.4", "skills": [], "figs": [], "summary": "Explain, with reference to conservation of momentum, the effect of the falling ball on the motion of the Earth."},
    {"qnum": "04.1", "page": 10, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "Describe what occurs in the photoelectric effect."},
    {"qnum": "04.2", "page": 10, "marks": 4, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "Deduce whether 380 nm violet light can cause photoelectric emission from potassium (work function 2.3 eV)."},
    {"qnum": "04.3", "page": 11, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "State and explain one piece of evidence that suggests light also possesses wave properties."},
    # Section C MCQs (05 - 34)
    {"qnum": "05", "page": 12, "marks": 1, "topic": "3.1", "skills": [], "figs": [], "summary": "MCQ: Identify the row where SI fundamental units are correctly matched to the physical quantity."},
    {"qnum": "06", "page": 12, "marks": 1, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "MCQ: Identify which nucleus (H-1, C-12, C-14, U-235) has the smallest specific charge."},
    {"qnum": "07", "page": 13, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the nuclide formed after Th-232 undergoes one alpha decay and two beta-minus decays."},
    {"qnum": "08", "page": 13, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the row that does not give the correct exchange particle for the process."},
    {"qnum": "09", "page": 13, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the row that correctly classifies a particle's category and quark combination."},
    {"qnum": "10", "page": 14, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the incorrect statement about muons."},
    {"qnum": "11", "page": 14, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Explain why a charged metal plate discharges under UV light but not red light."},
    {"qnum": "12", "page": 14, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify which class of electromagnetic waves will not ionise neutral atoms."},
    {"qnum": "13", "page": 15, "marks": 1, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the photon frequency emitted for a transition from level 2 to level 1."},
    {"qnum": "14", "page": 15, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the experiment that suggested the wave nature of electrons."},
    {"qnum": "15", "page": 16, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the phase difference between two points 50 mm apart on a 150 Hz, 30 m s^-1 wave."},
    {"qnum": "16", "page": 16, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Identify the incorrect statement about the behaviour of waves."},
    {"qnum": "17", "page": 16, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the minimum distance between two nodes in a 1.4 MHz radio stationary wave."},
    {"qnum": "18", "page": 17, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Identify the frequency and phase conditions for two loudspeakers to be coherent."},
    {"qnum": "19", "page": 17, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Identify the slit spacing and screen distance changes that increase double-slit fringe spacing."},
    {"qnum": "20", "page": 18, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Identify the correct diffraction angle statement when a grating with N slits/m is replaced by 2N slits/m."},
    {"qnum": "21", "page": 18, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Find how a light ray strikes a liquid (n=1.6) and glass (n=1.5) boundary to travel along it."},
    {"qnum": "22", "page": 19, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Identify which quantity is a scalar."},
    {"qnum": "23", "page": 19, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the perpendicular force F needed to hold a 12 kg pivoted car bonnet at 30 degrees."},
    {"qnum": "24", "page": 20, "marks": 1, "topic": "3.4", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the distance-time graph corresponding to the given speed-time curve."},
    {"qnum": "25", "page": 20, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the acceleration of a 4 kg falling body when air resistance is 30 N."},
    {"qnum": "26", "page": 21, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the energy lost by a 0.4 kg stone projected horizontally at 6.0 m s^-1 from 5.0 m hitting at 10 m s^-1."},
    {"qnum": "27", "page": 21, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Identify which quantity is the same for two frictionless toy cars of different masses descending X to Y."},
    {"qnum": "28", "page": 22, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Identify the expression for elastic energy stored in a stretched wire in terms of E, A, e, and L."},
    {"qnum": "29", "page": 22, "marks": 1, "topic": "3.5", "skills": [], "figs": [], "summary": "MCQ: State how the electrical conductivity of a copper wire changes when its temperature increases."},
    {"qnum": "30", "page": 22, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Estimate the order of magnitude for the diameter of an atom."},
    {"qnum": "31", "page": 23, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the effective resistance between terminals P and Q of the resistor network."},
    {"qnum": "32", "page": 23, "marks": 1, "topic": "3.5", "skills": [], "figs": [], "summary": "MCQ: Express the resistivity of a metal wire in terms of V, I, l, and A."},
    {"qnum": "33", "page": 24, "marks": 1, "topic": "3.5", "skills": [], "figs": [], "summary": "MCQ: Identify between which two points a high-resistance voltmeter reads zero in the resistor bridge circuit."},
    {"qnum": "34", "page": 24, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the thermal energy dissipated inside a 6.0 V, 3.0 ohm cell connected to 12 ohm in 1 minute."},
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
    mcq_clip = fitz.Rect(42, 120, 490, 305)
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
