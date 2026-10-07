from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import webbrowser
from datetime import date
from pathlib import Path
from typing import Any

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
    from markupsafe import Markup
    from ruamel.yaml import YAML
except ImportError as exc:
    raise SystemExit(
        "Missing renderer dependencies. Run:\n"
        "  Windows:      python -m pip install -r system\\requirements.txt\n"
        "  macOS/Linux:  python3 -m pip install -r system/requirements.txt"
    ) from exc


SYSTEM_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = SYSTEM_ROOT.parent
DEFAULT_TEMPLATE = SYSTEM_ROOT / "resume.html.j2"
DEFAULT_STYLESHEET = SYSTEM_ROOT / "resume.css"
MASTER_PROFILES = {
    "wearable-tech": {
        "label": "Wearable Technology",
        "path": PROJECT_ROOT / "master" / "Ehsan_Sharafian_Wearable_Tech.yaml",
    },
    "robotics": {
        "label": "Robotics",
        "path": PROJECT_ROOT / "master" / "Ehsan_Sharafian_Robotics.yaml",
    },
    "design": {
        "label": "Design",
        "path": PROJECT_ROOT / "master" / "Ehsan_Sharafian_Design.yaml",
    },
    "machine-learning": {
        "label": "Machine Learning",
        "path": PROJECT_ROOT / "master" / "Ehsan_Sharafian_Machine_Learning.yaml",
    },
}
DEFAULT_MASTER_PROFILE = "wearable-tech"


