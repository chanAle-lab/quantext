# quantext

Access and practice with the complete collection of **AQA AS & A-Level Physics (7407 / 7408)** past papers, official mark schemes, specification cheatsheets, active-recall flashcards, diagnostic quizzes, and teacher tools—all in one zero-build static web app.

## Architecture

- `index.html` — Single-file HTML/CSS/vanilla JS application with Light & Dark themes, URL-hash routing (`#view=...&topic=...`), `localStorage` persistence, side-by-side modal, and `@media print` PDF export.
- `questions.json` — Master database of AQA Physics topics (`3.1`–`3.13`), skills (`maths`, `practical`, `graph`), levels (`AS`, `A`), papers, and questions.
- `cheatsheets.json` — Topic-by-topic specification revision notes.
- `flashcards.json` — Active-recall flashcards across all 13 topics (with runtime fallback builder from `cheatsheets.json`).
- `quiz_questions.json` — Curated MCQs used for both the Practice diagnostic quiz and Teacher's Hub Quiz Show.
- `tools/` — Python (`pymupdf` + `Pillow`) PDF extraction, cropping, and database validation scripts.
- `img/<paper-id>/` — Cropped question (`q*.jpg`), figure/diagram (`fig-*.jpg`), and mark scheme (`ms-q*.jpg`) images.

## Local Development

Serve the directory with any static HTTP server:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Validating the Database

```bash
python tools/verify_db.py
```
