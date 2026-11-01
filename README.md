# Deliverable Scheduler

Extract deliverable deadlines from documents and add them to a calendar — automatically.

Upload a contract, email, or report (PDF, DOCX, or EML). A model finds every deliverable
date in it, you review and approve the ones that matter, and the approved items land on a
calendar.

> **Live demo**: https://deliverable-scheduler.onrender.com/ — a hosted instance using the
> OpenRouter backend. Use it to try the app instantly with no local setup. (First load can
> take ~30–60s while the free tier wakes up.)

## How it works

1. **Upload** a document (PDF / DOCX / EML).
2. **Parse** — the text is extracted from the file.
3. **Extract** — an LLM returns a structured list of deliverable dates
   (`title`, `deliverable_date`, `confidence`, `source_quote`).
4. **Review** — each candidate is shown with its confidence and a quote of the sentence
   that justified it. Approve or reject.
5. **Calendar** — approved items are written to a calendar (a mock provider here; a real
   Google/Outlook provider plugs into the same interface). Individual events can be
   deleted, or the whole calendar cleared.

## Extraction backends

The extractor is pluggable. The app prefers a hosted model and falls back to a bundled
local one:

- **Hosted model (primary)** — set the `OPENROUTER_API_KEY` environment variable (and
  optionally `OPENROUTER_MODEL`, default `openai/gpt-4o-mini`) and the app calls OpenRouter.
  No model download, higher accuracy, at a small per-call cost. This is what the
  [live demo](https://deliverable-scheduler.onrender.com/) uses.
- **Local model (optional, limited)** — without a key, the app runs a bundled
  `Qwen/Qwen2.5-0.5B-Instruct` entirely on your machine (no API key or network cost). It's
  provided for running locally without any paid service, but it's less accurate and
  occasionally returns empty `source_quote`s. Needs the optional dependencies (`torch`,
  `transformers`); the ~1 GB model downloads on first use.

When `OPENROUTER_API_KEY` is set, the hosted model is used; otherwise the app falls back
to the local model.

## Quickstart

**Fastest**: open the [live demo](https://deliverable-scheduler.onrender.com/) — no setup.

To run locally:

```bash
# 1. create + activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. install dependencies
pip install -r requirements.txt

# 3. run
python run.py
```

Open http://localhost:8000 and upload a document.

Choose a backend:

- **Hosted (recommended)** — `export OPENROUTER_API_KEY=sk-or-...` before running. Best
  accuracy, no model download. Optionally set `OPENROUTER_MODEL` to override the default
  `openai/gpt-4o-mini`.
- **Local (optional, limited)** — instead `pip install torch transformers`. No key needed,
  but extraction is less accurate, and the ~1 GB model downloads on first use.

## Usage

> Pick the right URL: **https://deliverable-scheduler.onrender.com/** for the hosted demo,
> or **http://localhost:8000** when running locally (`python run.py`). The steps below are
> identical either way.

1. Open the app (https://deliverable-scheduler.onrender.com/, or http://localhost:8000 if
   running locally). You'll land on the **Upload** page.
2. Click **Choose a document** and select `sample-data/project-deliverables.eml` (or drag
   in any PDF, DOCX, or EML), then click **Extract deadlines**.
3. You'll be taken to the **Review** page, which lists each extracted deliverable with
   its due date, confidence, and the sentence that justified it.
4. For each item, click **Approve** to add it to the calendar, or **Reject** to discard
   it. Approved items drop off the review list.
5. Click **Calendar** in the top nav to see the approved events.
6. From the Calendar page you can:
   - **Delete** an individual event, or
   - **Clear all events** to start over.
7. Try the error handling:
   - Upload `sample-data/unsupported-format-example.md` → an "Unsupported file type"
     message is shown.
   - Click **Extract deadlines** with no file selected → a "Please choose a file"
     message is shown.

## Dependencies

- **Web**: FastAPI, Uvicorn, Jinja2
- **Data**: SQLAlchemy, SQLite (tables are created automatically on startup)
- **Parsing**: PyMuPDF (PDF), python-docx (DOCX), stdlib `email` (EML)
- **Extraction**: `requests` (hosted / OpenRouter), or — optionally — `transformers` +
  `torch` for the local `Qwen/Qwen2.5-0.5B-Instruct` model.

## Sample data

See `sample-data/` for synthetic documents (a `.eml`, `.docx`, and `.pdf` with the same
three deliverables). Upload any of them to try the flow.

Example input (body of `sample-data/project-deliverables.eml`):

```
1. The client onboarding report is due 2026-11-15.
2. Submit the security compliance form by 2026-11-30.
3. The final budget spreadsheet is required no later than 2026-12-05.
```

Expected output — three extracted items:

```
- Client Onboarding Report   2026-11-15   confidence 1.0
- Security Compliance Form   2026-11-30   confidence 1.0
- Final Budget Spreadsheet   2026-12-05   confidence 1.0
```

## Project structure

```
app/
  main.py            # routes (upload -> review -> approve/reject -> calendar)
  parsing/           # PDF / DOCX / EML text extraction
  extraction/        # prompt, JSON parsing, local + OpenRouter extractors, factory
  calendar/          # calendar provider abstraction + mock implementation
  models.py          # SQLAlchemy models
  templates/         # Jinja2 HTML pages
  static/            # stylesheet
run.py               # entry point
```

## What's implemented, mocked, and deferred

- **Implemented**: document parsing, LLM extraction (structured prompt + validation),
  the review workflow, per-event delete / clear-all on the calendar, and persistence in
  SQLite.
- **Mocked**: the calendar (`MockCalendarProvider` stores events in memory). Real
  Google/Microsoft Calendar plugins implement the same `CalendarProvider` interface but
  are out of scope here.
- **Deferred**: authentication, and a real calendar integration.


## Limitations & next steps

- The bundled 0.5B local model occasionally misses dates or returns empty
  `source_quote`s; a larger model — or the hosted (OpenRouter) backend behind the same
  interface — improves accuracy.
- The mock calendar is in-memory and resets on restart (approved items persist in the
  database).