class ResumeError(RuntimeError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ResumeError(f"YAML file not found: {path}")

    yaml = YAML(typ="safe")
    with path.open("r", encoding="utf-8") as stream:
        data = yaml.load(stream)

    if not isinstance(data, dict):
        raise ResumeError(f"Expected a YAML mapping in {path}")
    if not isinstance(data.get("resume"), dict):
        raise ResumeError(f"Missing required 'resume' mapping in {path}")

    required = ("name", "summary", "education", "skills", "experience")
    missing = [key for key in required if key not in data["resume"]]
    if missing:
        raise ResumeError(f"Missing required resume fields: {', '.join(missing)}")

    data.setdefault("application", {})
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.width = 110
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        yaml.dump(data, stream)


def write_text(path: Path, text: str, newline: str) -> None:
    """Write text with fixed line endings.

    Path.write_text only accepts a ``newline`` argument on Python 3.10+, so use
    ``Path.open`` (which has always supported it) to stay compatible with the
    Python 3.9 that ships with macOS.
    """
    with path.open("w", encoding="utf-8", newline=newline) as stream:
        stream.write(text)


def richtext(value: Any) -> Markup:
    escaped = html.escape(str(value), quote=False)
    formatted = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    return Markup(formatted)


def render_html(
    input_yaml: Path,
    output_html: Path,
    template_path: Path = DEFAULT_TEMPLATE,
    stylesheet_path: Path = DEFAULT_STYLESHEET,
) -> None:
    data = load_yaml(input_yaml)

    if not template_path.is_file():
        raise ResumeError(f"HTML template not found: {template_path}")
    if not stylesheet_path.is_file():
        raise ResumeError(f"Stylesheet not found: {stylesheet_path}")

    environment = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=select_autoescape(("html", "xml")),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    environment.filters["richtext"] = richtext
    template = environment.get_template(template_path.name)

    stylesheet = stylesheet_path.read_text(encoding="utf-8")
    output_html.parent.mkdir(parents=True, exist_ok=True)
    write_text(
        output_html,
        template.render(**data, stylesheet=stylesheet),
        newline="\n",
    )


def find_browser(explicit_browser: str | None = None) -> Path:
    candidates: list[Path] = []

    if explicit_browser:
        candidates.append(Path(explicit_browser))

    for executable in ("msedge", "msedge.exe", "chrome", "chrome.exe", "chromium"):
        located = shutil.which(executable)
        if located:
            candidates.append(Path(located))

    if sys.platform == "win32":
        candidates.extend(
            [
                Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
                Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
                Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
                Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
            ]
        )
    elif sys.platform == "darwin":
        candidates.extend(
            [
                Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
                Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
            ]
        )

    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()

    raise ResumeError(
        "Microsoft Edge, Google Chrome, or Chromium was not found. "
        "Install one of them or render with --skip-pdf."
    )


def render_pdf(
    input_html: Path,
    output_pdf: Path,
    browser_path: str | None = None,
) -> None:
    browser = find_browser(browser_path)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    temporary_pdf = output_pdf.with_name(f".{output_pdf.stem}.rendering.pdf")
    if temporary_pdf.exists():
        temporary_pdf.unlink()

    source_uri = input_html.resolve().as_uri()
    attempts: list[str] = []

    # Some Chrome/Edge builds hang indefinitely when printing to PDF with
    # "--headless=new" (notably on macOS). Try it first, then fall back to the
    # classic "--headless" mode if it stalls or fails.
    for headless_flag in ("--headless=new", "--headless"):
        with tempfile.TemporaryDirectory(prefix="resume-browser-") as profile:
            command = [
                str(browser),
                headless_flag,
                "--disable-gpu",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-extensions",
                "--disable-background-networking",
                "--hide-scrollbars",
                "--no-pdf-header-footer",
                "--virtual-time-budget=10000",
                f"--user-data-dir={profile}",
                f"--print-to-pdf={temporary_pdf.resolve()}",
                source_uri,
            ]
            try:
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=90,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                attempts.append(f"{headless_flag}: timed out after 90 seconds")
                temporary_pdf.unlink(missing_ok=True)
                continue

        if result.returncode != 0:
            details = (result.stderr or result.stdout).strip()
            attempts.append(
                f"{headless_flag}: exit code {result.returncode}. {details}".strip()
            )
            temporary_pdf.unlink(missing_ok=True)
            continue

        if not temporary_pdf.is_file() or temporary_pdf.stat().st_size < 1000:
            attempts.append(f"{headless_flag}: did not produce a valid PDF")
            temporary_pdf.unlink(missing_ok=True)
            continue

        temporary_pdf.replace(output_pdf)
        return

    raise ResumeError(
        "Browser PDF rendering failed:\n  "
        + "\n  ".join(attempts)
        + "\nThe HTML preview was still generated; you can open it in a browser "
        "and use Print > Save as PDF instead."
    )


def render_resume(
    input_yaml: Path,
    output_html: Path,
    output_pdf: Path | None,
    template_path: Path = DEFAULT_TEMPLATE,
    stylesheet_path: Path = DEFAULT_STYLESHEET,
    browser_path: str | None = None,
) -> None:
    render_html(input_yaml, output_html, template_path, stylesheet_path)
    if output_pdf is not None:
        render_pdf(output_html, output_pdf, browser_path)


def open_in_browser(html_path: Path) -> None:
    """Open a rendered HTML file in the user's default browser.

    Used as a reliable alternative to automatic PDF generation: the browser's
    own Print > Save as PDF always works, even where headless PDF rendering is
    blocked (e.g. some managed macOS machines).
    """
    try:
        webbrowser.open(html_path.resolve().as_uri())
    except Exception:  # noqa: BLE001 - opening a browser is best effort
        pass


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    if not slug:
        raise ResumeError(f"Could not create a folder-safe name from {value!r}")
    return slug


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ResumeError("Application date must use YYYY-MM-DD format.") from exc


def master_path_for_args(args: argparse.Namespace) -> Path:
    if args.master:
        return Path(args.master).resolve()
    return MASTER_PROFILES[args.master_profile]["path"].resolve()


RENDER_CMD_CONTENT = (
    "@echo off\n"
    'python "%~dp0..\\..\\..\\system\\resume_tool.py" render '
    '-Input "%~dp0resume.yaml" '
    '-OutputHtml "%~dp0index.html" '
    '-OutputPdf "%~dp0resume.pdf" %*\n'
)

RENDER_COMMAND_CONTENT = (
    "#!/usr/bin/env bash\n"
    "# Re-render this application on macOS.\n"
    "# Double-click in Finder (macOS) or run from a terminal.\n"
    "# This is the macOS equivalent of Render.cmd.\n"
    'DIR="$(cd "$(dirname "$0")" && pwd)"\n'
    "if command -v python3 >/dev/null 2>&1; then\n"
    "  PY=python3\n"
    "elif command -v python >/dev/null 2>&1; then\n"
    "  PY=python\n"
    "else\n"
    '  echo "Python 3 was not found. Install it from '
    'https://www.python.org/downloads/ and try again."\n'
    "  exit 1\n"
    "fi\n"
    'if "$PY" "$DIR/../../../system/resume_tool.py" render '
    '-Input "$DIR/resume.yaml" '
    '-OutputHtml "$DIR/index.html" '
    '-OutputPdf "$DIR/resume.pdf" "$@"; then\n'
    "  exit 0\n"
    "fi\n"
    "\n"
    'echo "Automatic PDF generation failed; opening the HTML print preview instead."\n'
    '"$PY" "$DIR/../../../system/resume_tool.py" render '
    '-Input "$DIR/resume.yaml" '
    '-OutputHtml "$DIR/index.html" '
    '-SkipPdf -Open "$@"\n'
    "\n"
    "exit $?\n"
)


def write_render_launchers(application_folder: Path) -> None:
    """Write the Windows (.cmd) and macOS/Linux (.command) render launchers."""
    write_text(application_folder / "Render.cmd", RENDER_CMD_CONTENT, newline="\r\n")
    command_launcher = application_folder / "Render.command"
    write_text(command_launcher, RENDER_COMMAND_CONTENT, newline="\n")
    command_launcher.chmod(0o755)


def create_application(args: argparse.Namespace) -> None:
    application_date = parse_date(args.application_date)
    master_path = master_path_for_args(args)
    destination_root = Path(args.destination_root).resolve()
    resume_type = args.master_profile if not args.master else "custom"
    folder_name = (
        f"{application_date.isoformat()}-{resume_type}-"
        f"{slugify(args.company)}-{slugify(args.role)}"
    )
    application_folder = destination_root / str(application_date.year) / folder_name

    if application_folder.exists():
        raise ResumeError(
            f"Application folder already exists: {application_folder}\n"
            "Use a distinct role name or include the job ID."
        )

    application_folder.mkdir(parents=True)
    application_yaml = application_folder / "resume.yaml"
    shutil.copy2(master_path, application_yaml)

    data = load_yaml(application_yaml)
    data["application"] = {
        "master_profile": resume_type,
        "company": args.company,
        "role": args.role,
        "job_url": args.job_url,
        "created": application_date.isoformat(),
        "status": "Preparing",
    }
    write_yaml(application_yaml, data)

    write_render_launchers(application_folder)

    output_html = application_folder / "index.html"
    output_pdf = None if args.skip_pdf else application_folder / "resume.pdf"
    try:
        render_resume(
            application_yaml,
            output_html,
            output_pdf,
            browser_path=args.browser,
        )
    except ResumeError as exc:
        if (
            not args.pdf_fallback_open
            or output_pdf is None
            or not output_html.is_file()
        ):
            raise
        print(f"Warning: {exc}", file=sys.stderr)
        print("Opening the generated HTML print preview instead.")
        open_in_browser(output_html)
        output_pdf = None

    print("Application created successfully:")
    print(f"  {application_folder}")
    print("")
    print("Files:")
    print("  resume.yaml  - edit job-specific content here")
    print("  index.html   - self-contained browser preview")
    if output_pdf:
        print("  resume.pdf   - submission-ready PDF")
    print("  Render.cmd / Render.command - re-render after editing YAML")


def migrate_application_launchers(args: argparse.Namespace) -> int:
    applications_root = PROJECT_ROOT / "applications"
    old_path = "..\\..\\..\\resume_tool.py"
    new_path = "..\\..\\..\\system\\resume_tool.py"
    migrated = 0
    refreshed_command = 0

    for launcher in applications_root.glob("*/*/Render.cmd"):
        text = launcher.read_text(encoding="utf-8")
        updated = text.replace(old_path, new_path)
        if updated != text:
            write_text(launcher, updated, newline="\r\n")
            migrated += 1

        # Always refresh the macOS/Linux launcher so behavior changes (e.g. the
        # build-HTML-and-open flow) reach existing application folders too.
        command_launcher = launcher.with_name("Render.command")
        current = command_launcher.read_text(encoding="utf-8") if command_launcher.exists() else None
        if current != RENDER_COMMAND_CONTENT:
            write_text(command_launcher, RENDER_COMMAND_CONTENT, newline="\n")
            refreshed_command += 1
        command_launcher.chmod(0o755)

    if not args.quiet:
        print(f"Updated application launchers: {migrated}")
        print(f"Refreshed macOS/Linux launchers: {refreshed_command}")
    return 0


def prompt_required(label: str) -> str:
    while True:
        value = input(label).strip()
        if value:
            return value
        print("This value is required. Please try again.")


def wizard_command(args: argparse.Namespace) -> int:
    print("=" * 60)
    print("            Create a tailored resume application")
    print("=" * 60)
    print("")
    print("This wizard copies your master YAML, creates a job folder,")
    print("and renders the custom HTML resume and PDF.")
    print("")

    print("Choose the master resume for this application:")
    profile_names = list(MASTER_PROFILES)
    for number, profile_name in enumerate(profile_names, start=1):
        label = MASTER_PROFILES[profile_name]["label"]
        default_marker = " (default)" if profile_name == DEFAULT_MASTER_PROFILE else ""
        print(f"  {number}. {label}{default_marker}")
    while True:
        profile_choice = input("Master resume [1]: ").strip() or "1"
        if profile_choice.isdigit() and 1 <= int(profile_choice) <= len(profile_names):
            master_profile = profile_names[int(profile_choice) - 1]
            break
        print(f"Enter a number from 1 to {len(profile_names)}.")
    print("")

    company = prompt_required("Company name: ")
    role = prompt_required("Role or position title: ")
    job_url = input("Job URL (optional): ").strip()

    while True:
        application_date = input(
            "Application date YYYY-MM-DD (press Enter for today): "
        ).strip()
        if not application_date:
            application_date = date.today().isoformat()
            break
        try:
            parse_date(application_date)
            break
        except ResumeError as exc:
            print(exc)

    print("")
    print("-" * 60)
    print(f"Master:  {MASTER_PROFILES[master_profile]['label']}")
    print(f"Company: {company}")
    print(f"Role:    {role}")
    if job_url:
        print(f"URL:     {job_url}")
    print(f"Date:    {application_date}")
    print("PDF:     Yes (automatic)")
    print("-" * 60)
    print("")

    create_args = argparse.Namespace(
        company=company,
        role=role,
        job_url=job_url,
        application_date=application_date,
        master=None,
        master_profile=master_profile,
        destination_root=str(PROJECT_ROOT / "applications"),
        browser=args.browser,
        skip_pdf=False,
        pdf_fallback_open=args.pdf_fallback_open,
    )

    print("")
    try:
        create_application(create_args)
    except (ResumeError, OSError, subprocess.SubprocessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        print("")
        input("Press Enter to close this window...")
        return 1

    print("")
    print("Finished. Edit resume.yaml in the new application folder,")
    print("then run its Render.cmd (Windows) or Render.command (macOS) to rebuild it.")
    print("")
    input("Press Enter to close this window...")
    return 0


def render_command(args: argparse.Namespace) -> None:
    output_pdf = None if args.skip_pdf else Path(args.output_pdf).resolve()
    output_html = Path(args.output_html).resolve()
    render_resume(
        Path(args.input).resolve(),
        output_html,
        output_pdf,
        browser_path=args.browser,
    )
    print(f"Generated HTML: {output_html}")
    if output_pdf:
        print(f"Generated PDF:  {output_pdf}")
    if getattr(args, "open_html", False):
        print("Opening in your browser - use Print (Cmd+P) > Save as PDF.")
        open_in_browser(output_html)


def render_masters_command(args: argparse.Namespace) -> None:
    # Render a single canonical master resume. The four focus profiles
    # (wearable-tech, robotics, design, machine-learning) are not rendered
    # here -- they exist only as starting points you choose per job in the
    # New-Application wizard.
    profile = MASTER_PROFILES[DEFAULT_MASTER_PROFILE]
    output_html = SYSTEM_ROOT / "index.html"
    output_pdf = None if args.skip_pdf else PROJECT_ROOT / "Ehsan-Sharafian-Resume.pdf"
    render_resume(
        profile["path"],
        output_html,
        output_pdf,
        browser_path=args.browser,
    )
    print(f"Generated master HTML: {output_html}")
    if output_pdf:
        print(f"Generated master PDF:  {output_pdf}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render Ehsan Sharafian's YAML resume into HTML and PDF."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser(
        "create", help="Create and render a job-specific application folder."
    )
    create.add_argument("-Company", "--company", required=True)
    create.add_argument("-Role", "--role", required=True)
    create.add_argument("-JobUrl", "--job-url", default="")
    create.add_argument(
        "-ApplicationDate",
        "--application-date",
        default=date.today().isoformat(),
        help="Application date in YYYY-MM-DD format.",
    )
    create.add_argument(
        "-Master",
        "--master",
        default=None,
        help="Custom master YAML source (overrides --master-profile).",
    )
    create.add_argument(
        "-MasterProfile",
        "--master-profile",
        choices=MASTER_PROFILES,
        default=DEFAULT_MASTER_PROFILE,
        help="Master resume profile to use.",
    )
    create.add_argument(
        "-DestinationRoot",
        "--destination-root",
        default=str(PROJECT_ROOT / "applications"),
    )
    create.add_argument("-Browser", "--browser", default=None)
    create.add_argument("-SkipPdf", "--skip-pdf", action="store_true")
    create.add_argument("--pdf-fallback-open", action="store_true", help=argparse.SUPPRESS)
    create.set_defaults(handler=create_application)

    wizard = subparsers.add_parser(
        "wizard", help="Open an interactive job-application wizard."
    )
    wizard.add_argument("-Browser", "--browser", default=None)
    wizard.add_argument("--pdf-fallback-open", action="store_true", help=argparse.SUPPRESS)
    wizard.set_defaults(handler=wizard_command)

    migrate = subparsers.add_parser(
        "migrate", help="Update existing application Render.cmd launchers."
    )
    migrate.add_argument("--quiet", action="store_true")
    migrate.set_defaults(handler=migrate_application_launchers)

    render = subparsers.add_parser(
        "render", help="Render one YAML resume into HTML and PDF."
    )
    render.add_argument("-Input", "--input", required=True)
    render.add_argument("-OutputHtml", "--output-html", required=True)
    render.add_argument("-OutputPdf", "--output-pdf", default="resume.pdf")
    render.add_argument("-Browser", "--browser", default=None)
    render.add_argument("-SkipPdf", "--skip-pdf", action="store_true")
    render.add_argument(
        "-Open",
        "--open",
        dest="open_html",
        action="store_true",
        help="Open the rendered HTML in the default browser after rendering.",
    )
    render.set_defaults(handler=render_command)

    render_masters = subparsers.add_parser(
        "render-masters", help="Render all master resume profiles."
    )
    render_masters.add_argument("-Browser", "--browser", default=None)
    render_masters.add_argument("-SkipPdf", "--skip-pdf", action="store_true")
    render_masters.set_defaults(handler=render_masters_command)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.handler(args)
    except (ResumeError, OSError, subprocess.SubprocessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return int(result or 0)


if __name__ == "__main__":
    raise SystemExit(main())
