param (
    [Parameter(Mandatory=$true)]
    [string]$File
)

if (-not (Test-Path $File)) {
    Write-Host "[-] File not found: $File" -ForegroundColor Red
    exit 1
}

$content = Get-Content -Path $File -Raw
$words = ($content -split '\s+').Count
Write-Host "[*] Word count for $File : $words words" -ForegroundColor Cyan
