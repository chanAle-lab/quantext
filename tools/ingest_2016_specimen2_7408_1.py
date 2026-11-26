#!/usr/bin/env python3
"""Ingest AQA A-level Physics Paper 1 (7408/1) Specimen Set 2 into questions.json + img/2016-specimen2-7408-1/."""

from __future__ import annotations

import json
from pathlib import Path
import pymupdf as fitz

from crop_official_markscheme import crop_official_markschemes

ROOT = Path(__file__).resolve().parent.parent
PAPER_ID = "2016-specimen2-7408-1"
QP_PDF = ROOT / "raw_pdfs" / "media_1795693078614_5ec19d19.pdf"
MS_PDF = ROOT / "raw_pdfs" / "media_1795693078603_981fd7b7.pdf"
IMG_DIR = ROOT / "img" / PAPER_ID

PAPER_META = {
    "id": PAPER_ID,
    "year": 2016,
    "series": "Specimen Set 2",
    "date": "2016-06-01",
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
    {"filename": "fig-01-fig1.jpg", "page": 2, "x0": 115, "y0": 115, "x1": 530, "y1": 455},
    {"filename": "fig-04-fig4-5.jpg", "page": 11, "x0": 85, "y0": 100, "x1": 525, "y1": 665},
    {"filename": "fig-05-fig7.jpg", "page": 14, "x0": 115, "y0": 72, "x1": 535, "y1": 218},
    {"filename": "fig-06-fig9.jpg", "page": 18, "x0": 115, "y0": 75, "x1": 535, "y1": 375},
]

