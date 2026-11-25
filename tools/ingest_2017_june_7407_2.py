#!/usr/bin/env python3
"""Ingest AQA AS Physics Paper 2 (7407/2) June 2017 into questions.json + img/2017-june-7407-2/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2017-june-7407-2"
QP_PDF = ROOT / "raw_pdfs" / "media_1795607555734_c7e434c2.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795607556546_39a0ea8e.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2017,
    "series": "June",
    "date": "2017-06-08",
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
    {"filename": "fig-01-fig1.jpg", "page": 2, "x0": 48, "y0": 135, "x1": 540, "y1": 465},
    {"filename": "fig-01-fig3.jpg", "page": 5, "x0": 80, "y0": 68, "x1": 510, "y1": 640},
    {"filename": "fig-02-fig5.jpg", "page": 8, "x0": 48, "y0": 70, "x1": 540, "y1": 335},
    {"filename": "fig-02-fig6-8.jpg", "page": 11, "x0": 75, "y0": 68, "x1": 515, "y1": 670},
    {"filename": "fig-03-fig9.jpg", "page": 12, "x0": 48, "y0": 135, "x1": 540, "y1": 620},
    {"filename": "fig-04-fig11.jpg", "page": 16, "x0": 48, "y0": 70, "x1": 540, "y1": 415},
]

QUESTIONS = [
    # Section A
    {"qnum": "01.1", "page": 2, "marks": 1, "topic": "3.5", "skills": ["maths", "practical"], "figs": ["fig-01-fig1.jpg"], "summary": "Calculate the largest resistance R obtainable using two of the four given resistors."},
    {"qnum": "01.2", "page": 2, "marks": 2, "topic": "3.5", "skills": ["maths", "practical"], "figs": ["fig-01-fig1.jpg"], "summary": "Calculate the smallest resistance R obtainable using two of the four given resistors."},
    {"qnum": "01.3", "page": 3, "marks": 1, "topic": "3.5", "skills": ["practical"], "figs": ["fig-01-fig1.jpg"], "summary": "State why the open-circuit voltmeter reading equals the emf of the power supply."},
    {"qnum": "01.4", "page": 3, "marks": 1, "topic": "3.5", "skills": ["practical"], "figs": [], "summary": "Explain why the terminal voltmeter reading V is less than 1.62 V when switch S is closed."},
    {"qnum": "01.5", "page": 4, "marks": 1, "topic": "3.5", "skills": ["maths", "practical"], "figs": [], "summary": "Determine (emf - V) and V/R for the 2.2 ohm and 6.8 ohm series combination."},
    {"qnum": "01.6", "page": 4, "marks": 1, "topic": "3.1", "skills": ["graph", "practical"], "figs": ["fig-01-fig3.jpg"], "summary": "Plot the point from 01.5 onto Figure 3 and draw a best-fit line."},
    {"qnum": "01.7", "page": 4, "marks": 2, "topic": "3.5", "skills": ["graph", "maths", "practical"], "figs": ["fig-01-fig3.jpg"], "summary": "Determine the internal resistance r of the power supply from the gradient of Figure 3."},
    {"qnum": "01.8", "page": 6, "marks": 2, "topic": "3.5", "skills": ["practical"], "figs": ["fig-01-fig1.jpg"], "summary": "Discuss whether the Figure 4 resistor loop is an improvement over the two-resistor method."},
    {"qnum": "02.1", "page": 8, "marks": 1, "topic": "3.1", "skills": ["practical"], "figs": ["fig-02-fig5.jpg"], "summary": "Explain why the student measured the pencil width w at several points along its length."},
    {"qnum": "02.2", "page": 9, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "Determine the percentage uncertainty in the mean width w from Table 1."},
    {"qnum": "02.3", "page": 9, "marks": 2, "topic": "3.1", "skills": ["maths"], "figs": [], "summary": "Determine the diameter d of the cylindrical graphite core given it is 9.0% of the pencil volume."},
    {"qnum": "02.4", "page": 10, "marks": 1, "topic": "3.1", "skills": ["practical"], "figs": ["fig-02-fig6-8.jpg"], "summary": "Read and record the initial pencil length from the vernier scale in Figure 7."},
    {"qnum": "02.5", "page": 10, "marks": 1, "topic": "3.1", "skills": ["practical"], "figs": ["fig-02-fig6-8.jpg"], "summary": "Read and record the new pencil length from the vernier scale in Figure 8."},
    {"qnum": "02.6", "page": 10, "marks": 2, "topic": "3.1", "skills": ["maths", "practical"], "figs": [], "summary": "Calculate the total line length L_1/2 required to halve the original length of the pencil."},
    # Section B
    {"qnum": "03.1", "page": 13, "marks": 3, "topic": "3.3", "skills": ["maths", "graph"], "figs": ["fig-03-fig9.jpg"], "summary": "Show that the wavelength of the monochromatic light in the gravimeter is 600 nm."},
    {"qnum": "03.2", "page": 13, "marks": 2, "topic": "3.3", "skills": ["maths", "graph"], "figs": ["fig-03-fig9.jpg"], "summary": "Determine the phase difference in radians between the incident and reflected waves in Figure 9."},
    {"qnum": "03.3", "page": 14, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the acceleration due to gravity to 3 sf from 2.37e5 interference maxima in 0.120 s."},
    {"qnum": "03.4", "page": 15, "marks": 2, "topic": "3.4", "skills": ["graph", "maths"], "figs": [], "summary": "Determine the gradient of the distance-time graph Figure 10 at t = 0.12 s."},
    {"qnum": "03.5", "page": 15, "marks": 1, "topic": "3.4", "skills": ["graph"], "figs": [], "summary": "State what the gradient of the distance-time graph represents."},
    {"qnum": "04.1", "page": 16, "marks": 2, "topic": "3.2", "skills": ["maths"], "figs": ["fig-04-fig11.jpg"], "summary": "Calculate the specific charge of a Xe+ ion with an appropriate unit."},
    {"qnum": "04.2", "page": 17, "marks": 1, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "Calculate the kinetic energy in joules gained by each 1300 eV xenon ion."},
    {"qnum": "04.3", "page": 17, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Determine the operating time of the ion thruster before 79 kg of xenon is used up."},
    {"qnum": "04.4", "page": 18, "marks": 3, "topic": "3.4", "skills": [], "figs": [], "summary": "Suggest whether He+ or Xe+ ions make a better propellant by comparing speeds and momentum changes."},
    # Section C (MCQs 05 - 34)
    {"qnum": "05", "page": 19, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the average frictional force on a 2.5 kg mass sliding down a 5.0 m ramp."},
    {"qnum": "06", "page": 20, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify which row shows the strong and weak interactions experienced by a hadron or lepton."},
    {"qnum": "07", "page": 21, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Identify which combination of three 1.5 V cells gives 1.5 V emf and 7.5 A maximum current."},
    {"qnum": "08", "page": 22, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Determine proton and neutron numbers in the daughter nucleus after Ni-65 beta-minus decay."},
    {"qnum": "09", "page": 22, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the recoil velocity of a 4.0 kg rifle and total momentum after firing a 10 g bullet."},
    {"qnum": "10", "page": 22, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Order electromagnetic radiations by decreasing wavelength."},
    {"qnum": "11", "page": 23, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Identify the effect of a polariser on an unpolarised electromagnetic wave."},
    {"qnum": "12", "page": 23, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the current in a 2.0 ohm resistor in a three-branch parallel circuit."},
    {"qnum": "13", "page": 24, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the interactions involved in strange particle production and decay."},
    {"qnum": "14", "page": 24, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: State the phase difference between two points P and Q on a first-harmonic standing wave."},
    {"qnum": "15", "page": 25, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Classify momentum, mass, and velocity as scalar or vector quantities."},
    {"qnum": "16", "page": 25, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the unknown object weight on a pivoted metre-ruler balance."},
    {"qnum": "17", "page": 26, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Identify the term for a material that breaks without plastic deformation."},
    {"qnum": "18", "page": 26, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the energy transferred by a 6.5 ohm heating element at 12 V in 5 minutes."},
    {"qnum": "19", "page": 27, "marks": 1, "topic": "3.4", "skills": ["graph", "maths"], "figs": [], "summary": "MCQ: Calculate momentum gained from the area under a force-time graph."},
    {"qnum": "20", "page": 28, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Determine the effect of doubling incident light power on photoelectron Ek(max) and emission rate."},
    {"qnum": "21", "page": 29, "marks": 1, "topic": "3.2", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the Ek(max) vs frequency graph for a metal with a higher work function."},
    {"qnum": "22", "page": 30, "marks": 1, "topic": "3.2", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the graph showing the relationship between photon energy E and wavelength."},
    {"qnum": "23", "page": 30, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: State changes in velocity, frequency, and wavelength when light enters an optically denser medium."},
    {"qnum": "24", "page": 31, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the angle of refraction in glass (n = 1.5) for a ray at 35 degrees to the surface."},
    {"qnum": "25", "page": 31, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Identify how diffraction grating maxima spacing changes with longer wavelength and screen distance."},
    {"qnum": "26", "page": 32, "marks": 1, "topic": "3.1", "skills": [], "figs": [], "summary": "MCQ: Identify which expression cannot be used as a unit for the Young modulus."},
    {"qnum": "27", "page": 32, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the angular separation between the two second-order maxima of a 400 lines/mm grating."},
    {"qnum": "28", "page": 32, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the separation after 1.0 s of two balls, one projected horizontally and one dropped."},
    {"qnum": "29", "page": 33, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Compare total kinetic energy and collision forces in an elastic collision between different masses."},
    {"qnum": "30", "page": 33, "marks": 1, "topic": "3.4", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the incorrect statement about two wires X and Y from their force-extension graphs."},
    {"qnum": "31", "page": 34, "marks": 1, "topic": "3.5", "skills": [], "figs": [], "summary": "MCQ: Identify the correct statement about superconductors."},
    {"qnum": "32", "page": 34, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Determine the new resistance of a wire when both its length and radius are doubled."},
    {"qnum": "33", "page": 35, "marks": 1, "topic": "3.5", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the resistance-temperature graph for an NTC thermistor."},
    {"qnum": "34", "page": 36, "marks": 1, "topic": "3.5", "skills": [], "figs": [], "summary": "MCQ: Determine how ammeter and voltmeter readings change when light intensity on an LDR increases."},
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
    p25 = ms_doc[24]
    mcq_clip = fitz.Rect(60, 98, 500, 375)
    mcq_pix = p25.get_pixmap(clip=mcq_clip, matrix=fitz.Matrix(2.5, 2.5), alpha=False)
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
