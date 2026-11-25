#!/usr/bin/env python3
"""Ingest AQA AS Physics Paper 2 (7407/2) June 2018 into questions.json + img/2018-june-7407-2/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2018-june-7407-2"
QP_PDF = ROOT / "raw_pdfs" / "media_1795609950291_8c9267fb.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795609951362_32c0cf6d.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2018,
    "series": "June",
    "date": "2018-05-18",
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
    {"filename": "fig-01-fig1.jpg", "page": 2, "x0": 48, "y0": 125, "x1": 540, "y1": 620},
    {"filename": "fig-01-fig2.jpg", "page": 6, "x0": 110, "y0": 155, "x1": 465, "y1": 625},
    {"filename": "fig-02-fig3.jpg", "page": 8, "x0": 48, "y0": 62, "x1": 540, "y1": 500},
    {"filename": "fig-02-fig4.jpg", "page": 9, "x0": 65, "y0": 102, "x1": 515, "y1": 265},
    {"filename": "fig-02-fig5.jpg", "page": 10, "x0": 95, "y0": 130, "x1": 490, "y1": 485},
    {"filename": "fig-02-p13.jpg", "page": 13, "x0": 48, "y0": 62, "x1": 540, "y1": 235},
    {"filename": "fig-03-fig8.jpg", "page": 16, "x0": 90, "y0": 115, "x1": 495, "y1": 295},
    {"filename": "fig-04-p21.jpg", "page": 21, "x0": 48, "y0": 62, "x1": 540, "y1": 225},
]

QUESTIONS = [
    # Section A
    {"qnum": "01.1", "page": 3, "marks": 3, "topic": "3.4", "skills": ["maths", "practical"], "figs": ["fig-01-fig1.jpg"], "summary": "Determine the acceleration a of the air-track glider from the light-gate times in Table 1."},
    {"qnum": "01.2", "page": 4, "marks": 2, "topic": "3.4", "skills": ["practical"], "figs": ["fig-01-fig1.jpg"], "summary": "Explain how the data in Table 2 show that the distance between light gates in set B is greater than in set A."},
    {"qnum": "01.3", "page": 6, "marks": 2, "topic": "3.1", "skills": ["graph", "maths", "practical"], "figs": [], "summary": "Draw a best-fit straight line on Figure 2 and determine its gradient G."},
    {"qnum": "01.4", "page": 7, "marks": 1, "topic": "3.4", "skills": ["maths", "practical"], "figs": [], "summary": "Calculate the thickness h of each block given g = 2G / h and g = 9.8 m s^-2."},
    {"qnum": "01.5", "page": 7, "marks": 1, "topic": "3.1", "skills": ["graph", "practical"], "figs": ["fig-01-fig2.jpg"], "summary": "Explain how to test without drawing another graph whether Figure 2 supports a directly proportional to n."},
    {"qnum": "02.1", "page": 9, "marks": 2, "topic": "3.1", "skills": ["practical"], "figs": ["fig-02-fig3.jpg"], "summary": "State precautions to reduce systematic and random errors when measuring external diameter D with digital calipers."},
    {"qnum": "02.2", "page": 10, "marks": 1, "topic": "3.1", "skills": ["practical"], "figs": ["fig-02-fig3.jpg"], "summary": "Draw the sectional view of ring magnet B on Figure 5 to indicate how internal diameter d is measured."},
    {"qnum": "02.3", "page": 11, "marks": 3, "topic": "3.1", "skills": ["maths", "practical"], "figs": ["fig-02-fig4.jpg", "fig-02-fig5.jpg"], "summary": "Calculate the volume of ring magnet B from the caliper readings in Figures 4, 5, and 6."},
    {"qnum": "02.4", "page": 12, "marks": 5, "topic": "3.1", "skills": ["practical", "graph"], "figs": ["fig-02-p13.jpg"], "summary": "Describe an experiment and graphical analysis to test F = k / h^3 and determine constant k."},
    # Section B
    {"qnum": "03.1", "page": 14, "marks": 2, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "Show that the velocity of an alpha particle with kinetic energy 8.1e-13 J is approximately 2e7 m s^-1."},
    {"qnum": "03.2", "page": 14, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the average force exerted by air on an alpha particle stopped over a range of 3.5 cm."},
    {"qnum": "03.3", "page": 15, "marks": 3, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "Calculate the average ionisation energy in eV of an air molecule from 5.1e4 ions/cm over 3.5 cm."},
    {"qnum": "03.4", "page": 16, "marks": 2, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "Calculate the number of charge carriers passing a point during a 0.85 mA spark lasting 1.2 ns."},
    {"qnum": "03.5", "page": 17, "marks": 3, "topic": "3.5", "skills": [], "figs": ["fig-03-fig8.jpg"], "summary": "Discuss how the pd across the air gap varies as the alpha source is moved from 10 cm towards the wire gauze."},
    {"qnum": "04.1", "page": 19, "marks": 3, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "Calculate the refractive index nB of glass B given nA = 1.461 and light is 3.252% slower in glass B."},
    {"qnum": "04.2", "page": 20, "marks": 3, "topic": "3.3", "skills": ["graph"], "figs": ["fig-04-p21.jpg"], "summary": "Discuss how the reflected wavelength lambda_R changes as a lift starts at rest, accelerates downwards, then moves at constant velocity."},
    {"qnum": "04.3", "page": 22, "marks": 2, "topic": "3.3", "skills": ["graph"], "figs": [], "summary": "Explain whether optical fibre strain gauge P or Q should be selected to measure small accelerations."},
    # Section C (MCQs 05 - 34)
    {"qnum": "05", "page": 23, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify an isotope of nucleus P and its nucleon number from an N-Z graph."},
    {"qnum": "06", "page": 24, "marks": 1, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the number of alpha decays when U-236 decays to Pb-204."},
    {"qnum": "07", "page": 24, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the exchange particle Q and quark structure of particle R in an electron capture diagram."},
    {"qnum": "08", "page": 25, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify products X and Y in the neutral kaon decay K0 -> X + Y + anti-nu_e."},
    {"qnum": "09", "page": 25, "marks": 1, "topic": "3.2", "skills": ["graph"], "figs": [], "summary": "MCQ: State the gradient of the photoelectron Ek vs 1/lambda graph."},
    {"qnum": "10", "page": 26, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the energy level diagram showing UV excitation from ground state followed by visible emission."},
    {"qnum": "11", "page": 27, "marks": 1, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "MCQ: Express the de Broglie wavelength of a particle of mass m and kinetic energy E."},
    {"qnum": "12", "page": 27, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Link the photoelectric effect and electron diffraction to particle and wave properties."},
    {"qnum": "13", "page": 28, "marks": 1, "topic": "3.1", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the percentage uncertainty in the first-harmonic frequency of a stretched string."},
    {"qnum": "14", "page": 28, "marks": 1, "topic": "3.1", "skills": [], "figs": [], "summary": "MCQ: Order forces with prefixes pN, fN, GN, and TN in increasing magnitude."},
    {"qnum": "15", "page": 29, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Determine the path of a light ray incident at 44 degrees on a glass-air boundary (n = 1.5)."},
    {"qnum": "16", "page": 30, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the travel time along optical fibre Q with double the core diameter of fibre P."},
    {"qnum": "17", "page": 31, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Find the lowest frequency heard when a stretched string of fundamental frequency f is touched one third along its length."},
    {"qnum": "18", "page": 32, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the number of lines per mm of a diffraction grating from first-order fringe spacing."},
    {"qnum": "19", "page": 33, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate wave frequency given phase difference pi/6 rad over 0.12 m and speed 340 m s^-1."},
    {"qnum": "20", "page": 33, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the position x of a bird of weight 2W on a uniform rod when tension in P is half tension in Q."},
    {"qnum": "21", "page": 34, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the steady speed of a 950 kg car ascending a 12-degree hill at 6.5e4 W."},
    {"qnum": "22", "page": 34, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Identify the correct statement about a girl's acceleration while bouncing in the air above a trampoline."},
    {"qnum": "23", "page": 35, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Identify which wire extends the least before breaking from stiffness and maximum strain energy data."},
    {"qnum": "24", "page": 35, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Compare terminal velocities of two equal-volume spheres P and Q where P has greater mass."},
    {"qnum": "25", "page": 36, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the time taken for an aircraft to fly distance D due north in a wind blowing at angle theta."},
    {"qnum": "26", "page": 37, "marks": 1, "topic": "3.4", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the momentum-time graph corresponding to a triangular resultant force-time graph."},
    {"qnum": "27", "page": 38, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the kinetic energy ratio of objects P and Q (mP = 10 mQ) accelerated by equal force F for time T."},
    {"qnum": "28", "page": 38, "marks": 1, "topic": "3.5", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the power vs current graph for an ohmic component."},
    {"qnum": "29", "page": 39, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Convert 1.0 kilowatt-hour (kW h) into electron-volts (eV)."},
    {"qnum": "30", "page": 40, "marks": 1, "topic": "3.5", "skills": ["graph"], "figs": [], "summary": "MCQ: Determine the resistance of a non-ohmic component at current I2 from its V-I graph."},
    {"qnum": "31", "page": 41, "marks": 1, "topic": "3.5", "skills": [], "figs": [], "summary": "MCQ: Determine how ammeter readings A1 and A2 change when thermistor temperature decreases in a parallel circuit."},
    {"qnum": "32", "page": 42, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the voltmeter and ammeter readings in a circuit with two 3.0 V cells in parallel and a 12 ohm resistor."},
    {"qnum": "33", "page": 42, "marks": 1, "topic": "3.5", "skills": [], "figs": [], "summary": "MCQ: Identify the base-derived unit expression equivalent to the ohm."},
    {"qnum": "34", "page": 43, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Determine the ammeter and voltmeter readings in a 1.50 V three-resistor parallel-series circuit."},
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
    p16 = ms_doc[15]
    mcq_clip = fitz.Rect(30, 68, 560, 340)
    mcq_pix = p16.get_pixmap(clip=mcq_clip, matrix=fitz.Matrix(2.5, 2.5), alpha=False)
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