QUESTIONS = [
    {"qnum": "01.1", "page": 2, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": ["fig-01-fig1.jpg"], "summary": "Calculate the initial vertical component of velocity of the golf ball."},
    {"qnum": "01.2", "page": 2, "marks": 1, "topic": "3.4", "skills": [], "figs": ["fig-01-fig1.jpg"], "summary": "Draw an arrow on Figure 1 to show the direction of the force acting on the ball at point X."},
    {"qnum": "01.3", "page": 3, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Show that the time taken for the ball to reach point Y is about 4 s."},
    {"qnum": "01.4", "page": 3, "marks": 3, "topic": "3.4", "skills": ["graph"], "figs": [], "summary": "Sketch on Figure 2 how the vertical velocity component v changes throughout the 6.0 s flight."},
    {"qnum": "01.5", "page": 4, "marks": 3, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "Calculate the height h of the cliff."},
    {"qnum": "01.6", "page": 4, "marks": 2, "topic": "3.4", "skills": [], "figs": ["fig-01-fig1.jpg"], "summary": "Draw on Figure 1 the path the ball takes when air resistance is taken into account."},
    {"qnum": "02.1", "page": 6, "marks": 2, "topic": "3.3", "skills": [], "figs": [], "summary": "Distinguish between longitudinal and transverse waves."},
    {"qnum": "02.2", "page": 6, "marks": 2, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "Calculate the tension required for a 0.050 m piano wire to vibrate at 4.1 kHz."},
    {"qnum": "02.3", "page": 7, "marks": 2, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "Evaluate whether it is safe to use the piano wire given its breaking stress."},
    {"qnum": "02.4", "page": 7, "marks": 4, "topic": "3.3", "skills": [], "figs": [], "summary": "Explain which end of the tapered wire has greater diameter and why the second harmonic has the shape in Figure 3."},
    {"qnum": "03.1", "page": 8, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "Name one process in which a proton changes into a neutron."},
    {"qnum": "03.2", "page": 8, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "Name the particle interaction involved when a proton changes into a neutron."},
    {"qnum": "03.3", "page": 8, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "Write an equation for the process and show that baryon number and lepton number are conserved."},
    {"qnum": "03.4", "page": 9, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "State the quark composition of a K+ kaon."},
    {"qnum": "03.5", "page": 9, "marks": 2, "topic": "3.2", "skills": [], "figs": [], "summary": "Explain one conserved property and one non-conserved property in K+ -> pi+ + pi0."},
    {"qnum": "04.1", "page": 10, "marks": 2, "topic": "3.6", "skills": [], "figs": [], "summary": "State the conditions for simple harmonic motion."},
    {"qnum": "04.2", "page": 11, "marks": 2, "topic": "3.6", "skills": ["graph", "maths"], "figs": ["fig-04-fig4-5.jpg"], "summary": "Show from the v-t graph in Figure 5 that the maximum displacement of the vibrating plate is 3.5 x 10^-4 m."},
    {"qnum": "04.3", "page": 12, "marks": 1, "topic": "3.6", "skills": ["graph"], "figs": ["fig-04-fig4-5.jpg"], "summary": "Draw on Figure 6 the displacement-time (s-t) graph between 0 and 75 ms."},
    {"qnum": "04.4", "page": 12, "marks": 1, "topic": "3.6", "skills": ["graph"], "figs": ["fig-04-fig4-5.jpg"], "summary": "State one time at which the vibrating plate has maximum potential energy."},
    {"qnum": "04.5", "page": 13, "marks": 3, "topic": "3.6", "skills": [], "figs": [], "summary": "Explain how and why sand grains lose contact with the vibrating plate above a particular frequency."},
    {"qnum": "04.6", "page": 13, "marks": 2, "topic": "3.6", "skills": ["maths"], "figs": [], "summary": "Calculate the lowest frequency at which the sand grains lose contact with the plate."},
    {"qnum": "05.1", "page": 14, "marks": 1, "topic": "3.5", "skills": [], "figs": ["fig-05-fig7.jpg"], "summary": "State Ohm's law."},
    {"qnum": "05.2", "page": 14, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": ["fig-05-fig7.jpg"], "summary": "Calculate, in mA, the current in the 20.0 ohm cylinder of conducting putty."},
    {"qnum": "05.3", "page": 15, "marks": 4, "topic": "3.5", "skills": ["practical"], "figs": [], "summary": "Discuss problems that make the circuit in Figure 8 unsuitable for demonstrating Ohm's law for the putty."},
    {"qnum": "05.4", "page": 16, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": ["fig-05-fig7.jpg"], "summary": "Show that resistivity rho = (R / l^2) x volume of the cylinder."},
    {"qnum": "05.5", "page": 16, "marks": 3, "topic": "3.5", "skills": ["maths"], "figs": ["fig-05-fig7.jpg"], "summary": "Calculate the resistivity of the conducting putty with an appropriate unit."},
    {"qnum": "06.1", "page": 18, "marks": 2, "topic": "3.4", "skills": ["maths"], "figs": ["fig-06-fig9.jpg"], "summary": "Calculate the moment of the 50 N counterweight about the pivot when the shaduf beam is horizontal."},
    {"qnum": "06.2", "page": 19, "marks": 5, "topic": "3.4", "skills": ["maths"], "figs": ["fig-06-fig9.jpg"], "summary": "Calculate the additional force required at the end of the horizontal beam to lift the half-full bucket of water."},
    {"qnum": "06.3", "page": 19, "marks": 3, "topic": "3.4", "skills": [], "figs": [], "summary": "Explain how the force in Question 6.2 would differ if the weight of the beam is not negligible."},
    # Section B MCQs (07 - 31)
    {"qnum": "07", "page": 20, "marks": 1, "topic": "3.2", "skills": ["maths"], "figs": [], "summary": "MCQ: Identify the nucleus with a smaller specific charge than O-18."},
    {"qnum": "08", "page": 20, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Find nucleon and proton numbers after Mg-25 is bombarded with an alpha particle and emits a neutron."},
    {"qnum": "09", "page": 21, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the radioactive emission sequence that forms an isotope of the original element."},
    {"qnum": "10", "page": 21, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the incorrect statement concerning forces between leptons and hadrons."},
    {"qnum": "11", "page": 21, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify a hadron of zero charge."},
    {"qnum": "12", "page": 22, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Order radio waves, gamma rays, visible light, and infrared by increasing photon energy."},
    {"qnum": "13", "page": 22, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify the correct statement about photoelectric emission from a metal surface."},
    {"qnum": "14", "page": 23, "marks": 1, "topic": "3.2", "skills": [], "figs": [], "summary": "MCQ: Identify which electron transition emits an infrared photon given R -> Q emits visible light."},
    {"qnum": "15", "page": 23, "marks": 1, "topic": "3.2", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the graph of photon momentum p against wavelength lambda."},
    {"qnum": "16", "page": 24, "marks": 1, "topic": "3.3", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify quantities z and s on a displacement-time wave graph."},
    {"qnum": "17", "page": 24, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the phase difference between two coherent sound waves with path difference 0.90 m and wavelength 0.40 m."},
    {"qnum": "18", "page": 25, "marks": 1, "topic": "3.3", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the double-slit fringe separation for 600 nm light, 0.50 mm slit separation, and 1.50 m screen distance."},
    {"qnum": "19", "page": 25, "marks": 1, "topic": "3.3", "skills": [], "figs": [], "summary": "MCQ: Identify the change that causes the received microwave signal behind a gap to decrease and then increase."},
    {"qnum": "20", "page": 25, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Identify whether impulse and force are scalars or vectors."},
    {"qnum": "21", "page": 26, "marks": 1, "topic": "3.4", "skills": [], "figs": [], "summary": "MCQ: Identify which quantity of a vertically fired firework is never zero before hitting the ground."},
    {"qnum": "22", "page": 26, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the momentum of a 0.20 kg ball at the highest point Q of its projectile trajectory."},
    {"qnum": "23", "page": 27, "marks": 1, "topic": "3.4", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate the load needed for 0.1% strain in a steel wire of area 0.5 mm^2."},
    {"qnum": "24", "page": 27, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the new current when a wire is replaced with one of double length and double diameter at constant pd."},
    {"qnum": "25", "page": 27, "marks": 1, "topic": "3.5", "skills": [], "figs": [], "summary": "MCQ: Identify the incorrect statement when a second identical resistor is connected in series across pd V."},
    {"qnum": "26", "page": 28, "marks": 1, "topic": "3.5", "skills": [], "figs": [], "summary": "MCQ: Identify which resistor arrangement has the greatest total resistance."},
    {"qnum": "27", "page": 28, "marks": 1, "topic": "3.5", "skills": ["maths"], "figs": [], "summary": "MCQ: Find external resistance R for a 2.0 V cell with 1.0 ohm internal resistance and 1.6 V terminal pd."},
    {"qnum": "28", "page": 29, "marks": 1, "topic": "3.6", "skills": ["maths"], "figs": [], "summary": "MCQ: Calculate speed v and centripetal acceleration a of a helicopter on an 800 m diameter circle with 5.0 min period."},
    {"qnum": "29", "page": 29, "marks": 1, "topic": "3.6", "skills": ["graph"], "figs": [], "summary": "MCQ: Identify the velocity-displacement graph for a body in simple harmonic motion."},
    {"qnum": "30", "page": 30, "marks": 1, "topic": "3.6", "skills": ["maths"], "figs": [], "summary": "MCQ: Find the new periods of a simple pendulum and mass-spring system when g increases fourfold."},
    {"qnum": "31", "page": 30, "marks": 1, "topic": "3.6", "skills": [], "figs": [], "summary": "MCQ: Identify the correct statement for a driven mechanical oscillator."},
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
    p12 = ms_doc[11]
    mcq_clip = fitz.Rect(42, 120, 490, 305)
    mcq_pix = p12.get_pixmap(clip=mcq_clip, matrix=fitz.Matrix(2.5, 2.5), alpha=False)
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
