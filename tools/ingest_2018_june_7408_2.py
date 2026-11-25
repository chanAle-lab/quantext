#!/usr/bin/env python3
"""Ingest AQA A-level Physics Paper 2 (7408/2) June 2018 into questions.json + img/2018-june-7408-2/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2018-june-7408-2"
QP_PDF = ROOT / "raw_pdfs" / "media_1795609285686_41750593.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795609285683_c13f35b3.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2018,
    "series": "June",
    "date": "2018-06-08",
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
    {"filename": "fig-01-p3.jpg", "page": 3, "x0": 48, "y0": 62, "x1": 540, "y1": 265},
    {"filename": "fig-02-fig2.jpg", "page": 4, "x0": 150, "y0": 250, "x1": 435, "y1": 380},
    {"filename": "fig-03-fig4.jpg", "page": 7, "x0": 85, "y0": 268, "x1": 495, "y1": 450},
    {"filename": "fig-04-fig6.jpg", "page": 10, "x0": 150, "y0": 250, "x1": 430, "y1": 395},
    {"filename": "fig-04-fig8.jpg", "page": 11, "x0": 120, "y0": 368, "x1": 465, "y1": 595},
    {"filename": "fig-05-table1.jpg", "page": 14, "x0": 65, "y0": 280, "x1": 525, "y1": 440},
    {"filename": "fig-06-fig11-12.jpg", "page": 16, "x0": 48, "y0": 62, "x1": 540, "y1": 765},
    {"filename": "fig-07-fig13.jpg", "page": 19, "x0": 48, "y0": 62, "x1": 540, "y1": 575},
]

QUESTIONS = [
    # Section A
    {"qnum": "01.1", "page": 2, "marks": 2, "topic": "3.6", "skills": [], "figs": [], "summary": "Explain what is meant by specific latent heat of fusion."},
    {"qnum": "01.2", "page": 2, "marks": 3, "topic": "3.6", "skills": ["maths"], "figs": ["fig-01-p3.jpg"], "summary": "Calculate the rise in water temperature produced by a 2.7 kW heater in 1.0 hour in a 4.5 m^3 hot tub."},
    {"qnum": "01.3", "page": 3, "marks": 2, "topic": "3.6", "skills": [], "figs": [], "summary": "Explain why the water temperature rise is greater when the circulating pump works at higher speeds."},
    {"qnum": "02.1", "page": 4, "marks": 2, "topic": "3.7", "skills": [], "figs": [], "summary": "Define the electric field strength at a point in an electric field."},
    {"qnum": "02.2", "page": 4, "marks": 3, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "Calculate the point charge Q given zero resultant electric field strength at P between Q and +46 uC."},
    {"qnum": "02.3", "page": 5, "marks": 2, "topic": "3.7", "skills": [], "figs": ["fig-02-fig2.jpg"], "summary": "Explain without calculation whether net work must be done moving a proton from infinity to P."},
    {"qnum": "02.4", "page": 6, "marks": 2, "topic": "3.7", "skills": [], "figs": [], "summary": "Explain the motion of a charged ball suspended in a horizontal uniform electric field after the thread breaks."},
    {"qnum": "03.1", "page": 7, "marks": 2, "topic": "3.7", "skills": [], "figs": [], "summary": "State what is meant by a capacitance of 370 uF."},
    {"qnum": "03.2", "page": 7, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "Calculate the resistance R in a 370 uF charging circuit with a time constant of 1.0 s."},
    {"qnum": "03.3", "page": 8, "marks": 2, "topic": "3.7", "skills": ["graph", "maths"], "figs": ["fig-03-fig4.jpg"], "summary": "Mark the capacitor pd at t = 2.0 s on Figure 5 and sketch the charging pd-time curve."},
    {"qnum": "03.4", "page": 8, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "Calculate the time taken for the charging current to fall to half its initial value."},
    {"qnum": "03.5", "page": 9, "marks": 3, "topic": "3.7", "skills": ["maths"], "figs": ["fig-03-fig4.jpg"], "summary": "Calculate the time taken for the charge on the 370 uF capacitor to reach 3.0 mC."},
    {"qnum": "04.1", "page": 10, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "State Lenz's law."},
    {"qnum": "04.2", "page": 10, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "State how the ammeter reading changes as a bar magnet is moved towards a coil and brought to a halt."},
    {"qnum": "04.3", "page": 10, "marks": 2, "topic": "3.7", "skills": [], "figs": ["fig-04-fig6.jpg"], "summary": "Explain how an induced current from E to F in Figure 6 demonstrates Lenz's law."},
    {"qnum": "04.4", "page": 11, "marks": 2, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "Calculate the time taken to move a 32 mm square coil into a 0.38 T field inducing 2.9e-4 V."},
    {"qnum": "04.5", "page": 12, "marks": 2, "topic": "3.7", "skills": ["maths"], "figs": ["fig-04-fig8.jpg"], "summary": "Calculate the angular speed of the rotating square coil when the maximum induced emf is 5.1 mV."},
    {"qnum": "05.1", "page": 13, "marks": 1, "topic": "3.8", "skills": [], "figs": [], "summary": "Suggest with a reason which type of radiation is most appropriate for sterilising metallic surgical instruments."},
    {"qnum": "05.2", "page": 13, "marks": 1, "topic": "3.8", "skills": [], "figs": [], "summary": "Explain why irradiated surgical instruments do not become radioactive once sterilised."},
    {"qnum": "05.3", "page": 14, "marks": 2, "topic": "3.8", "skills": ["maths", "practical"], "figs": [], "summary": "Explain with calculations why the count-rate data in Table 1 are not consistent with an inverse-square law."},
    {"qnum": "05.4", "page": 15, "marks": 2, "topic": "3.8", "skills": ["practical"], "figs": ["fig-05-table1.jpg"], "summary": "State two possible reasons why the count-rate results do not follow the expected inverse-square law."},
    {"qnum": "06.1", "page": 17, "marks": 1, "topic": "3.8", "skills": ["graph", "maths"], "figs": ["fig-06-fig11-12.jpg"], "summary": "Determine the predicted depth of water at t = 57 s from the exponential decay curve in Figure 12."},
    {"qnum": "06.2", "page": 17, "marks": 1, "topic": "3.8", "skills": ["practical"], "figs": ["fig-06-fig11-12.jpg"], "summary": "Suggest how to change the Figure 11 apparatus to represent a sample with a greater number of nuclei."},
    {"qnum": "06.3", "page": 17, "marks": 1, "topic": "3.8", "skills": ["practical"], "figs": ["fig-06-fig11-12.jpg"], "summary": "Suggest how to change the Figure 11 apparatus to represent a nuclide with a smaller decay constant."},
    {"qnum": "06.4", "page": 17, "marks": 1, "topic": "3.8", "skills": ["maths"], "figs": [], "summary": "Calculate in years the half-life of Rb-87 from its decay constant 1.42e-11 yr^-1."},
    {"qnum": "06.5", "page": 18, "marks": 3, "topic": "3.8", "skills": ["maths"], "figs": [], "summary": "Calculate the initial mass of Rb-87 in a Moon rock sample formed 4.47e9 years ago."},
    {"qnum": "06.6", "page": 18, "marks": 3, "topic": "3.8", "skills": ["maths"], "figs": [], "summary": "Calculate the activity of a 1.23 mg sample of Rb-87 with an appropriate unit."},
    {"qnum": "07.1", "page": 19, "marks": 2, "topic": "3.8", "skills": ["graph"], "figs": ["fig-07-fig13.jpg"], "summary": "Draw four arrows on Figure 13 to show the alpha, beta-, beta-, alpha decay chain to Pb-208."},
    {"qnum": "07.2", "page": 20, "marks": 4, "topic": "3.8", "skills": [], "figs": [], "summary": "Explain why stable Pb-208 has more neutrons than protons in terms of nuclear forces and their ranges."},
    {"qnum": "07.3", "page": 20, "marks": 1, "topic": "3.8", "skills": [], "figs": [], "summary": "Write the nuclear equation for Pb-205 decaying by electron capture to an isotope of thallium."},
    {"qnum": "07.4", "page": 21, "marks": 2, "topic": "3.8", "skills": [], "figs": [], "summary": "Explain the origin and location of two sources of electromagnetic radiation emitted from the thallium atom."},
    {"qnum": "07.5", "page": 21, "marks": 2, "topic": "3.8", "skills": [], "figs": [], "summary": "Explain why metastable Tc-99 is suitable as a radioactive source for medical diagnosis."},
    # Section B (MCQs 08 - 32)
    {"qnum": "08", "page": 22, "marks": 1, "topic": "3.6", "skills": ["graph", "maths"], "figs": [], "summary": "MCQ: Determine the gradient of the pressure vs Celsius temperature graph for an ideal gas."},
    {"qnum": "09", "page": 23, "marks": 1, "topic": "3.6", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the mass ratio of ideal gas in two connected flasks X and Y at 150 K and 300 K."},
    {"qnum": "10", "page": 23, "marks": 1, "topic": "3.6", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the mean square speed of an air molecule at 750 K."},
    {"qnum": "11", "page": 23, "marks": 1, "topic": "3.6", "skills": [], "figs": [], "summary": "MCQ: Identify the cause of the observed Brownian motion of smoke particles in air."},
    {"qnum": "12", "page": 24, "marks": 1, "topic": "3.6", "skills": [], "figs": [], "summary": "MCQ: Identify the vector diagram showing the change in momentum delta(mv) in an elastic wall collision."},
    {"qnum": "13", "page": 25, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the gravitational force exerted on the Sun by the Earth."},
    {"qnum": "14", "page": 25, "marks": 1, "topic": "3.7", "skills": ["graph"], "figs": [], "summary": "MCQ: Compare two equal-radius planets K and L from their gravitational potential vs distance graph."},
    {"qnum": "15", "page": 26, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Identify the direction of the gravitational field at point X on an equipotential diagram."},
    {"qnum": "16", "page": 27, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the surface gravitational potential of planet M with double the density and radius of planet N."},
    {"qnum": "17", "page": 27, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the total change in gravitational potential energy of a spacecraft moving between solar orbits."},
    {"qnum": "18", "page": 28, "marks": 1, "topic": "3.7", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the linear graph relating orbital period T and orbital radius r of a planet."},
    {"qnum": "19", "page": 29, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Express the mean density of the Earth in terms of g, R, and G."},
    {"qnum": "20", "page": 30, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Identify the electric field lines for a +10 uC sphere inside an uncharged conducting sphere."},
    {"qnum": "21", "page": 31, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Express the electric potential of a charged spherical conductor of radius r and surface field E."},
    {"qnum": "22", "page": 32, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the magnitude of the fourth charge at the corner of a square from the centre potential."},
    {"qnum": "23", "page": 33, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Determine the final electric field when an isolated parallel-plate capacitor's separation is doubled."},
    {"qnum": "24", "page": 33, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the relative permittivity of the dielectric in a capacitor with equal capacitance to an air capacitor."},
    {"qnum": "25", "page": 34, "marks": 1, "topic": "3.7", "skills": ["graph"], "figs": [], "summary": "MCQ: Deduce a property of a charging capacitor from its linear pd vs charge graph."},
    {"qnum": "26", "page": 35, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Find the speed of a charged particle leaving two successive magnetic field chambers."},
    {"qnum": "27", "page": 36, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Determine the effect of a magnetic field perpendicular to a circular current-carrying coil."},
    {"qnum": "28", "page": 36, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the primary current and secondary voltage of an 80% efficient transformer."},
    {"qnum": "29", "page": 37, "marks": 1, "topic": "3.8", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the graph of intensity vs angle for electron diffraction by a nucleus."},
    {"qnum": "30", "page": 38, "marks": 1, "topic": "3.8", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the nuclear radius of C-12 given the radius of U-238."},
    {"qnum": "31", "page": 38, "marks": 1, "topic": "3.8", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the number of U-235 fission events per second needed to generate 900 MW at 25% efficiency."},
    {"qnum": "32", "page": 38, "marks": 1, "topic": "3.8", "skills": [], "figs": [], "summary": "MCQ: Identify which substance can be used as a moderator in a nuclear reactor."},
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
    p22 = ms_doc[21]
    mcq_clip = fitz.Rect(45, 78, 595, 270)
    mcq_pix = p22.get_pixmap(clip=mcq_clip, matrix=fitz.Matrix(2.5, 2.5), alpha=False)
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
