$ErrorActionPreference = "Continue"
Set-Location (Join-Path $PSScriptRoot "..")
while ($true) {
  Get-Date
  python -m qihuo_signal update
  python -m qihuo_signal poll --once
  python -m qihuo_signal news-poll
  Start-Sleep -Seconds 900
}

