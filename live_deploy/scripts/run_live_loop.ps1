$ErrorActionPreference = "Continue"
Set-Location (Join-Path $PSScriptRoot "..")
$loopIntervalSeconds = if ($env:QIHUO_LOOP_INTERVAL_SECONDS) { [int]$env:QIHUO_LOOP_INTERVAL_SECONDS } else { 900 }
$newsIntervalSeconds = if ($env:QIHUO_NEWS_INTERVAL_SECONDS) { [int]$env:QIHUO_NEWS_INTERVAL_SECONDS } else { 28800 }
$lastNewsAt = [DateTimeOffset]::FromUnixTimeSeconds(0)
while ($true) {
  Get-Date
  python -m qihuo_signal update
  python -m qihuo_signal poll --once
  $now = [DateTimeOffset]::UtcNow
  if (($now.ToUnixTimeSeconds() - $lastNewsAt.ToUnixTimeSeconds()) -ge $newsIntervalSeconds) {
    python -m qihuo_signal news-poll
    if ($LASTEXITCODE -eq 0) {
      $lastNewsAt = $now
    }
  }
  Start-Sleep -Seconds $loopIntervalSeconds
}
