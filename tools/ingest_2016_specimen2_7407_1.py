#!/usr/bin/env python3
"""Ingest AQA AS Physics Paper 1 (7407/1) Specimen Set 2 into questions.json + img/2016-specimen2-7407-1/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2016-specimen2-7407-1"
QP_PDF = ROOT / "raw_pdfs" / "media_1795693525046_f1ce46cc.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795693525040_aee808bb.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2016,
    "series": "Specimen Set 2",
    "date": "2016-06-01",
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
    {"filename": "fig-02-fig1.jpg", "page": 4, "x0": 115, "y0": 68, "x1": 545, "y1": 395},
    {"filename": "fig-03-fig2.jpg", "page": 6, "x0": 115, "y0": 75, "x1": 545, "y1": 325},
    {"filename": "fig-06-fig5.jpg", "page": 12, "x0": 115, "y0": 68, "x1": 535, "y1": 510},
    {"filename": "fig-07-fig7.jpg", "page": 15, "x0": 55, "y0": 75, "x1": 535, "y1": 335},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "Identify the quark-antiquark composition for a meson."},
    {"qnum": "01.2", "page": 2, "marks": 3, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "Show that each photon created when a 2.0 keV positron annihilates with an electron at rest has energy 8.2 x 10^-14 J."},
    {"qnum": "01.3", "page": 2, "marks": 2, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "Calculate the wavelength of a photon of energy 8.2 x 10^-14 J."},
    {"qnum": "01.4", "page": 3, "marks": 3, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "Show that the speed of the 2.0 keV positron before the collision was about 2.7 x 10^7 m s^-1."},
    {"qnum": "01.5", "page": 3, "marks": 2, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "Calculate the de Broglie wavelength of the positron travelling at 2.7 x 10^7 m s^-1."},
    {"qnum": "01.6", "page": 3, "marks": 4, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "Discuss whether electrons of this de Broglie wavelength can demonstrate diffraction through graphite (0.15 nm spacing)."},
    {"qnum": "02.1", "page": 4, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": ["fig-02-fig1.jpg"], "summary": "Show that the maximum possible speed of water arriving at the turbine after falling 90 m is about 40 m s^-1."},
    {"qnum": "02.2", "page": 4, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": ["fig-02-fig1.jpg"], "summary": "Estimate the radius of the intake pipe for a water flow rate of 3.5 m^3 s^-1."},
    {"qnum": "02.3", "page": 5, "marks": 4, "topic": "3.4", "skills": ["maths"], "figs": ["fig-02-fig1.jpg"], "summary": "Calculate the maximum possible power output of the turbine and generator when water leaves at 12 m s^-1."},
    {"qnum": "02.4", "page": 5, "marks": 2, "topic": "3.4", "skills": [], "figs": [], "summary": "Explain two possible reasons for energy losses reducing the output power to 60%."},
    {"qnum": "03.1", "page": 6, "marks": 2, "topic": "3.4", "skills": [], "figs": [], "summary": "State the principle of moments."},
    {"qnum": "03.2", "page": 6, "marks": 4, "topic": "3.4", "skills": ["maths"], "figs": ["fig-03-fig2.jpg"], "summary": "Show by taking moments about A that the tension in the steel wire supporting the shelf and vase is about 50 N."},
    {"qnum": "03.3", "page": 7, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the tensile strain of the steel wire (area 7.8 x 10^-7 m^2, Young modulus 180 GPa)."},
    {"qnum": "04.1", "page": 8, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the air resistance acting on an 11 000 kg car with 230 kN thrust and 2.9 m s^-2 acceleration."},
    {"qnum": "04.2", "page": 8, "marks": 2, "topic": "3.4", "skills": [], "figs": [], "summary": "Explain why the acceleration of the car decreases and eventually reaches zero at constant thrust."},
    {"qnum": "04.3", "page": 8, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the time taken for a detached part P (1.5 m high, initial upward velocity 2.5 m s^-1) to reach the ground."},
    {"qnum": "04.4", "page": 9, "marks": 2, "topic": "3.4", "skills": ["graph"], "figs": [], "summary": "Draw on Figure 3 the path that P would follow when horizontal air resistance is not negligible."},
    {"qnum": "04.5", "page": 9, "marks": 2, "topic": "3.4", "skills": [], "figs": [], "summary": "Explain the modified trajectory in 4.4 and why air resistance is negligible in the vertical direction."},
    {"qnum": "05.1", "page": 10, "marks": 6, "topic": "3.2", "skills": [], "figs": [], "summary": "Explain how line spectra are produced via charged-particle collisions and discrete atomic energy levels."},
    {"qnum": "06.1", "page": 12, "marks": 2, "topic": "3.5", "skills": ["graph"], "figs": ["fig-06-fig5.jpg"], "summary": "Draw on Figure 5 the I-V characteristic of the car headlight lamp with supply connections reversed."},
    {"qnum": "06.2", "page": 12, "marks": 2, "topic": "3.5", "skills": ["graph", "maths"], "figs": ["fig-06-fig5.jpg"], "summary": "Deduce the working voltage and power marking on the car headlight lamp from Figure 5."},
    {"qnum": "06.3", "page": 13, "marks": 1, "topic": "3.5", "skills": ["graph", "maths"], "figs": ["fig-06-fig5.jpg"], "summary": "Determine the resistance of the lamp when the pd across it is half the working voltage."},
    {"qnum": "06.4", "page": 13, "marks": 3, "topic": "3.5", "skills": [], "figs": ["fig-06-fig5.jpg"], "summary": "Explain how the resistance of the lamp varies as the voltage increases from zero to its working voltage."},
    {"qnum": "06.5", "page": 14, "marks": 2, "topic": "3.5", "skills": ["practical", "maths"], "figs": [], "summary": "Discuss the limitations of the circuit in Figure 6 for collecting the lamp I-V characteristic data."},
    {"qnum": "07.1", "page": 15, "marks": 1, "topic": "3.3", "skills": [], "figs": ["fig-07-fig7.jpg"], "summary": "State the phase relationship between points A and B on the vibrating guitar string."},
    {"qnum": "07.2", "page": 15, "marks": 2, "topic": "3.3", "skills": ["maths"], "figs": ["fig-07-fig7.jpg"], "summary": "Calculate the speed of the 330 Hz wave along the 0.66 m guitar string."},
    {"qnum": "07.3", "page": 16, "marks": 3, "topic": "3.3", "skills": ["maths"], "figs": ["fig-07-fig7.jpg"], "summary": "Show that the tension in the guitar string (3.1 g, 0.91 m) sounding the harmonic in Figure 7 is about 70 N."},
    {"qnum": "07.4", "page": 16, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Estimate the elastic energy stored in the string and discuss whether there is a significant risk if it breaks."},
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

    qnums = [q["qnum"] for q in QUESTIONS]
    ms_written = crop_official_markschemes(MS_PDF, qnums, IMG_DIR / "ms")
    print(f"Cropped {len(ms_written)} / {len(qnums)} mark schemes for {PAPER_ID}")

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
