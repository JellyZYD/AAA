$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")
python -m qihuo_signal update
python -m qihuo_signal poll --once

