#!/usr/bin/env python3
"""Ingest AQA AS Physics Paper 1 (7407/1) June 2016 into questions.json + img/2016-june-7407-1/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2016-june-7407-1"
QP_PDF = ROOT / "raw_pdfs" / "media_1795606549697_d45dbf3f.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795606549706_7b3b1541.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2016,
    "series": "June",
    "date": "2016-05-24",
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
    {"filename": "fig-01-fig1.jpg", "page": 2, "x0": 60, "y0": 112, "x1": 538, "y1": 352},
    {"filename": "fig-01-fig2.jpg", "page": 3, "x0": 120, "y0": 344, "x1": 480, "y1": 530},
    {"filename": "fig-02-fig3.jpg", "page": 6, "x0": 60, "y0": 64, "x1": 538, "y1": 292},
    {"filename": "fig-02-fig4.jpg", "page": 7, "x0": 60, "y0": 140, "x1": 538, "y1": 290},
    {"filename": "fig-03-fig5.jpg", "page": 8, "x0": 60, "y0": 64, "x1": 538, "y1": 305},
    {"filename": "fig-04-fig6.jpg", "page": 11, "x0": 60, "y0": 64, "x1": 538, "y1": 380},
    {"filename": "fig-04-fig7.jpg", "page": 12, "x0": 100, "y0": 105, "x1": 500, "y1": 350},
    {"filename": "fig-05-fig8.jpg", "page": 14, "x0": 60, "y0": 64, "x1": 538, "y1": 298},
    {"filename": "fig-06-passage.jpg", "page": 17, "x0": 60, "y0": 64, "x1": 538, "y1": 225},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 1, "topic": "3.4", "skills": [], "figs": ["fig-01-fig1.jpg"], "summary": "State what happens to the momentum of air passing through a jet engine."},
    {"qnum": "01.2", "page": 2, "marks": 3, "topic": "3.4", "skills": [], "figs": ["fig-01-fig1.jpg"], "summary": "Explain, using Newton's laws of motion, why the air exerts a forward force on the engine."},
    {"qnum": "01.3", "page": 3, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": ["fig-01-fig1.jpg"], "summary": "Calculate the thrust force exerted on the jet engine from mass flow rate and speed increase."},
    {"qnum": "01.4", "page": 3, "marks": 2, "topic": "3.4", "skills": [], "figs": ["fig-01-fig2.jpg"], "summary": "Explain why the momentum of air deflected at an angle changes even when its speed is unchanged."},
    {"qnum": "01.5", "page": 4, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the deceleration of an aircraft given the horizontal braking force and mass."},
    {"qnum": "01.6", "page": 4, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the stopping distance of the aircraft along the runway assuming constant deceleration."},
    {"qnum": "01.7", "page": 4, "marks": 2, "topic": "3.4", "skills": [], "figs": [], "summary": "Suggest why the decelerating force provided by the deflector plates may not remain constant in practice."},
    {"qnum": "02.1", "page": 6, "marks": 2, "topic": "3.3", "skills": [], "figs": ["fig-02-fig3.jpg"], "summary": "Suggest how stationary waves are formed inside a microwave oven."},
    {"qnum": "02.2", "page": 7, "marks": 2, "topic": "3.3", "skills": ["practical"], "figs": ["fig-02-fig4.jpg"], "summary": "Explain why a stationary chocolate bar melts only at specific positions in a microwave oven."},
    {"qnum": "02.3", "page": 7, "marks": 5, "topic": "3.3", "skills": ["maths", "practical"], "figs": ["fig-02-fig4.jpg"], "summary": "Calculate the frequency of the microwaves by taking measurements from the full-sized Figure 4 diagram."},
    {"qnum": "02.4", "page": 7, "marks": 1, "topic": "3.3", "skills": ["practical"], "figs": [], "summary": "Explain why most microwave ovens use a rotating turntable during cooking."},
    {"qnum": "03.1", "page": 8, "marks": 2, "topic": "3.4", "skills": [], "figs": [], "summary": "Define tensile stress and tensile strain."},
    {"qnum": "03.2", "page": 8, "marks": 2, "topic": "3.4", "skills": ["graph"], "figs": ["fig-03-fig5.jpg"], "summary": "Identify a mechanical property of material A using evidence from the stress-strain graph."},
    {"qnum": "03.3", "page": 9, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the tensile force at the breaking point of a cylindrical specimen of material A."},
    {"qnum": "03.4", "page": 9, "marks": 6, "topic": "3.4", "skills": ["graph"], "figs": ["fig-03-fig5.jpg"], "summary": "Discuss which of materials A-D is most suitable for a lift cable and a bungee rope, and why others are rejected."},
    {"qnum": "04.1", "page": 11, "marks": 3, "topic": "3.5", "skills": ["maths", "practical"], "figs": ["fig-04-fig6.jpg"], "summary": "Calculate the diameter of an unused corrosion-probe wire from its resistance, length, and resistivity."},
    {"qnum": "04.2", "page": 12, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": ["fig-04-fig7.jpg"], "summary": "Calculate the total resistance of the parallel-arm probe circuit."},
    {"qnum": "04.3", "page": 12, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": ["fig-04-fig7.jpg"], "summary": "Calculate the current in resistor R3 in the probe circuit."},
    {"qnum": "04.4", "page": 13, "marks": 3, "topic": "3.5", "skills": ["maths"], "figs": ["fig-04-fig7.jpg"], "summary": "Calculate the resistance of the working probe when R1 is 2.4 ohm."},
    {"qnum": "04.5", "page": 13, "marks": 2, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "Calculate the percentage change in the probe's diameter when its resistance increases by 1.6%."},
    {"qnum": "04.6", "page": 13, "marks": 2, "topic": "3.5", "skills": [], "figs": ["fig-04-fig7.jpg"], "summary": "Explain without calculation why a voltmeter across AB does not change when the cell is replaced with one having internal resistance."},
    {"qnum": "05.1", "page": 14, "marks": 3, "topic": "3.2", "skills": [], "figs": ["fig-05-fig8.jpg"], "summary": "Explain why a photocell produces a current only above a threshold frequency."},
    {"qnum": "05.2", "page": 14, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "State and explain the effect on photocurrent when the intensity of radiation is increased."},
    {"qnum": "05.3", "page": 15, "marks": 3, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "Calculate the maximum kinetic energy in joules of photoelectrons emitted from a surface of work function 2.1 eV."},
    {"qnum": "05.4", "page": 16, "marks": 1, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "Calculate the stopping potential using the maximum kinetic energy from 05.3."},
    {"qnum": "05.5", "page": 16, "marks": 3, "topic": "3.2", "skills": [], "figs": [], "summary": "Explain the effect of increasing the radiation frequency on the stopping potential."},
    {"qnum": "06.1", "page": 17, "marks": 2, "topic": "3.2", "skills": [], "figs": ["fig-06-passage.jpg"], "summary": "State what is meant by isotopes."},
    {"qnum": "06.2", "page": 17, "marks": 2, "topic": "3.2", "skills": [], "figs": ["fig-06-passage.jpg"], "summary": "Explain why two photons are formed instead of one when helium annihilates with anti-helium."},
    {"qnum": "06.3", "page": 18, "marks": 4, "topic": "3.2", "skills": ["maths"], "figs": ["fig-06-passage.jpg"], "summary": "Calculate the maximum frequency of the photons produced in the helium/anti-helium annihilation."},
    {"qnum": "06.4", "page": 18, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "Complete the decay equation for an antineutron decaying into an antiproton."},
    {"qnum": "06.5", "page": 18, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "Identify the fundamental interaction responsible for antineutron decay."},
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

    # 2. Crop official mark schemes
    qnums = [q["qnum"] for q in QUESTIONS]
    ms_written = crop_official_markschemes(MS_PDF, qnums, IMG_DIR / "ms")
    print(f"Cropped {len(ms_written)} / {len(qnums)} mark schemes for {PAPER_ID}")

    # 3. Update questions.json
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
