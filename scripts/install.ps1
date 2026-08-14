# Link skills/ into ~/.claude/skills (Windows).
# Usage: run as Administrator if you want a symlink; falls back to junction, then copy.
$ErrorActionPreference = "Stop"
$SkillsSource = Join-Path $PSScriptRoot ".." "skills"
$SkillsTarget = Join-Path $env:USERPROFILE ".claude" "skills"

if (!(Test-Path $SkillsSource)) { Write-Host "ERROR: skills/ not found at $SkillsSource" -f Red; exit 1 }
if (Test-Path $SkillsTarget) { Remove-Item $SkillsTarget -Recurse -Force }

try {
    New-Item -ItemType SymbolicLink -Path $SkillsTarget -Target $SkillsSource | Out-Null
    Write-Host "Linked (symlink): $SkillsTarget -> $SkillsSource"
} catch {
    try {
        & cmd /c "mklink /J `"$SkillsTarget`" `"$SkillsSource`"" | Out-Null
        Write-Host "Linked (junction): $SkillsTarget -> $SkillsSource"
    } catch {
        Copy-Item -Path $SkillsSource -Destination $SkillsTarget -Recurse
        Write-Host "Copied (no auto-update on future changes): $SkillsTarget"
    }
}
