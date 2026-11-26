#!/usr/bin/env python3
"""Ingest AQA A-level Physics Paper 2 (7408/2) Specimen 2014 into questions.json + img/2014-specimen-7408-2/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2014-specimen-7408-2"
QP_PDF = ROOT / "raw_pdfs" / "media_1795692434151_d4f743aa.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795692434187_61b44abe.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2014,
    "series": "Specimen",
    "date": "2014-10-08",
    "code": "7408/2",
    "unit": "A-level Paper 2",
    "level": "A",
    "spec": "current",
    "totalMarks": 85,
    "duration": "2 hours",
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-01-fig1.jpg", "page": 2, "x0": 55, "y0": 135, "x1": 535, "y1": 575},
    {"filename": "fig-02-fig2.jpg", "page": 6, "x0": 55, "y0": 75, "x1": 535, "y1": 235},
    {"filename": "fig-05-fig3.jpg", "page": 12, "x0": 55, "y0": 65, "x1": 565, "y1": 340},
    {"filename": "fig-05-fig4-6.jpg", "page": 13, "x0": 55, "y0": 62, "x1": 540, "y1": 790},
    {"filename": "fig-06-passage.jpg", "page": 14, "x0": 55, "y0": 290, "x1": 535, "y1": 765},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": ["fig-01-fig1.jpg"], "summary": "Calculate the time taken for a crushed ore particle to fall 4.5 m between vertical plates."},
    {"qnum": "01.2", "page": 3, "marks": 3, "topic": "3.7", "skills": ["maths"], "figs": ["fig-01-fig1.jpg"], "summary": "Show that the horizontal acceleration of a particle with specific charge 1.2e-6 C kg^-1 at 65 kV is about 0.2 m s^-2."},
    {"qnum": "01.3", "page": 3, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "Calculate the total horizontal deflection of the particle while falling between the plates."},
    {"qnum": "01.4", "page": 3, "marks": 2, "topic": "3.7", "skills": [], "figs": [], "summary": "Explain why the vertical fall time between the plates is independent of particle mass."},
    {"qnum": "01.5", "page": 4, "marks": 4, "topic": "3.7", "skills": [], "figs": [], "summary": "State and explain two reasons why the horizontal acceleration differs for each particle."},
    {"qnum": "02.1", "page": 6, "marks": 2, "topic": "3.7", "skills": ["maths"], "figs": ["fig-02-fig2.jpg"], "summary": "Calculate the thickness of the polythene dielectric sheet in a 370 pF parallel-plate capacitor."},
    {"qnum": "02.2", "page": 6, "marks": 2, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "Show that the pd increases to about 80 V when the polythene sheet is removed while isolated."},
    {"qnum": "02.3", "page": 7, "marks": 2, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "Calculate the energy now stored by the capacitor after the polythene sheet is removed."},
    {"qnum": "02.4", "page": 7, "marks": 2, "topic": "3.7", "skills": [], "figs": [], "summary": "Explain why energy stored increases when the polythene sheet is pulled out from between the plates."},
    {"qnum": "03.1", "page": 8, "marks": 2, "topic": "3.6", "skills": [], "figs": [], "summary": "State two assumptions about molecular motion in the derivation of the kinetic theory equation."},
    {"qnum": "03.2", "page": 8, "marks": 3, "topic": "3.6", "skills": [], "figs": [], "summary": "Use kinetic theory to explain why air pressure inside a football rises with temperature at constant volume."},
    {"qnum": "03.3", "page": 9, "marks": 6, "topic": "3.6", "skills": ["maths"], "figs": [], "summary": "Deduce whether an inflated football with 11.4 g of air at 17 C satisfies the pressure rule."},
    {"qnum": "04.1", "page": 10, "marks": 1, "topic": "3.8", "skills": ["maths"], "figs": [], "summary": "Show that initially about 7.5e10 atoms of sodium-24 are injected into the ancient flask."},
    {"qnum": "04.2", "page": 10, "marks": 3, "topic": "3.8", "skills": ["maths"], "figs": [], "summary": "Show that the initial activity of the injected sodium-24 solution is about 1e6 Bq."},
    {"qnum": "04.3", "page": 11, "marks": 3, "topic": "3.8", "skills": ["maths"], "figs": [], "summary": "Calculate the total activity after 3.5 h and determine the volume of liquid in the flask."},
    {"qnum": "04.4", "page": 11, "marks": 2, "topic": "3.8", "skills": ["maths"], "figs": [], "summary": "Compare the archaeologist's mass-based volume estimate with 4.3 and account for any difference."},
    {"qnum": "05.1", "page": 12, "marks": 4, "topic": "3.7", "skills": [], "figs": ["fig-05-fig3.jpg"], "summary": "Explain how Lenz's law predicts the induced current direction in coil Y when the switch is opened and closed."},
    {"qnum": "05.2", "page": 14, "marks": 3, "topic": "3.7", "skills": ["maths", "graph"], "figs": ["fig-05-fig4-6.jpg"], "summary": "Determine the horizontal component BH of the Earth's magnetic flux density from Figure 6."},
    {"qnum": "06.1", "page": 15, "marks": 2, "topic": "3.7", "skills": [], "figs": ["fig-06-passage.jpg"], "summary": "Describe two essential features of a geostationary satellite orbit."},
    {"qnum": "06.2", "page": 15, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": ["fig-06-passage.jpg"], "summary": "Calculate the orbital period in seconds of the polar-orbiting satellite at angular speed 2.5e-4 rad s^-1."},
    {"qnum": "06.3", "page": 15, "marks": 3, "topic": "3.7", "skills": ["maths"], "figs": ["fig-06-passage.jpg"], "summary": "Show that at 12 000 km from the satellite the microwave beam has a width of 1900 km."},
    {"qnum": "06.4", "page": 15, "marks": 3, "topic": "3.7", "skills": ["maths"], "figs": ["fig-06-passage.jpg"], "summary": "Show that a stationary receiver at the South Pole remains in contact for no more than about 20 minutes."},
    {"qnum": "06.5", "page": 16, "marks": 4, "topic": "3.7", "skills": [], "figs": ["fig-06-passage.jpg"], "summary": "Discuss how moving the satellite to a higher orbit affects signal strength and contact time."},
    # Section B MCQs (07 - 31)
    {"qnum": "07", "page": 17, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Identify the correct unit for g^2 / G."},
    {"qnum": "08", "page": 17, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the surface gravitational field strength of a planet with half Earth's radius and quarter mass."},
    {"qnum": "09", "page": 18, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the ratio y/d for the neutral gravitational point between stars of mass M and 4M."},
    {"qnum": "10", "page": 18, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Identify the correct statement about Newton's law of gravitation."},
    {"qnum": "11", "page": 19, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Identify the correct statement when a negative charge is displaced in a non-uniform electric field."},
    {"qnum": "12", "page": 20, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Express the electrostatic force on charge Q midway between parallel plates of separation d and pd V."},
    {"qnum": "13", "page": 20, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Identify the correct statement at closest approach P of an alpha particle deflected by a nucleus."},
    {"qnum": "14", "page": 21, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Find distance r from a point charge where potential rises from 45 V to 50 V when r decreases by 1.5 m."},
    {"qnum": "15", "page": 21, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the new electrostatic force between +Q and -2Q after adding +Q to each and doubling separation."},
    {"qnum": "16", "page": 21, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Identify the incorrect statement about a parallel-plate capacitor."},
    {"qnum": "17", "page": 22, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the pd and number of datalogger readings after one time constant for a 10 mF, 500 ohm discharge."},
    {"qnum": "18", "page": 22, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the mass of a 0.30 m wire carrying 2.0 A floating in a 5.0e-2 T magnetic field."},
    {"qnum": "19", "page": 23, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Express the frequency of circular rotation of a charged particle in a magnetic field B."},
    {"qnum": "20", "page": 23, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Identify the direction of motion and induced emf for a vertical rod moving in a horizontal magnetic field."},
    {"qnum": "21", "page": 24, "marks": 1, "topic": "3.6", "skills": [], "figs": [], "summary": "MCQ: Determine how frequencies of a simple pendulum and mass-spring system change down a mine."},
    {"qnum": "22", "page": 24, "marks": 1, "topic": "3.7", "skills": ["graph"], "figs": [], "summary": "MCQ: Describe the induced emf from a piecewise linear flux linkage vs time graph."},
    {"qnum": "23", "page": 25, "marks": 1, "topic": "3.6", "skills": [], "figs": [], "summary": "MCQ: Identify which change increases the steady-state temperature rise delta-t of a flowing liquid."},
    {"qnum": "24", "page": 26, "marks": 1, "topic": "3.6", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the ratio of specific heat capacity to specific latent heat of fusion from cooling-solidifying data."},
    {"qnum": "25", "page": 26, "marks": 1, "topic": "3.6", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the new volume of a gas at constant pressure when its rms molecular speed doubles."},
    {"qnum": "26", "page": 27, "marks": 1, "topic": "3.6", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the equilibrium pressure when two gas bottles (2V at p, V at 2p) are connected."},
    {"qnum": "27", "page": 27, "marks": 1, "topic": "3.8", "skills": [], "figs": [], "summary": "MCQ: Identify the final nuclide after beta-, alpha, and beta- emissions."},
    {"qnum": "28", "page": 28, "marks": 1, "topic": "3.8", "skills": [], "figs": [], "summary": "MCQ: Identify the best description of the decay constant for a radioisotope."},
    {"qnum": "29", "page": 28, "marks": 1, "topic": "3.8", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the ratio of nuclear radii of Sb-125 and Zn-64."},
    {"qnum": "30", "page": 28, "marks": 1, "topic": "3.8", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the half-life of a nuclide whose activity falls to 1/16 in 64 days."},
    {"qnum": "31", "page": 29, "marks": 1, "topic": "3.8", "skills": ["graph", "maths"], "figs": [], "summary": "MCQ: Estimate the total binding energy of W-184 from the binding energy per nucleon graph."},
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
    print(f"Cropped {len(ms_written)} / {len(ab_qnums)} Section A mark schemes for {PAPER_ID}")

    ms_doc = fitz.open(str(MS_PDF))
    p12 = ms_doc[11]
    mcq_clip = fitz.Rect(110, 198, 705, 360)
    mcq_pix = p12.get_pixmap(clip=mcq_clip, matrix=fitz.Matrix(2.5, 2.5), alpha=False)
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
