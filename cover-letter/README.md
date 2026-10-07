# Cover-letter system

This folder turns a single master cover-letter YAML into a professional,
self-contained HTML file and a submission-ready PDF, styled to match the
`resume/` system. It mirrors that system's structure and launchers.

## Structure

```text
cover-letter/
|-- master/
|   `-- Ehsan_Sharafian_Cover_Letter.yaml   # editable content + placeholders
|-- applications/
|   `-- YYYY/
|       `-- YYYY-MM-DD-company-role/
|           |-- coverletter.yaml            # tailored copy + job metadata
|           |-- index.html                  # self-contained preview
|           |-- cover-letter.pdf            # submission version
|           |-- Render.cmd                  # rebuild (Windows)
|           `-- Render.command             # rebuild (macOS/Linux)
|-- system/
|   |-- coverletter_tool.py                 # renderer + wizard
|   |-- coverletter.html.j2                 # document structure
|   |-- coverletter.css                     # screen + print design
|   `-- requirements.txt                    # Python dependencies
|-- New-Cover-Letter.cmd / .command         # interactive wizard
`-- Render-Master.cmd / .command            # rebuild the master preview + PDF
```

## One-time setup

```cmd
python -m pip install -r system\requirements.txt
```

(macOS/Linux: `python3 -m pip install -r system/requirements.txt`.) Microsoft
Edge, Google Chrome, or Chromium is required for automatic PDF generation.

## Create a cover letter for a job

Double-click `New-Cover-Letter.cmd` (Windows) or `New-Cover-Letter.command`
(macOS). The wizard asks for company, role, job URL, and date, then creates a
folder like `applications/2026/2026-09-05-medtronic-biomechanics-intern/` and
renders the HTML and PDF.

Command-line mode:

```cmd
New-Cover-Letter.cmd -Company "Medtronic" -Role "Biomechanics Intern" -JobUrl "https://example.com/job/123"
```

## Tailor and re-render

Open the new folder's `coverletter.yaml` and **replace every `[placeholder]`**
(for example `[Company name]`, `[specific technology/product/research area]`).
Unfilled placeholders are highlighted in the rendered draft so you never submit
one by accident. Then double-click `Render.cmd` (Windows) or `Render.command`
(macOS) to rebuild that letter's HTML and PDF.

Markdown-style `**bold**` is supported in paragraph text if you want emphasis.

## Update the master

Edit `master/Ehsan_Sharafian_Cover_Letter.yaml`, then run `Render-Master.cmd`
(Windows) or `Render-Master.command` (macOS). This regenerates
`system/master-preview.html`, `system/index.html`, and
`Ehsan-Sharafian-Cover-Letter.pdf` at this folder's root.

## Change the design

Edit `system/coverletter.css` (and `system/coverletter.html.j2` only for
structural changes). Existing application PDFs stay unchanged until you re-run
their `Render.cmd` / `Render.command`.
