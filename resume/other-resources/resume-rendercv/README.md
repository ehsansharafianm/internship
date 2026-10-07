# RenderCV resume workflow

This directory keeps one complete master resume and creates a self-contained
folder for every tailored job application.

## Directory structure

```text
resume-rendercv/
|-- master/
|   `-- Ehsan_Sharafian_Master.yaml
|-- applications/
|   `-- YYYY/
|       `-- YYYY-MM-DD-company-role/
|           |-- resume.yaml
|           |-- resume.pdf
|           |-- job.md
|           `-- rendercv_output/
|               |-- Ehsan_Sharafian_CV.typ
|               |-- Ehsan_Sharafian_CV.md
|               |-- Ehsan_Sharafian_CV.html
|               `-- Ehsan_Sharafian_CV_1.png
|-- New-Application.cmd
`-- New-Application.ps1
```

The master YAML is the complete source of truth. Update it whenever a new
publication, skill, position, or accomplishment should be available to future
applications. Do not tailor the master for a single job.

## Create an application

Open PowerShell in `resume-rendercv` and run:

```powershell
.\New-Application.cmd `
  -Company "Medtronic" `
  -Role "Biomechanics Engineer" `
  -JobUrl "https://example.com/job"
```

The command:

1. Creates a dated application folder under `applications/<year>/`.
2. Copies the master to `resume.yaml`.
3. Creates `job.md` for requirements, tailoring notes, and status.
4. Renders `resume.pdf` and the additional RenderCV formats.
5. Stops instead of overwriting a folder that already exists.

Choose a different built-in RenderCV theme with:

```powershell
.\New-Application.cmd `
  -Company "Example Company" `
  -Role "Robotics Engineer" `
  -Theme "engineeringresumes"
```

Create the folder without rendering when RenderCV is not installed yet:

```powershell
.\New-Application.cmd `
  -Company "Example Company" `
  -Role "Research Engineer" `
  -SkipRender
```

The `.cmd` launcher works even when Windows blocks direct execution of
PowerShell scripts. It applies the execution-policy exception only to this
single command and does not change the computer's system-wide policy.

## Tailor and re-render

Edit only the new application's `resume.yaml`. Typical tailoring includes:

- rewriting the professional summary;
- moving the most relevant skills and experience earlier;
- emphasizing matching accomplishments and measurable results;
- removing details that do not support the target role;
- using the job's terminology accurately.

Then open PowerShell in the application folder and run:

```powershell
python -m rendercv render .\resume.yaml
```

The application folder is a snapshot of what was submitted. After applying,
set the status and application date in `job.md`. If a materially different
resume is submitted later, create a new application folder instead of
overwriting the old submission.

## Install RenderCV

This repository's YAML schema targets RenderCV 2.8:

```powershell
python -m pip install "rendercv[full]==2.8"
```

Verify the installation:

```powershell
python -m rendercv --version
```

## Save a generated application to Git

From the repository root:

```powershell
git add resume-rendercv/applications
git commit -m "Add tailored resume for Company Role"
git push
```

This repository is public. Do not put private recruiter notes, interview
details, or other confidential information in `job.md`.
