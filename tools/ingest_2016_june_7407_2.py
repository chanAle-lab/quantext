#!/usr/bin/env python3
"""Ingest AQA AS Physics Paper 2 (7407/2) June 2016 into questions.json + img/2016-june-7407-2/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2016-june-7407-2"
QP_PDF = ROOT / "raw_pdfs" / "media_1795606549721_5edd2400.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795606549686_f02c126b.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2016,
    "series": "June",
    "date": "2016-06-09",
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
    {"filename": "fig-01-fig1.jpg", "page": 2, "x0": 60, "y0": 138, "x1": 538, "y1": 760},
    {"filename": "fig-01-fig2.jpg", "page": 3, "x0": 110, "y0": 285, "x1": 490, "y1": 765},
    {"filename": "fig-02-table1.jpg", "page": 6, "x0": 60, "y0": 64, "x1": 538, "y1": 725},
    {"filename": "fig-02-fig5.jpg", "page": 7, "x0": 100, "y0": 64, "x1": 495, "y1": 480},
    {"filename": "fig-02-fig6.jpg", "page": 8, "x0": 110, "y0": 115, "x1": 495, "y1": 530},
    {"filename": "fig-03-fig8.jpg", "page": 12, "x0": 60, "y0": 138, "x1": 538, "y1": 600},
]

QUESTIONS = [
    # Section A
    {"qnum": "01.1", "page": 3, "marks": 1, "topic": "3.4", "skills": ["practical"], "figs": ["fig-01-fig1.jpg"], "crop_exclude_y": 290, "summary": "Determine the extension of wire Q from the vernier scale in Figure 1."},
    {"qnum": "01.2", "page": 3, "marks": 1, "topic": "3.4", "skills": ["graph", "practical"], "figs": ["fig-01-fig1.jpg", "fig-01-fig2.jpg"], "crop_exclude_y": 290, "summary": "Determine the mass added to the hanger using Figure 2 and Figure 1."},
    {"qnum": "01.3", "page": 4, "marks": 1, "topic": "3.1", "skills": ["practical"], "figs": [], "summary": "Calculate the true diameter of wire Q correcting for zero error on digital vernier callipers."},
    {"qnum": "01.4", "page": 5, "marks": 4, "topic": "3.4", "skills": ["maths", "practical"], "figs": ["fig-01-fig1.jpg", "fig-01-fig2.jpg"], "summary": "Determine the Young modulus of the metal in wire Q."},
    {"qnum": "01.5", "page": 5, "marks": 4, "topic": "3.1", "skills": ["practical"], "figs": [], "summary": "Discuss two ways using a smaller diameter wire affects the percentage uncertainty in Young modulus."},
    {"qnum": "02.1", "page": 7, "marks": 1, "topic": "3.1", "skills": ["graph", "practical"], "figs": ["fig-02-table1.jpg", "fig-02-fig5.jpg"], "summary": "Plot two missing thermocouple data points onto Figure 5."},
    {"qnum": "02.2", "page": 7, "marks": 1, "topic": "3.1", "skills": ["graph", "practical"], "figs": ["fig-02-fig5.jpg"], "summary": "Draw a suitable best-fit curve on Figure 5."},
    {"qnum": "02.3", "page": 7, "marks": 1, "topic": "3.1", "skills": ["graph"], "figs": ["fig-02-fig5.jpg"], "summary": "Determine the maximum emf from Figure 5."},
    {"qnum": "02.4", "page": 8, "marks": 1, "topic": "3.1", "skills": ["graph"], "figs": ["fig-02-fig5.jpg", "fig-02-fig6.jpg"], "summary": "Explain why a more accurate neutral temperature may be obtained from the gradient graph Figure 6."},
    {"qnum": "02.5", "page": 9, "marks": 2, "topic": "3.1", "skills": ["graph", "maths"], "figs": ["fig-02-fig6.jpg"], "summary": "Determine the vertical intercept constant alpha from G = beta*theta + alpha using Figure 6."},
    {"qnum": "02.6", "page": 10, "marks": 1, "topic": "3.5", "skills": ["maths", "practical"], "figs": [], "summary": "Calculate the full-scale deflection in microvolts of a 100 uA, 1000 ohm meter."},
    {"qnum": "02.7", "page": 10, "marks": 2, "topic": "3.1", "skills": ["practical"], "figs": [], "summary": "Discuss why the 50-division meter is unsuitable for the thermocouple experiment."},
    # Section B
    {"qnum": "03.1", "page": 13, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": ["fig-03-fig8.jpg"], "summary": "Show that the weight of a 5.0 cm diameter steel ball is approximately 5 N."},
    {"qnum": "03.2", "page": 13, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": ["fig-03-fig8.jpg"], "summary": "Calculate the moment of the weight of the ball about the seismometer pivot with an appropriate unit."},
    {"qnum": "03.3", "page": 13, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": ["fig-03-fig8.jpg"], "summary": "Calculate the extension of the supporting spring in equilibrium."},
    {"qnum": "03.4", "page": 14, "marks": 2, "topic": "3.4", "skills": [], "figs": ["fig-03-fig8.jpg"], "summary": "Explain what happens to the line drawn on the drum when the seismometer frame accelerates rapidly downwards."},
    {"qnum": "04.1", "page": 15, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "Complete the nuclear equation for the alpha decay of plutonium-238."},
    {"qnum": "04.2", "page": 15, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the total rate of energy transfer from Pu-238 decay at 6% efficiency for 100 W output."},
    {"qnum": "04.3", "page": 15, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "Calculate the current when the RTG outputs 100 W at 32 V."},
    {"qnum": "04.4", "page": 16, "marks": 2, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "Calculate the maximum number of 45 ohm components that can be connected in parallel across the RTG."},
    {"qnum": "04.5", "page": 16, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the average electrical power output of a UK solar panel providing 1000 kW h per year."},
    {"qnum": "04.6", "page": 16, "marks": 1, "topic": "3.1", "skills": ["maths"], "figs": [], "summary": "Estimate to an order of magnitude the solar panel area needed for 100 W average power on Mars."},
    # Section C (MCQs 05 - 34)
    {"qnum": "05", "page": 17, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify which series of alpha and beta-minus emissions produces an isotope of the original element."},
    {"qnum": "06", "page": 17, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the equation representing particle-antiparticle annihilation."},
    {"qnum": "07", "page": 18, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify which particle is a lepton (not made of quarks)."},
    {"qnum": "08", "page": 18, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: State the quark structure of an antiproton."},
    {"qnum": "09", "page": 18, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Determine charge, baryon number, and strangeness of particle X in a weak interaction."},
    {"qnum": "10", "page": 19, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the hydrogen energy-level transition emitting an ultraviolet photon."},
    {"qnum": "11", "page": 19, "marks": 1, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the de Broglie wavelength of an alpha particle moving at the same speed as a proton."},
    {"qnum": "12", "page": 20, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate phase difference between two points 0.16 m apart on a 256 Hz sound wave."},
    {"qnum": "13", "page": 20, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Determine the new first harmonic frequency when wire length and tension are both doubled."},
    {"qnum": "14", "page": 21, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Identify what causes the separation of diffraction grating maxima to decrease."},
    {"qnum": "15", "page": 21, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Describe the diffraction pattern produced when white light passes through a single narrow slit."},
    {"qnum": "16", "page": 21, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Identify the correct condition for total internal reflection."},
    {"qnum": "17", "page": 22, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the speed of light in glass of refractive index 1.42."},
    {"qnum": "18", "page": 22, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Identify the scalar quantity."},
    {"qnum": "19", "page": 23, "marks": 1, "topic": "3.4", "skills": ["graph"], "figs": [], "summary": "MCQ: Match a falling object's velocity-time graph to its acceleration-time graph."},
    {"qnum": "20", "page": 24, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate average velocity and average speed for a two-stage out-and-back jog."},
    {"qnum": "21", "page": 24, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Estimate maximum height of a golf ball hit on the Moon with a 4.0 s time of flight."},
    {"qnum": "22", "page": 24, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Determine the effect of a perpendicular force on the forward and sideways speeds of a space probe."},
    {"qnum": "23", "page": 25, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Explain why lap time decreases as fuel mass decreases in a racing car."},
    {"qnum": "24", "page": 25, "marks": 1, "topic": "3.4", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the quantity represented by the area under a force-displacement graph."},
    {"qnum": "25", "page": 25, "marks": 1, "topic": "3.1", "skills": [], "figs": [], "summary": "MCQ: Identify which expression is not a unit of power."},
    {"qnum": "26", "page": 26, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the maximum possible speed of a roller coaster car released from 65 m."},
    {"qnum": "27", "page": 26, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the average impact force on a 500 kg car crumpling by 0.30 m from 10 m/s."},
    {"qnum": "28", "page": 26, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the number of electrons passing a point in 2 minutes at 20 mA."},
    {"qnum": "29", "page": 27, "marks": 1, "topic": "3.5", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the I-V characteristic of a resistor and diode in series."},
    {"qnum": "30", "page": 28, "marks": 1, "topic": "3.5", "skills": [], "figs": [], "summary": "MCQ: Identify which circuit change reduces the charge flowing through resistor R in time t."},
    {"qnum": "31", "page": 28, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the resistance of a 132 kV transmission line delivering 800 MW with 1% heat loss."},
    {"qnum": "32", "page": 29, "marks": 1, "topic": "3.5", "skills": [], "figs": [], "summary": "MCQ: Identify which change increases the pd across a thermistor in a potential divider."},
    {"qnum": "33", "page": 30, "marks": 1, "topic": "3.5", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the V-I graph for terminal potential difference across a cell with internal resistance."},
    {"qnum": "34", "page": 31, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the internal resistance of a battery from open-circuit and loaded terminal voltages."},
]


def main() -> None:
    assert sum(q["marks"] for q in QUESTIONS) == PAPER_META["totalMarks"]
    IMG_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Extract shared figures at 2.5x scale
    qp_doc = fitz.open(str(QP_PDF))
    mat = fitz.Matrix(2.5, 2.5)
    for fig in FIGURES:
        page = qp_doc[fig["page"] - 1]
        clip = fitz.Rect(fig["x0"], fig["y0"], fig["x1"], fig["y1"])
        pix = page.get_pixmap(clip=clip, matrix=mat, alpha=False)
        pix.save(str(IMG_DIR / fig["filename"]))
    qp_doc.close()

    # 2. Crop Section A & B official mark schemes
    ab_qnums = [q["qnum"] for q in QUESTIONS if "." in q["qnum"]]
    ms_written = crop_official_markschemes(MS_PDF, ab_qnums, IMG_DIR / "ms")
    print(f"Cropped {len(ms_written)} / {len(ab_qnums)} Section A/B mark schemes for {PAPER_ID}")

    # 3. Crop Section C MCQ Answer Key table (page 14)
    ms_doc = fitz.open(str(MS_PDF))
    p14 = ms_doc[13]
    mcq_clip = fitz.Rect(60, 318, 500, 495)
    mcq_pix = p14.get_pixmap(clip=mcq_clip, matrix=fitz.Matrix(2.5, 2.5), alpha=False)
    mcq_key_rel = f"img/{PAPER_ID}/ms/mcq-key.png"
    mcq_pix.save(str(ROOT / mcq_key_rel))
    ms_doc.close()

    # 4. Update questions.json
    db_path = ROOT / "questions.json"
    db = json.loads(db_path.read_text(encoding="utf-8"))
    db["papers"] = [p for p in db["papers"] if p["id"] != PAPER_ID] + [PAPER_META]
    db["questions"] = [q for q in db["questions"] if q["paper"] != PAPER_ID]

    for q in QUESTIONS:
        slug = q["qnum"].replace(".", "-")
        ms_path = f"img/{PAPER_ID}/ms/q{slug}.png" if "." in q["qnum"] else mcq_key_rel
        entry = {
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
        }
        if "crop_exclude_y" in q:
            entry["crop_exclude_y"] = q["crop_exclude_y"]
        db["questions"].append(entry)

    db_path.write_text(json.dumps(db, indent=2) + "\n", encoding="utf-8")
    print(f"Updated questions.json with {len(QUESTIONS)} questions for {PAPER_ID}")


if __name__ == "__main__":
    main()
