# Deliverable Scheduler

Extract deliverable deadlines from documents and add them to a calendar — automatically.

Upload a contract, email, or report (PDF, DOCX, or EML). A model finds every deliverable
date in it, you review and approve the ones that matter, and the approved items land on a
calendar.

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

The extractor is pluggable; the app picks a backend based on configuration:

- **Local model (default)** — a bundled `Qwen/Qwen2.5-0.5B-Instruct` runs entirely on your
  machine, with no API key or network cost. This backend needs the optional dependencies
  (`torch`, `transformers`); the ~1 GB model downloads on first use.
- **Hosted model (optional)** — set the `OPENROUTER_API_KEY` environment variable (and
  optionally `OPENROUTER_MODEL`, default `openai/gpt-4o-mini`) and the app calls OpenRouter
  instead. No model download, better accuracy, at a small per-call cost.

When no key is configured, the app uses the local model.

## Quickstart

```bash
# 1. create + activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. install dependencies
pip install -r requirements.txt

# 3. (optional) install the local-model backend
pip install torch transformers

# 4. run
python run.py
```

Open http://localhost:8000 and upload a document.

> Note: with the local model, the first upload downloads the model (~1 GB) and runs on
> CPU, so the first extraction can take a minute or two. Set `OPENROUTER_API_KEY` to skip
> this and use the hosted model instead.

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

## How AI was used

[...]

## Limitations & next steps

- The bundled 0.5B local model occasionally misses dates or returns empty
  `source_quote`s; a larger model — or the hosted (OpenRouter) backend behind the same
  interface — improves accuracy.
- The mock calendar is in-memory and resets on restart (approved items persist in the
  database).

Time spent: [...]  Next I'd investigate: [...]