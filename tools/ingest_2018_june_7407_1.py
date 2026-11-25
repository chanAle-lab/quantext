#!/usr/bin/env python3
"""Ingest AQA AS Physics Paper 1 (7407/1) June 2018 into questions.json + img/2018-june-7407-1/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2018-june-7407-1"
QP_PDF = ROOT / "raw_pdfs" / "media_1795609950295_a9b24638.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795609950992_d0709874.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2018,
    "series": "June",
    "date": "2018-05-15",
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
    {"filename": "fig-02-fig1.jpg", "page": 4, "x0": 180, "y0": 105, "x1": 400, "y1": 240},
    {"filename": "fig-02-fig2.jpg", "page": 5, "x0": 110, "y0": 90, "x1": 470, "y1": 225},
    {"filename": "fig-03-fig3.jpg", "page": 8, "x0": 48, "y0": 62, "x1": 540, "y1": 360},
    {"filename": "fig-04-fig4.jpg", "page": 12, "x0": 48, "y0": 62, "x1": 540, "y1": 332},
    {"filename": "fig-05-fig5.jpg", "page": 15, "x0": 190, "y0": 300, "x1": 400, "y1": 465},
    {"filename": "fig-06-fig6.jpg", "page": 18, "x0": 48, "y0": 62, "x1": 540, "y1": 325},
    {"filename": "fig-06-table1.jpg", "page": 19, "x0": 140, "y0": 102, "x1": 445, "y1": 220},
    {"filename": "fig-06-fig7.jpg", "page": 20, "x0": 140, "y0": 102, "x1": 445, "y1": 310},
    {"filename": "fig-07-fig8.jpg", "page": 22, "x0": 48, "y0": 62, "x1": 540, "y1": 315},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 3, "topic": "3.2", "skills": [], "figs": [], "summary": "Describe the strong nuclear interaction responsible for keeping protons and neutrons together in a stable nucleus."},
    {"qnum": "01.2", "page": 2, "marks": 3, "topic": "3.2", "skills": [], "figs": [], "summary": "Explain how baryon number is conserved in alpha decay and beta decay."},
    {"qnum": "01.3", "page": 3, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "Deduce the quark structure of the Lambda-0 baryon from pi- + p -> K0 + Lambda0."},
    {"qnum": "01.4", "page": 3, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "State one feature of K0 -> pi+ + pi- that shows it is an example of the weak interaction."},
    {"qnum": "01.5", "page": 3, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "Explain why many teams of scientists and engineers must collaborate for advances in particle physics."},
    {"qnum": "02.1", "page": 4, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the speed of a truck at point A after descending a vertical displacement of 8.0 m."},
    {"qnum": "02.2", "page": 5, "marks": 3, "topic": "3.4", "skills": [], "figs": ["fig-02-fig1.jpg"], "summary": "Discuss how the acceleration of the truck on a curved ramp (Figure 2) differs from a straight ramp (Figure 1)."},
    {"qnum": "02.3", "page": 6, "marks": 1, "topic": "3.4", "skills": [], "figs": ["fig-02-fig1.jpg", "fig-02-fig2.jpg"], "summary": "Explain why the final speed on the horizontal runway equals the speed at A in Figure 1."},
    {"qnum": "02.4", "page": 6, "marks": 3, "topic": "3.4", "skills": [], "figs": ["fig-02-fig2.jpg"], "summary": "Discuss any changes in the momentum of the truck and collected rainwater as rain falls vertically into it."},
    {"qnum": "03.1", "page": 8, "marks": 1, "topic": "3.2", "skills": [], "figs": ["fig-03-fig3.jpg"], "summary": "Identify the regions of the electromagnetic spectrum for transitions A, B, and C in Figure 3."},
    {"qnum": "03.2", "page": 9, "marks": 3, "topic": "3.2", "skills": [], "figs": ["fig-03-fig3.jpg"], "summary": "Explain why excitation by a photon requires an exact energy whereas an electron needs only a minimum kinetic energy."},
    {"qnum": "03.3", "page": 9, "marks": 3, "topic": "3.2", "skills": ["maths"], "figs": ["fig-03-fig3.jpg"], "summary": "Determine whether any transition in Figure 3 causes photoelectron emission from caesium (threshold 5.1e14 Hz)."},
    {"qnum": "03.4", "page": 10, "marks": 3, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "Calculate the maximum speed of electrons emitted from caesium by 12.1 eV photons."},
    {"qnum": "04.1", "page": 12, "marks": 2, "topic": "3.4", "skills": [], "figs": ["fig-04-fig4.jpg"], "summary": "State two necessary conditions for the suspended beam in Figure 4 to be in equilibrium."},
    {"qnum": "04.2", "page": 12, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "State what is meant by the centre of mass."},
    {"qnum": "04.3", "page": 13, "marks": 2, "topic": "3.4", "skills": [], "figs": ["fig-04-fig4.jpg"], "summary": "Explain why the centre of mass of the beam in Figure 4 must be vertically below A."},
    {"qnum": "04.4", "page": 13, "marks": 4, "topic": "3.4", "skills": ["maths"], "figs": ["fig-04-fig4.jpg"], "summary": "Calculate the tensions T1 in cable AB and T2 in cable AC for a 12 000 N beam."},
    {"qnum": "04.5", "page": 14, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the extension of the 12 m steel crane cable caused by the 12 000 N beam."},
    {"qnum": "05.1", "page": 15, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the weight of an ice cube of volume 4.0e-6 m^3 and density 920 kg m^-3."},
    {"qnum": "05.2", "page": 15, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the volume of water displaced by the floating ice cube in Figure 5."},
    {"qnum": "05.3", "page": 16, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": ["fig-05-fig5.jpg"], "summary": "Calculate the volume of the small piece of iron embedded in an ice cube displacing 3.9e-3 kg of water."},
    {"qnum": "06.1", "page": 19, "marks": 4, "topic": "3.5", "skills": ["maths"], "figs": ["fig-06-fig6.jpg"], "summary": "Determine with calculations which two lamps in Figure 6 are at their normal brightness."},
    {"qnum": "06.2", "page": 20, "marks": 3, "topic": "3.5", "skills": [], "figs": ["fig-06-table1.jpg"], "summary": "Explain what is observed regarding lamp brightness when lamp E is connected across Figure 7."},
    {"qnum": "06.3", "page": 21, "marks": 3, "topic": "3.5", "skills": ["maths"], "figs": ["fig-06-table1.jpg", "fig-06-fig7.jpg"], "summary": "Deduce with calculations the effect on the battery current when lamp B fails."},
    {"qnum": "07.1", "page": 22, "marks": 2, "topic": "3.3", "skills": [], "figs": ["fig-07-fig8.jpg"], "summary": "Describe the white-light interference pattern seen on the screen in Figure 8."},
    {"qnum": "07.2", "page": 23, "marks": 4, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "Describe with a calculation the interference pattern when only green (lambda) and red (1.2 lambda) light pass through."},
    {"qnum": "07.3", "page": 24, "marks": 6, "topic": "3.3", "skills": ["practical"], "figs": ["fig-07-fig8.jpg"], "summary": "Discuss how decreasing slit separation s or screen distance D affects the interference pattern and wavelength uncertainty."},
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
