[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string]$Company,

    [Parameter(Mandatory)]
    [ValidateNotNullOrEmpty()]
    [string]$Role,

    [ValidateNotNullOrEmpty()]
    [string]$Theme = "classic",

    [ValidateNotNullOrEmpty()]
    [string]$JobUrl = "",

    [ValidateNotNull()]
    [datetime]$ApplicationDate = (Get-Date),

    [ValidateNotNullOrEmpty()]
    [string]$PythonCommand = "python",

    [string]$DestinationRoot,

    [switch]$SkipRender
)

$ErrorActionPreference = "Stop"

function ConvertTo-Slug {
    param(
        [Parameter(Mandatory)]
        [string]$Value
    )

    $slug = $Value.ToLowerInvariant() -replace "[^a-z0-9]+", "-"
    $slug = $slug.Trim("-")

    if ([string]::IsNullOrWhiteSpace($slug)) {
        throw "Could not create a folder-safe name from '$Value'."
    }

    return $slug
}

$projectRoot = $PSScriptRoot
$masterYaml = Join-Path $projectRoot "master\Ehsan_Sharafian_Master.yaml"

if (-not (Test-Path -LiteralPath $masterYaml -PathType Leaf)) {
    throw "Master YAML not found: $masterYaml"
}

if ([string]::IsNullOrWhiteSpace($DestinationRoot)) {
    $DestinationRoot = Join-Path $projectRoot "applications"
}

$companySlug = ConvertTo-Slug -Value $Company
$roleSlug = ConvertTo-Slug -Value $Role
$dateText = $ApplicationDate.ToString("yyyy-MM-dd")
$yearText = $ApplicationDate.ToString("yyyy")
$folderName = "$dateText-$companySlug-$roleSlug"
$yearFolder = Join-Path $DestinationRoot $yearText
$applicationFolder = Join-Path $yearFolder $folderName

if (Test-Path -LiteralPath $applicationFolder) {
    throw "Application folder already exists: $applicationFolder"
}

New-Item -ItemType Directory -Path $applicationFolder -Force | Out-Null

$applicationYaml = Join-Path $applicationFolder "resume.yaml"
Copy-Item -LiteralPath $masterYaml -Destination $applicationYaml

$yaml = Get-Content -Raw -Encoding UTF8 -LiteralPath $applicationYaml
$yaml = $yaml -replace "(?m)^(\s*theme:\s*)\S+\s*$", "`${1}$Theme"
$yaml = $yaml -replace "(?m)^(\s*pdf_path:\s*).+$", "`${1}resume.pdf"
Set-Content -Encoding UTF8 -LiteralPath $applicationYaml -Value $yaml

$jobNotes = @"
# $Company - $Role

- Application date: $dateText
- Status: Preparing
- Job URL: $JobUrl
- Resume file: resume.pdf
- Theme: $Theme

## Important requirements

-

## Tailoring decisions

-

## Follow-up

-
"@

$jobNotesPath = Join-Path $applicationFolder "job.md"
Set-Content -Encoding UTF8 -LiteralPath $jobNotesPath -Value $jobNotes

if (-not $SkipRender) {
    $previousPythonUtf8 = $env:PYTHONUTF8
    $previousPythonIoEncoding = $env:PYTHONIOENCODING
    $env:PYTHONUTF8 = "1"
    $env:PYTHONIOENCODING = "utf-8"

    Push-Location $applicationFolder
    try {
        & $PythonCommand -m rendercv render ".\resume.yaml"
        if ($LASTEXITCODE -ne 0) {
            throw "RenderCV exited with code $LASTEXITCODE."
        }
    }
    finally {
        Pop-Location
        $env:PYTHONUTF8 = $previousPythonUtf8
        $env:PYTHONIOENCODING = $previousPythonIoEncoding
    }
}

Write-Host ""
Write-Host "Application created:"
Write-Host "  $applicationFolder"
Write-Host ""
Write-Host "Next:"
Write-Host "  1. Edit resume.yaml for the job."
Write-Host "  2. Update job.md with requirements and application status."
if ($SkipRender) {
    Write-Host "  3. Render from the folder with: python -m rendercv render .\resume.yaml"
}
else {
    Write-Host "  3. Re-render after editing with: python -m rendercv render .\resume.yaml"
}
