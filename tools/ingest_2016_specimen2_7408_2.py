#!/usr/bin/env python3
"""Ingest AQA A-level Physics Paper 2 (7408/2) Specimen Set 2 into questions.json + img/2016-specimen2-7408-2/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2016-specimen2-7408-2"
QP_PDF = ROOT / "raw_pdfs" / "media_1795693078604_d416da95.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795693078641_956e64cc.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2016,
    "series": "Specimen Set 2",
    "date": "2016-06-01",
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
    {"filename": "fig-01-fig1.jpg", "page": 2, "x0": 115, "y0": 230, "x1": 540, "y1": 650},
    {"filename": "fig-01-fig2.jpg", "page": 3, "x0": 125, "y0": 62, "x1": 545, "y1": 360},
    {"filename": "fig-02-fig4-5.jpg", "page": 6, "x0": 65, "y0": 65, "x1": 540, "y1": 645},
    {"filename": "fig-02-fig6.jpg", "page": 7, "x0": 90, "y0": 270, "x1": 540, "y1": 525},
    {"filename": "fig-03-fig7.jpg", "page": 10, "x0": 90, "y0": 70, "x1": 540, "y1": 330},
    {"filename": "fig-05-fig8.jpg", "page": 14, "x0": 55, "y0": 62, "x1": 540, "y1": 255},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "Explain what is meant by a capacitance of 120 uF."},
    {"qnum": "01.2", "page": 2, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "Setup for Figure 1 capacitor-discharge speed measurement."},
    {"qnum": "01.3", "page": 3, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": ["fig-01-fig1.jpg", "fig-01-fig2.jpg"], "summary": "Calculate the charge passing through the resistor and the maximum current during discharge."},
    {"qnum": "01.4", "page": 4, "marks": 3, "topic": "3.7", "skills": ["maths"], "figs": ["fig-01-fig2.jpg"], "summary": "Calculate the energy transferred as the capacitor discharges through the 1.3 kohm resistor."},
    {"qnum": "01.5", "page": 4, "marks": 3, "topic": "3.7", "skills": ["graph", "maths"], "figs": ["fig-01-fig2.jpg"], "summary": "Sketch on Figure 3 the variation of the magnitude of current in the resistor with a current scale."},
    {"qnum": "01.6", "page": 5, "marks": 4, "topic": "3.7", "skills": ["maths"], "figs": ["fig-01-fig1.jpg", "fig-01-fig2.jpg"], "summary": "Calculate the capacitor discharge time and hence determine the mean speed of the steel ball."},
    {"qnum": "01.7", "page": 5, "marks": 2, "topic": "3.7", "skills": ["practical"], "figs": [], "summary": "Discuss two reasons why the calculated mean speed is likely lower than the initial speed."},
    {"qnum": "02.1", "page": 6, "marks": 1, "topic": "3.2", "skills": [], "figs": ["fig-02-fig4-5.jpg"], "summary": "Explain what is meant by ionisation in the context of the mass spectrometer."},
    {"qnum": "02.2", "page": 7, "marks": 3, "topic": "3.7", "skills": [], "figs": ["fig-02-fig4-5.jpg"], "summary": "Discuss the energy transfers that take place in the accelerator as the ion passes through it."},
    {"qnum": "02.3", "page": 7, "marks": 3, "topic": "3.7", "skills": [], "figs": [], "summary": "Discuss how the path changes when an ion enters the velocity selector with velocity greater than v."},
    {"qnum": "02.4", "page": 7, "marks": 1, "topic": "3.7", "skills": [], "figs": ["fig-02-fig6.jpg"], "summary": "Draw on Figure 6 the path of the faster ion in the velocity selector."},
    {"qnum": "02.5", "page": 8, "marks": 2, "topic": "3.7", "skills": [], "figs": ["fig-02-fig4-5.jpg"], "summary": "Discuss how the path of an ion in the mass separator is affected when it has more nucleons."},
    {"qnum": "02.6", "page": 8, "marks": 3, "topic": "3.7", "skills": [], "figs": ["fig-02-fig4-5.jpg"], "summary": "Compare with justification the path of a doubly charged ion with a singly charged ion of the same mass."},
    {"qnum": "03.1", "page": 10, "marks": 2, "topic": "3.7", "skills": ["maths"], "figs": ["fig-03-fig7.jpg"], "summary": "Calculate the electric potential energy, in J, of the 4.9 MeV alpha particle at closest approach S."},
    {"qnum": "03.2", "page": 10, "marks": 3, "topic": "3.7", "skills": ["maths"], "figs": ["fig-03-fig7.jpg"], "summary": "Calculate r, the distance of closest approach of the alpha particle to the gold nucleus."},
    {"qnum": "03.3", "page": 11, "marks": 3, "topic": "3.8", "skills": ["maths"], "figs": [], "summary": "Determine the number of nucleons in the gold nucleus from R = 7.16 x 10^-15 m and R0 = 1.23 x 10^-15 m."},
    {"qnum": "03.4", "page": 11, "marks": 2, "topic": "3.7", "skills": [], "figs": [], "summary": "Explain how the distance of closest approach r changes when the target nucleus has fewer protons."},
    {"qnum": "04.1", "page": 12, "marks": 2, "topic": "3.7", "skills": [], "figs": [], "summary": "Define the gravitational potential at a point."},
    {"qnum": "04.2", "page": 12, "marks": 2, "topic": "3.7", "skills": [], "figs": [], "summary": "Explain why gravitational potential is always negative."},
    {"qnum": "04.3", "page": 12, "marks": 2, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "Show that the magnitude of gravitational potential at Earth's surface is about 6.3 x 10^7 J kg^-1."},
    {"qnum": "04.4", "page": 12, "marks": 2, "topic": "3.7", "skills": [], "figs": [], "summary": "Describe and explain two features of a geostationary orbit."},
    {"qnum": "04.5", "page": 13, "marks": 3, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "Calculate the gain in gravitational potential energy of a 1200 kg satellite placed at radius 4.23 x 10^7 m."},
    {"qnum": "04.6", "page": 13, "marks": 4, "topic": "3.7", "skills": [], "figs": [], "summary": "Discuss changes to the orbital motion when the satellite is placed into an orbit with a longer period."},
    {"qnum": "05.1", "page": 14, "marks": 1, "topic": "3.7", "skills": [], "figs": ["fig-05-fig8.jpg"], "summary": "Explain the purpose of the core in the step-down transformer."},
    {"qnum": "05.2", "page": 14, "marks": 2, "topic": "3.7", "skills": [], "figs": [], "summary": "Describe and explain two features of the transformer core that improve efficiency."},
    {"qnum": "05.3", "page": 14, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "Explain why transformers only work continuously when supplied with an alternating current."},
    {"qnum": "05.4", "page": 15, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "Calculate the number of turns on the primary coil of the 230 V to 20 V transformer."},
    {"qnum": "05.5", "page": 15, "marks": 2, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "Calculate the efficiency of the transformer."},
    # Section B MCQs (06 - 30)
    {"qnum": "06", "page": 16, "marks": 1, "topic": "3.6", "skills": ["maths"], "figs": [], "summary": "MCQ: Estimate the maximum temperature change when 0.010 kg ice at 0 C is dropped into 0.10 kg water at 15 C."},
    {"qnum": "07", "page": 16, "marks": 1, "topic": "3.6", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the number of molecules per unit volume in gas Q at 350 K and equal pressure to P at 280 K."},
    {"qnum": "08", "page": 17, "marks": 1, "topic": "3.6", "skills": [], "figs": [], "summary": "MCQ: Identify which statement is not a valid assumption in deriving p = (1/3) N m (c_rms)^2."},
    {"qnum": "09", "page": 17, "marks": 1, "topic": "3.6", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the correct pV against Celsius temperature graph for one mole of nitrogen and oxygen."},
    {"qnum": "10", "page": 18, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the distance from Earth's centre where a spacecraft experiences zero resultant gravitational force."},
    {"qnum": "11", "page": 18, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the ratio of electric force to gravitational force on an electron in a 5000 N C^-1 field."},
    {"qnum": "12", "page": 18, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Find gravitational potential at distance 2R when surface potential is -4000 J kg^-1."},
    {"qnum": "13", "page": 19, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Identify the incorrect statement comparing satellites X and Y at orbital radii R and 4R."},
    {"qnum": "14", "page": 19, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the electrostatic force on a gold nucleus at closest approach 4.0 x 10^-14 m to an alpha particle."},
    {"qnum": "15", "page": 20, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Identify what is true about the force on an electron entering a uniform electric field at right angles."},
    {"qnum": "16", "page": 20, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the electric field strength midway between point charges +4 uC and -8 uC separated by 2.0 m."},
    {"qnum": "17", "page": 21, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the capacitance of a capacitor whose stored energy decreases by 0.030 J as pd drops from 60 V to 10 V."},
    {"qnum": "18", "page": 21, "marks": 1, "topic": "3.7", "skills": [], "figs": [], "summary": "MCQ: Identify what increases when the plate separation of an isolated charged capacitor is increased."},
    {"qnum": "19", "page": 21, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the energy stored in a 0.50 uF capacitor initially at 2.0 uC after one time constant."},
    {"qnum": "20", "page": 22, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the time for pd across a 500 uF capacitor discharging through 100 kohm to halve."},
    {"qnum": "21", "page": 22, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the number of electrons per second in a horizontal wire supported by a 0.16 T magnetic field."},
    {"qnum": "22", "page": 22, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Identify the mass and charge of particle P2 moving in a circle of half the radius of P1."},
    {"qnum": "23", "page": 23, "marks": 1, "topic": "3.7", "skills": ["maths"], "figs": [], "summary": "MCQ: Find initial and final magnetic flux linkage of a coil rotated by 30 deg from parallel to B."},
    {"qnum": "24", "page": 23, "marks": 1, "topic": "3.8", "skills": [], "figs": [], "summary": "MCQ: Identify the Rutherford scattering deduction from most alpha particles passing undeflected."},
    {"qnum": "25", "page": 24, "marks": 1, "topic": "3.1", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the oscilloscope trace when sensitivity changes from 1 to 2 V/div and time base from 10 to 20 ms/div."},
    {"qnum": "26", "page": 24, "marks": 1, "topic": "3.8", "skills": [], "figs": [], "summary": "MCQ: Identify the correct property of beta particles emitted in a school laboratory."},
    {"qnum": "27", "page": 25, "marks": 1, "topic": "3.8", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the average count rate after 24 hours given half-life 12 h and background 20 cpm."},
    {"qnum": "28", "page": 25, "marks": 1, "topic": "3.8", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the graph showing how nuclear radius R varies with nucleon number A."},
    {"qnum": "29", "page": 26, "marks": 1, "topic": "3.8", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the maximum power output of a reactor losing 4.0 x 10^-6 kg hour^-1 of mass."},
    {"qnum": "30", "page": 26, "marks": 1, "topic": "3.8", "skills": [], "figs": [], "summary": "MCQ: State the principal purpose of the graphite moderator in a nuclear reactor."},
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
