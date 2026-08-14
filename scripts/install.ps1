# Claude Code Skills Installation Script for Windows
# This script links or copies the skills to your Claude Code configuration

$ErrorActionPreference = "Stop"

# Get the script directory
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptRoot
$SkillsSource = Join-Path $ProjectRoot "skills"

# Claude Code config path
$ClaudeConfigPath = "$env:USERPROFILE\.claude"
$SkillsTarget = Join-Path $ClaudeConfigPath "skills"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Claude Code Skills Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if skills directory exists
if (!(Test-Path $SkillsSource)) {
    Write-Host "ERROR: Skills directory not found at: $SkillsSource" -ForegroundColor Red
    exit 1
}

Write-Host "Source: $SkillsSource" -ForegroundColor Yellow
Write-Host "Target: $SkillsTarget" -ForegroundColor Yellow
Write-Host ""

# Check if Claude config directory exists
if (!(Test-Path $ClaudeConfigPath)) {
    Write-Host "Creating Claude Code config directory..." -ForegroundColor Green
    New-Item -ItemType Directory -Path $ClaudeConfigPath | Out-Null
}

# Check if skills target already exists
if (Test-Path $SkillsTarget) {
    $item = Get-Item $SkillsTarget
    if ($item.LinkType -eq "SymbolicLink") {
        Write-Host "Existing symbolic link found." -ForegroundColor Yellow
        $choice = Read-Host "Remove and recreate? (y/N)"
        if ($choice -eq "y" -or $choice -eq "Y") {
            Remove-Item $SkillsTarget -Force
            Write-Host "Removed existing link." -ForegroundColor Green
        } else {
            Write-Host "Installation cancelled." -ForegroundColor Yellow
            exit 0
        }
    } elseif (Test-Path (Join-Path $SkillsTarget ".git")) {
        Write-Host "ERROR: Target is a git repository. Remove manually if needed." -ForegroundColor Red
        exit 1
    } else {
        Write-Host "Existing directory found. This will be replaced." -ForegroundColor Yellow
        $choice = Read-Host "Continue? (y/N)"
        if ($choice -eq "y" -or $choice -eq "Y") {
            Remove-Item $SkillsTarget -Recurse -Force
            Write-Host "Removed existing directory." -ForegroundColor Green
        } else {
            Write-Host "Installation cancelled." -ForegroundColor Yellow
            exit 0
        }
    }
}

# Create symbolic link
Write-Host ""
Write-Host "Creating symbolic link..." -ForegroundColor Green
try {
    New-Item -ItemType SymbolicLink -Path $SkillsTarget -Target $SkillsSource | Out-Null
    Write-Host "SUCCESS: Symbolic link created!" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Could not create symbolic link (may require admin permissions)" -ForegroundColor Yellow
    Write-Host "Falling back to directory copy..." -ForegroundColor Yellow

    # Check if junction is supported
    try {
        # Try using junction instead
        & cmd /c "mklink /J `"$SkillsTarget`" `"$SkillsSource`"" | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "SUCCESS: Junction created!" -ForegroundColor Green
        } else {
            throw "Junction creation failed"
        }
    } catch {
        # Fall back to copy
        Write-Host "Creating directory copy..." -ForegroundColor Yellow
        Copy-Item -Path $SkillsSource -Destination $SkillsTarget -Recurse
        Write-Host "SUCCESS: Directory copied!" -ForegroundColor Green
        Write-Host "NOTE: Updates to skills won't be reflected automatically." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Skills are now available in Claude Code:" -ForegroundColor Green
Get-ChildItem $SkillsSource -Directory | ForEach-Object {
    $skillMd = Join-Path $_.FullName "skill.md"
    $title = $null
    if (Test-Path $skillMd) {
        $match = Select-String -Path $skillMd -Pattern '^title:\s*(.+)$' | Select-Object -First 1
        if ($match) {
            $title = ($match.Line -replace '^title:\s*', '').Trim().Trim('"', "'")
        }
    }
    if (-not $title) { $title = $_.Name }
    Write-Host "  - $title" -ForegroundColor White
}
Write-Host ""
