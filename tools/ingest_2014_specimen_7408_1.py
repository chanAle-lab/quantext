#!/usr/bin/env python3
"""Ingest AQA A-level Physics Paper 1 (7408/1) Specimen 2014 into questions.json + img/2014-specimen-7408-1/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2014-specimen-7408-1"
QP_PDF = ROOT / "raw_pdfs" / "media_1795692434197_e730130f.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795692434109_aa47fbdb.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2014,
    "series": "Specimen",
    "date": "2014-10-08",
    "code": "7408/1",
    "unit": "A-level Paper 1",
    "level": "A",
    "spec": "current",
    "totalMarks": 85,
    "duration": "2 hours",
    "pdf": None,
    "ms": None,
}

FIGURES = [
    {"filename": "fig-02-fig1.jpg", "page": 4, "x0": 180, "y0": 125, "x1": 400, "y1": 318},
    {"filename": "fig-03-fig2.jpg", "page": 8, "x0": 55, "y0": 75, "x1": 530, "y1": 275},
    {"filename": "fig-04-fig3.jpg", "page": 10, "x0": 120, "y0": 135, "x1": 470, "y1": 420},
    {"filename": "fig-05-table1.jpg", "page": 13, "x0": 125, "y0": 115, "x1": 525, "y1": 205},
    {"filename": "fig-06-passage.jpg", "page": 14, "x0": 55, "y0": 75, "x1": 535, "y1": 435},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "Determine the number of protons and neutrons in one americium-241 nucleus."},
    {"qnum": "01.2", "page": 2, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "State and explain the decay process producing americium-241 from plutonium-241."},
    {"qnum": "01.3", "page": 3, "marks": 3, "topic": "3.2", "skills": [], "figs": [], "summary": "Write the alpha-decay equation for americium-241 and find A and Z of daughter nuclide X."},
    {"qnum": "01.4", "page": 3, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "State what is meant by ionisation."},
    {"qnum": "01.5", "page": 3, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "Explain why a smoke detector containing americium-241 poses no risk to the user."},
    {"qnum": "02.1", "page": 4, "marks": 1, "topic": "3.4", "skills": ["graph"], "figs": ["fig-02-fig1.jpg"], "summary": "Mark point P on Figure 1 where Hooke's law is no longer obeyed."},
    {"qnum": "02.2", "page": 4, "marks": 3, "topic": "3.4", "skills": ["practical", "graph"], "figs": ["fig-02-fig1.jpg"], "summary": "Outline how to use Figure 1 and other measurements to determine the Young modulus of the wire."},
    {"qnum": "02.3", "page": 5, "marks": 1, "topic": "3.4", "skills": ["graph"], "figs": ["fig-02-fig1.jpg"], "summary": "Draw on Figure 1 the unloading force-extension curve from point A."},
    {"qnum": "02.4", "page": 5, "marks": 2, "topic": "3.4", "skills": ["graph"], "figs": ["fig-02-fig1.jpg"], "summary": "Explain why the unloading force-extension graph has its drawn shape."},
    {"qnum": "02.5", "page": 5, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the force needed to produce a 0.20% strain in a 6.0 mm steel cable."},
    {"qnum": "02.6", "page": 5, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Determine the maximum upward acceleration of a 600 kg mass without exceeding 0.20% strain."},
    {"qnum": "02.7", "page": 6, "marks": 3, "topic": "3.4", "skills": [], "figs": [], "summary": "Discuss cable changes to lift a 1200 kg load at the same acceleration without exceeding 0.20% strain."},
    {"qnum": "03.1", "page": 8, "marks": 1, "topic": "3.5", "skills": [], "figs": ["fig-03-fig2.jpg"], "summary": "Write down the relationship between currents I1, I2, and I3 in Figure 2."},
    {"qnum": "03.2", "page": 8, "marks": 1, "topic": "3.5", "skills": [], "figs": ["fig-03-fig2.jpg"], "summary": "State the potential difference across R3 when R1 = 0 ohm."},
    {"qnum": "03.3", "page": 8, "marks": 2, "topic": "3.5", "skills": ["maths"], "figs": ["fig-03-fig2.jpg"], "summary": "Determine the current I2 when R1 = 0 ohm."},
    {"qnum": "03.4", "page": 9, "marks": 3, "topic": "3.5", "skills": [], "figs": ["fig-03-fig2.jpg"], "summary": "State and explain what happens to the pd across R2 as R1 increases from zero."},
    {"qnum": "04.1", "page": 10, "marks": 4, "topic": "3.4", "skills": ["maths"], "figs": ["fig-04-fig3.jpg"], "summary": "Determine the speed of an 8.80 g pellet that embeds in a 450 g ballistic pendulum rising 0.63 m."},
    {"qnum": "04.2", "page": 11, "marks": 4, "topic": "3.4", "skills": [], "figs": ["fig-04-fig3.jpg"], "summary": "Compare the height reached by a steel block when the pellet rebounds, comparing energy and momentum changes."},
    {"qnum": "04.3", "page": 11, "marks": 2, "topic": "3.4", "skills": [], "figs": [], "summary": "Discuss whether the wooden or steel block experiment gives a more accurate pellet velocity."},
    {"qnum": "05.1", "page": 12, "marks": 3, "topic": "3.3", "skills": [], "figs": [], "summary": "Describe the structure of a step-index optical fibre and the purpose of its core and cladding."},
    {"qnum": "05.2", "page": 13, "marks": 2, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "Explain how the difference in refractive index for blue and red light changes a white-light pulse."},
    {"qnum": "05.3", "page": 13, "marks": 2, "topic": "3.3", "skills": [], "figs": ["fig-05-table1.jpg"], "summary": "Discuss two changes to reduce material pulse broadening in the optical fibre."},
    {"qnum": "06.1", "page": 14, "marks": 1, "topic": "3.3", "skills": ["practical"], "figs": ["fig-06-passage.jpg"], "summary": "Suggest an experiment that demonstrates the wave nature of sound."},
    {"qnum": "06.2", "page": 15, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": ["fig-06-passage.jpg"], "summary": "Calculate the time between seeing a gun flash and hearing the bang over 2.5 km using Gassendi's speed."},
    {"qnum": "06.3", "page": 15, "marks": 1, "topic": "3.3", "skills": [], "figs": ["fig-06-passage.jpg"], "summary": "Explain why Gassendi assumed the speed of light is infinite compared with the speed of sound."},
    {"qnum": "06.4", "page": 15, "marks": 2, "topic": "3.3", "skills": [], "figs": ["fig-06-passage.jpg"], "summary": "Explain one observation showing that the speed of sound does not depend on frequency."},
    {"qnum": "06.5", "page": 16, "marks": 1, "topic": "3.1", "skills": [], "figs": ["fig-06-passage.jpg"], "summary": "Explain why Borelli and Viviani's value of 350 m s^-1 was much better than Gassendi's."},
    {"qnum": "06.6", "page": 16, "marks": 2, "topic": "3.3", "skills": ["maths"], "figs": ["fig-06-passage.jpg"], "summary": "Calculate the constant k in c = k sqrt(theta + 273.15) using data from the passage."},
    {"qnum": "06.7", "page": 16, "marks": 2, "topic": "3.1", "skills": [], "figs": [], "summary": "State the steps taken by the scientific community for a measured value to be accepted."},
    # Section B MCQs (07 - 31)
    {"qnum": "07", "page": 17, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the product nucleus when Be-9 captures a proton and emits an alpha particle."},
    {"qnum": "08", "page": 17, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the correct statement comparing X-rays with UV radiation."},
    {"qnum": "09", "page": 18, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify which property of light source A must exceed source B to emit photoelectrons."},
    {"qnum": "10", "page": 18, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Compare strain, stress, tension, and elastic energy in two copper wires X and Y in series."},
    {"qnum": "11", "page": 19, "marks": 1, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the new de Broglie wavelength of an electron when its kinetic energy increases from E to 4E."},
    {"qnum": "12", "page": 20, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Identify the string shape after two opposite wave pulses have passed through each other."},
    {"qnum": "13", "page": 21, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Identify which wave quantities change when monochromatic light passes from air into glass."},
    {"qnum": "14", "page": 21, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: State which quantity increases when light intensity increases in a photocell."},
    {"qnum": "15", "page": 21, "marks": 1, "topic": "3.5", "skills": [], "figs": [], "summary": "MCQ: Determine how ammeter and voltmeter readings change when variable resistor R decreases."},
    {"qnum": "16", "page": 22, "marks": 1, "topic": "3.5", "skills": [], "figs": [], "summary": "MCQ: Identify which statement is not equal to the emf of the cell."},
    {"qnum": "17", "page": 22, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Identify the correct statement for 490 nm light incident on a 6e5 lines/m diffraction grating."},
    {"qnum": "18", "page": 23, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the particles present after an electron ionises a neutral atom."},
    {"qnum": "19", "page": 23, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Identify which resultant magnitude cannot be formed by forces of 6 N and 10 N."},
    {"qnum": "20", "page": 23, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the minimum length l of a wheel wrench applying two 500 N couple forces."},
    {"qnum": "21", "page": 24, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Compare vertical and angled projections of two ballbearings X and Y."},
    {"qnum": "22", "page": 24, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: State the proportionality between distance y and fall time x from rest."},
    {"qnum": "23", "page": 24, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the work done by a 500 N driving force at 72 km h^-1 in 5 minutes."},
    {"qnum": "24", "page": 25, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the initial accelerations of 1 kg and 2 kg masses when the connecting string breaks."},
    {"qnum": "25", "page": 25, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the velocity of a freely falling object after falling distance 2d."},
    {"qnum": "26", "page": 26, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the efficiency of a 100 W motor raising a 10 kg mass at 0.5 m s^-1."},
    {"qnum": "27", "page": 27, "marks": 1, "topic": "3.4", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the resultant force-time graph corresponding to an S-shaped velocity-time graph."},
    {"qnum": "28", "page": 28, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Identify direct experimental evidence that light is a transverse wave."},
    {"qnum": "29", "page": 28, "marks": 1, "topic": "3.6", "skills": ["maths"], "figs": [], "summary": "MCQ: Express the hanging mass M in terms of m, v, r, and g for horizontal circular motion."},
    {"qnum": "30", "page": 29, "marks": 1, "topic": "3.6", "skills": ["maths"], "figs": [], "summary": "MCQ: Identify which SHM quantity doubles when frequency doubles at constant amplitude."},
    {"qnum": "31", "page": 29, "marks": 1, "topic": "3.6", "skills": [], "figs": [], "summary": "MCQ: Identify the correct statement about the acceleration of a particle in undamped SHM."},
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
    p13 = ms_doc[12]
    mcq_clip = fitz.Rect(48, 162, 750, 345)
    mcq_pix = p13.get_pixmap(clip=mcq_clip, matrix=fitz.Matrix(2.5, 2.5), alpha=False)
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
