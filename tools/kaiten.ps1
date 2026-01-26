<#
.SYNOPSIS
    Kaiten board manager via GitHub Actions

.DESCRIPTION
    Triggers GitHub Actions workflow to interact with Kaiten board.
    Bypasses corporate firewall by running actions on GitHub's servers.

.EXAMPLE
    .\kaiten.ps1 list-boards
    .\kaiten.ps1 list-cards -BoardId 12345
    .\kaiten.ps1 create-card -BoardId 12345 -ColumnId 67890 -Title "New task"
    .\kaiten.ps1 close-card -CardId 11111
#>

param(
    [Parameter(Position=0, Mandatory=$true)]
    [ValidateSet("list-boards", "list-cards", "create-card", "update-card", "move-card", "close-card")]
    [string]$Action,

    [string]$BoardId,
    [string]$CardId,
    [string]$ColumnId,
    [string]$Title,
    [string]$Description
)

$repo = "majdkassawat/RecycleWebsite"

# Build the inputs
$inputs = @()
$inputs += "-f", "action=$Action"

if ($BoardId) { $inputs += "-f", "board_id=$BoardId" }
if ($CardId) { $inputs += "-f", "card_id=$CardId" }
if ($ColumnId) { $inputs += "-f", "column_id=$ColumnId" }
if ($Title) { $inputs += "-f", "title=$Title" }
if ($Description) { $inputs += "-f", "description=$Description" }

Write-Host "🚀 Triggering Kaiten action: $Action" -ForegroundColor Cyan

# Trigger the workflow
$result = gh workflow run kaiten.yml --repo $repo @inputs 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Workflow triggered successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "View results at: https://github.com/$repo/actions" -ForegroundColor Yellow
    Write-Host ""
    
    # Wait a moment then show the run
    Start-Sleep -Seconds 3
    gh run list --repo $repo --workflow kaiten.yml --limit 1
} else {
    Write-Host "❌ Failed to trigger workflow: $result" -ForegroundColor Red
}
