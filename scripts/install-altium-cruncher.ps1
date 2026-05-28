#Requires -Version 5.1

[CmdletBinding()]
param(
    [string]$Version = "",
    [switch]$IncludeEasyeda,
    [switch]$Force,
    [switch]$SkipUvInstall,
    [switch]$NoUpdateShell
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([Parameter(Mandatory = $true)][string]$Message)

    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Resolve-CommandPath {
    param([Parameter(Mandatory = $true)][string]$Name)

    $command = Get-Command -Name $Name -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }

    return $null
}

function Add-DirectoryToPath {
    param([string]$Directory)

    if (-not $Directory) {
        return
    }
    if (-not (Test-Path -LiteralPath $Directory)) {
        return
    }

    $pathEntries = $env:Path -split ";"
    if ($pathEntries -notcontains $Directory) {
        $env:Path = "$Directory;$env:Path"
    }
}

function Resolve-UvPath {
    $uvPath = Resolve-CommandPath -Name "uv"
    if ($uvPath) {
        return $uvPath
    }

    $candidates = @(
        (Join-Path $HOME ".local\bin\uv.exe"),
        (Join-Path $env:USERPROFILE ".local\bin\uv.exe"),
        (Join-Path $env:USERPROFILE ".cargo\bin\uv.exe")
    )

    foreach ($candidate in $candidates) {
        if ($candidate -and (Test-Path -LiteralPath $candidate)) {
            return $candidate
        }
    }

    return $null
}

Write-Step "Checking for uv"
$uv = Resolve-UvPath

if (-not $uv) {
    if ($SkipUvInstall) {
        throw "uv was not found. Install uv first or rerun without -SkipUvInstall."
    }

    Write-Step "Installing uv"
    & powershell -NoProfile -ExecutionPolicy ByPass -Command "irm https://astral.sh/uv/install.ps1 | iex"
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Add-DirectoryToPath -Directory (Join-Path $HOME ".local\bin")
    Add-DirectoryToPath -Directory (Join-Path $env:USERPROFILE ".local\bin")
    Add-DirectoryToPath -Directory (Join-Path $env:USERPROFILE ".cargo\bin")

    $uv = Resolve-UvPath
    if (-not $uv) {
        throw "uv install completed, but uv.exe was not found on PATH. Open a new PowerShell window and run this script again."
    }
}

Write-Host "Using uv: $uv"

$packageName = "altium-cruncher"
if ($IncludeEasyeda) {
    $packageName = "altium-cruncher[easyeda]"
}

$packageSpec = $packageName
if ($Version.Trim()) {
    $packageSpec = "$packageName==$($Version.Trim())"
}

Write-Step "Installing $packageSpec"
$installArgs = @("tool", "install")
if ($Force) {
    $installArgs += "--force"
}
$installArgs += $packageSpec

& $uv @installArgs
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

$toolBin = (& $uv tool dir --bin | Select-Object -Last 1).Trim()
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
Add-DirectoryToPath -Directory $toolBin

if (-not $NoUpdateShell) {
    Write-Step "Updating shell PATH"
    & $uv tool update-shell
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "uv tool update-shell did not complete. The tool is installed, but you may need to add '$toolBin' to PATH or open a new shell."
    }
}

$altiumCruncher = Resolve-CommandPath -Name "altium-cruncher"
if (-not $altiumCruncher) {
    $candidate = Join-Path $toolBin "altium-cruncher.exe"
    if (Test-Path -LiteralPath $candidate) {
        $altiumCruncher = $candidate
    }
}

if (-not $altiumCruncher) {
    throw "altium-cruncher was installed, but the executable was not found. Open a new PowerShell window and run 'altium-cruncher version'."
}

Write-Step "Verifying installation"
& $altiumCruncher version
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "altium-cruncher is installed. Open a new PowerShell window if the command is not available in existing shells." -ForegroundColor Green
