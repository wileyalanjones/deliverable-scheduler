# Unsupported Format Example

This file is intentionally a Markdown (`.md`) file. It exists to demonstrate what
happens when a user uploads a file type the app doesn't support.

Uploading this file should show an error rather than crash:

> Unsupported file type: "md". Please upload a PDF, DOCX, or EML.

Even though this file contains text — including something that looks like a
deliverable date (e.g. "the report is due 2026-11-15") — `.md` is not one of the
supported formats, so the app rejects it gracefully.