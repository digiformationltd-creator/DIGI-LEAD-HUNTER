# Digiformation LTD — Lead Hunter Start Script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
Set-Location "$projectRoot"
python "$projectRoot
un.py"
