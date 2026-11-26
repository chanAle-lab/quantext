#!/usr/bin/env python3
"""Ingest AQA AS Physics Paper 1 (7407/1) Specimen 2014 into questions.json + img/2014-specimen-7407-1/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2014-specimen-7407-1"
QP_PDF = ROOT / "raw_pdfs" / "media_1795693504245_00ec2a6b.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795693504260_523e1010.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2014,
    "series": "Specimen",
    "date": "2014-10-08",
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
    {"filename": "fig-03-fig1-2.jpg", "page": 8, "x0": 115, "y0": 75, "x1": 555, "y1": 420},
    {"filename": "fig-04-fig3.jpg", "page": 10, "x0": 115, "y0": 75, "x1": 555, "y1": 435},
    {"filename": "fig-05-fig4-5.jpg", "page": 12, "x0": 115, "y0": 65, "x1": 555, "y1": 555},
    {"filename": "fig-06-data.jpg", "page": 15, "x0": 115, "y0": 65, "x1": 540, "y1": 270},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 5, "topic": "3.2", "skills": [], "figs": [], "summary": "Complete Table 1 comparing relative charge, baryon number, and quark composition of pi+ and proton."},
    {"qnum": "01.2", "page": 2, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "Circle the type of interaction shown in pi+ + p -> K+ + X."},
    {"qnum": "01.3", "page": 2, "marks": 3, "topic": "3.2", "skills": [], "figs": [], "summary": "Deduce the relative charge, baryon number, and strangeness of particle X."},
    {"qnum": "01.4", "page": 3, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "Circle the type of interaction shown in X -> n + pi+."},
    {"qnum": "01.5", "page": 3, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "Explain why the decay X -> n + pi+ is a weak interaction."},
    {"qnum": "01.6", "page": 3, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "Write down the equation for the beta-minus decay of the neutron."},
    {"qnum": "01.7", "page": 3, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "Explain why no further decays occur after the neutron and pion decay."},
    {"qnum": "02.1", "page": 4, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "Explain why no charge is lost when ultraviolet light is shone on a positively charged metal plate."},
    {"qnum": "02.2", "page": 4, "marks": 6, "topic": "3.2", "skills": [], "figs": [], "summary": "Discuss combinations of metal and UV light source from Tables 2 and 3 to demonstrate threshold frequency and work function."},
    {"qnum": "02.3", "page": 6, "marks": 3, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "Calculate the maximum kinetic energy, in J, of electrons emitted from zinc (work function 4.3 eV) by 1.2 x 10^15 Hz UV light."},
    {"qnum": "02.4", "page": 6, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "Explain why the calculated kinetic energy of emitted photoelectrons is a maximum."},
    {"qnum": "03.1", "page": 8, "marks": 4, "topic": "3.3", "skills": [], "figs": ["fig-03-fig1-2.jpg"], "summary": "Explain the variation in loudness at Y in Quincke's tube as the movable tube is slowly pulled out."},
    {"qnum": "03.2", "page": 9, "marks": 3, "topic": "3.3", "skills": ["maths"], "figs": ["fig-03-fig1-2.jpg"], "summary": "Calculate the minimum distance moved by the movable tube for the sound at Y to be at its quietest (800 Hz, 340 m s^-1)."},
    {"qnum": "03.3", "page": 9, "marks": 4, "topic": "3.3", "skills": ["practical"], "figs": [], "summary": "State and explain measurements to obtain a reliable value for the speed of sound using Quincke's tube."},
    {"qnum": "04.1", "page": 10, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": ["fig-04-fig3.jpg"], "summary": "Calculate the density of the 16 g, 16 mm diameter steel ball."},
    {"qnum": "04.2", "page": 10, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": ["fig-04-fig3.jpg"], "summary": "Calculate the speed of the steel ball just before impact after falling 1.27 m."},
    {"qnum": "04.3", "page": 11, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the speed of the steel ball just after impact if it rebounds to 0.85 m."},
    {"qnum": "04.4", "page": 11, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the change in momentum of the steel ball due to the impact."},
    {"qnum": "04.5", "page": 11, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the average force of the ball on the lens during the 40 ms impact."},
    {"qnum": "04.6", "page": 11, "marks": 2, "topic": "3.4", "skills": [], "figs": [], "summary": "Explain, with reference to momentum, why the test should specify the material of the plinth."},
    {"qnum": "05.1", "page": 12, "marks": 1, "topic": "3.5", "skills": [], "figs": ["fig-05-fig4-5.jpg"], "summary": "Explain what is meant by a potential divider."},
    {"qnum": "05.2", "page": 13, "marks": 3, "topic": "3.5", "skills": [], "figs": ["fig-05-fig4-5.jpg"], "summary": "State and explain what happens to the voltmeter reading across thermistor T when R increases at constant temperature."},
    {"qnum": "05.3", "page": 13, "marks": 2, "topic": "3.5", "skills": [], "figs": ["fig-05-fig4-5.jpg"], "summary": "State and explain what happens to the ammeter reading when the temperature of the thermistor increases."},
    {"qnum": "05.4", "page": 13, "marks": 2, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "Calculate the resistance of R so that an alarm across T (2.5 kohm at 0 C) sounds when pd exceeds 3.0 V on a 12.0 V supply."},
    {"qnum": "05.5", "page": 14, "marks": 1, "topic": "3.5", "skills": [], "figs": [], "summary": "State one change to the circuit so the alarm sounds when temperature rises above a certain value instead."},
    {"qnum": "06.1", "page": 15, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the tensile force required to produce a pre-strain of 3.0 x 10^-4 in the steel rail."},
    {"qnum": "06.2", "page": 15, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the elastic strain energy stored in a 45 m rail pre-strained as in 6.1."},
    {"qnum": "06.3", "page": 16, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": ["fig-06-data.jpg"], "summary": "Calculate the temperature at which the pre-strained steel rail becomes unstressed."},
    {"qnum": "06.4", "page": 16, "marks": 2, "topic": "3.4", "skills": [], "figs": [], "summary": "Explain why the engineer does not use the highest observed temperature to determine the pre-strain."},
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
