param (
    [switch]$Install = $false
)

$pandocInstalled = $false
$pythonDocxInstalled = $false

# Check Pandoc
try {
    $pandocVersion = pandoc --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $pandocInstalled = $true
        Write-Host "[+] Pandoc is installed." -ForegroundColor Green
    }
} catch {
    Write-Host "[-] Pandoc is NOT installed." -ForegroundColor Red
}

# Check python-docx
try {
    $pipCheck = python -c "import docx" 2>&1
    if ($LASTEXITCODE -eq 0) {
        $pythonDocxInstalled = $true
        Write-Host "[+] python-docx is installed." -ForegroundColor Green
    } else {
        Write-Host "[-] python-docx is NOT installed." -ForegroundColor Red
    }
} catch {
    Write-Host "[-] python-docx is NOT installed (or Python is missing)." -ForegroundColor Red
}

if ($Install) {
    if (-not $pandocInstalled) {
        Write-Host "[*] Attempting to install Pandoc via winget..." -ForegroundColor Yellow
        winget install --id JohnMacFarlane.Pandoc -e --source winget --accept-package-agreements --accept-source-agreements
    }
    if (-not $pythonDocxInstalled) {
        Write-Host "[*] Attempting to install python-docx via pip..." -ForegroundColor Yellow
        python -m pip install python-docx
    }
    Write-Host "[*] Installation phase complete. Please re-run without -Install to verify." -ForegroundColor Cyan
} else {
    if (-not $pandocInstalled -or -not $pythonDocxInstalled) {
        Write-Host "`nWARNING: Missing dependencies detected." -ForegroundColor Yellow
        Write-Host "Antigravity Agent: You should ask the user for permission to install these dependencies by running this script again with the -Install flag." -ForegroundColor Yellow
    } else {
        Write-Host "`nAll dependencies are installed. You may proceed to Phase 1." -ForegroundColor Green
    }
}
