# Remove the skills link from ~/.claude/skills (Windows).
$ErrorActionPreference = "Stop"
$SkillsTarget = Join-Path $env:USERPROFILE ".claude" "skills"
if (Test-Path (Join-Path $SkillsTarget ".git")) { Write-Host "Refusing: target is a git repo" -f Red; exit 1 }
if (Test-Path $SkillsTarget) { Remove-Item $SkillsTarget -Recurse -Force; Write-Host "Removed: $SkillsTarget" }
