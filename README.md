# Custom YAML resume system

This directory maintains four focused master resumes and turns the selected
YAML master into a professional, self-contained HTML file and a
submission-ready PDF.

## Organized structure

```text
resume/
|-- master/
|   |-- Ehsan_Sharafian_Wearable_Tech.yaml
|   |-- Ehsan_Sharafian_Robotics.yaml
|   |-- Ehsan_Sharafian_Design.yaml
|   `-- Ehsan_Sharafian_Machine_Learning.yaml
|-- applications/
|   `-- YYYY/
|       `-- YYYY-MM-DD-resume-type-company-role/
|           |-- resume.yaml          # tailored information and job metadata
|           |-- index.html           # self-contained HTML with embedded style
|           |-- resume.pdf           # submission version
|           `-- Render.cmd           # rebuild this application
|-- system/
|   |-- resume_tool.py               # renderer and application wizard
|   |-- resume.html.j2               # semantic document structure
|   |-- resume.css                   # professional screen and print design
|   |-- master-previews/             # rendered HTML for all four masters
|   `-- requirements.txt             # Python dependencies
|-- New-Application.cmd              # interactive application wizard (Windows)
|-- New-Application.command          # interactive application wizard (macOS/Linux)
|-- Render-Master.cmd                # rebuild the master outputs (Windows)
|-- Render-Master.command           # rebuild the master outputs (macOS/Linux)
|-- Ehsan-Sharafian-Resume-*.pdf     # rendered PDFs for all four masters
`-- Ehsan-Sharafian-Resume.pdf       # wearable-tech compatibility copy
```

The four master YAML files are independent. They currently contain identical
resume content, so each one can be tailored later without affecting the other
focus areas. Wearable Technology is the default master when no profile is
specified.

## Cross-platform launchers

Every launcher ships in two forms that do exactly the same thing:

- `*.cmd` — double-click on **Windows**.
- `*.command` — double-click in **Finder** on **macOS** (also runnable from a
  terminal on macOS or Linux).

Both call the same `system/resume_tool.py`. Each new application folder gets
both a `Render.cmd` and a `Render.command`.

Both launchers build the HTML and write the PDF automatically using Microsoft
Edge, Google Chrome, or Chromium in the background. The macOS `.command` files
are direct equivalents of their Windows `.cmd` counterparts. If a browser
blocks background PDF printing on macOS, the launcher opens the generated HTML
as a fallback; use **Print (Cmd+P) > Save as PDF**.

On macOS the first time you double-click a `.command` file, Gatekeeper may ask
for confirmation; choose **Open**. The repository stores these launchers with
their executable flag. If a launcher loses that flag after being copied outside
Git, restore it with `chmod +x <file>.command` from a terminal.

The editable content, HTML structure, and CSS design remain separate at the
source level. During rendering, CSS is embedded into `index.html`, so generated
application folders do not need a separate stylesheet. Company, role, URL,
date, and status are stored in the `application` section of `resume.yaml`, so a
separate notes file is not required.

## One-time setup

On **Windows**, open Command Prompt in the `resume` directory:

```cmd
python -m pip install -r system\requirements.txt
```

On **macOS/Linux**, open a terminal in the `resume` directory:

```bash
python3 -m pip install -r system/requirements.txt
```

Microsoft Edge, Google Chrome, or Chromium is required for PDF generation. The
renderer automatically checks standard Windows and macOS installation
locations.

## Create a job-specific resume interactively

Double-click the launcher for your system:

```text
New-Application.cmd        (Windows)
New-Application.command    (macOS)
```

The wizard asks for:

1. master resume focus;
2. company name;
3. role or position title;
4. job URL;
5. application date.

The application and its PDF are then generated automatically. The generated
folder name includes the selected resume type, for example:

```text
2026-09-05-robotics-company-name-robotics-engineer
```

The window remains open after completion so messages and errors can be read.

Command-line mode is also supported:

```cmd
New-Application.cmd -MasterProfile wearable-tech -Company "Medtronic" -Role "Biomechanics Engineer" -JobUrl "https://example.com/job/12345"
```

```bash
./New-Application.command -MasterProfile wearable-tech -Company "Medtronic" -Role "Biomechanics Engineer" -JobUrl "https://example.com/job/12345"
```

Valid profile names are `wearable-tech`, `robotics`, `design`, and
`machine-learning`. Advanced command-line use can still supply a custom YAML
file with `-Master`; it overrides `-MasterProfile`.

## Tailor and re-render an application

Open the generated application's `resume.yaml`. Change only the content needed
for that job:

- rewrite `resume.summary`;
- reorder or rewrite `resume.skills`;
- prioritize relevant experience and highlights;
- remove content that does not support the role;
- keep all claims and metrics accurate.

The application metadata is at the top:

```yaml
application:
  master_profile: wearable-tech
  company: Medtronic
  role: Biomechanics Engineer
  job_url: https://example.com/job/12345
  created: 2026-07-29
  status: Preparing
```

`master_profile` records which focused master was used to start the
application. It does not change how the resume is displayed.

After editing, double-click the application's `Render.cmd` (Windows) or
`Render.command` (macOS). It regenerates its HTML and PDF without changing the
master or another application.

## Update the masters

Edit the relevant focus file in `master/`:

```text
Ehsan_Sharafian_Wearable_Tech.yaml
Ehsan_Sharafian_Robotics.yaml
Ehsan_Sharafian_Design.yaml
Ehsan_Sharafian_Machine_Learning.yaml
```

Then double-click the launcher for your system:

```text
Render-Master.cmd        (Windows)
Render-Master.command    (macOS)
```

This regenerates four HTML previews under `system/master-previews/` and four
focus-specific PDFs at the repository root. For compatibility, the wearable
technology output is also copied to `system/index.html` and
`Ehsan-Sharafian-Resume.pdf`.

## Change the shared design

Edit:

```text
system\resume.css
```

Edit `system\resume.html.j2` only when changing the HTML document structure.
Existing application PDFs remain unchanged until their `Render.cmd` (Windows) or
`Render.command` (macOS) is run.

## Save applications to Git

From the repository root:

```cmd
git add .
git commit -m "Add tailored manual resume"
git push
```

This repository is public. Do not store confidential information in
`resume.yaml`.
