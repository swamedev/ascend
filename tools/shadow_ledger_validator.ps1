# Shadow Ledger Validator (PowerShell Version)
# Valida a integridade do manifest.md e ADRs no Windows.

$manifestPath = Join-Path $PSScriptRoot "..\manifest.md"

if (-not (Test-Path $manifestPath)) {
    Write-Error "manifest.md nao encontrado em $manifestPath"
    exit 1
}

$content = Get-Content -Path $manifestPath -Raw

$hasArchMode = $content.Contains("ARCHITECTURE_MODE")
$hasAdrs = $content.Contains("## Architecture Decision Records")
$hasChangelog = $content.Contains("## Changelog")

$allOk = $true

Write-Host "=== SHADOW LEDGER VALIDATION ===" -ForegroundColor Cyan

if ($hasArchMode) { Write-Host "  ✅ ARCHITECTURE_MODE detectado" -ForegroundColor Green } else { Write-Host "  ❌ ARCHITECTURE_MODE ausente" -ForegroundColor Red; $allOk = $false }
if ($hasAdrs) { Write-Host "  ✅ Secao de ADRs detectada" -ForegroundColor Green } else { Write-Host "  ❌ Secao de ADRs ausente" -ForegroundColor Red; $allOk = $false }
if ($hasChangelog) { Write-Host "  ✅ Secao de Changelog detectada" -ForegroundColor Green } else { Write-Host "  ❌ Secao de Changelog ausente" -ForegroundColor Red; $allOk = $false }

# Extrai e valida ADRs usando expressão regular
$pattern = '### (ADR-\d+):[\s\S]*?\*\*Hash:\*\*\s*`([^`]+)`'
$matches = [regex]::Matches($content, $pattern)
$count = $matches.Count

Write-Host "  📋 Encontradas $count ADRs no manifesto." -ForegroundColor Yellow

foreach ($match in $matches) {
    $adrId = $match.Groups[1].Value
    $adrHash = $match.Groups[2].Value
    if ($adrHash -and $adrHash.Length -gt 5) {
        Write-Host "  ✅ $adrId — Hash: $adrHash" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $adrId — Hash invalido ou ausente!" -ForegroundColor Yellow
        $allOk = $false
    }
}

if ($allOk) {
    Write-Host "[LEDGER] ✅ INTEGRIDADE CONFIRMADA" -ForegroundColor Green
    exit 0
} else {
    Write-Host "[LEDGER] ⚠️ PROBLEMAS DETECTADOS" -ForegroundColor Red
    exit 1
}
