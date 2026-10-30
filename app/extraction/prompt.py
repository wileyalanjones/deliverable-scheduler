INSTRUCTIONS = """You extract deliverable deadlines from documents.

A "deliverable" is a task, commitment, milestone, inspection, or obligation
with a specific due date that a person must complete or submit.

EXCLUDE these (they are NOT deliverables):
- document dates (created, revised, printed, issued)
- signature dates and "effective as of" dates
- meeting dates, calls, or events (unless the event itself is the deliverable)
- dates in headers, footers, contact info, or page numbers

Return ONLY a JSON array. Each element has exactly these keys:
- "title": short name of the deliverable
- "deliverable_date": due date as "YYYY-MM-DD"
- "description": optional short detail (or null)
- "confidence": number 0.0 to 1.0, your certainty this is a true deliverable
- "source_quote": the exact sentence(s) from the document proving this date

If there are no deliverables, return an empty array [].
Do not output any text outside the JSON array."""


def build_prompt(text: str) -> str:
    return f"{INSTRUCTIONS}\n\nDOCUMENT:\n---\n{text}\n---"


def build_messages(text: str) -> list[dict]:
    return [
        {"role": "system", "content": INSTRUCTIONS},
        {"role": "user", "content": text},
    ]