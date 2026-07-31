$ErrorActionPreference = "Stop"
$Project = Split-Path -Parent $MyInvocation.MyCommand.Path
$Release = Join-Path $Project "build\portable-staging\DouyinLeadSystem-Portable"
$OutputDir = Join-Path $Project "release"
$BasePython = "C:\Users\12131\AppData\Roaming\uv\python\cpython-3.10.18-windows-x86_64-none"
$Venv = Join-Path $Project ".venv310"

if (!(Test-Path "$BasePython\python.exe")) { throw "Python 3.10 runtime not found" }
if (!(Test-Path "$Venv\Lib\site-packages")) { throw "Python 3.10 packages not found" }

if (Test-Path $Release) {
    $ResolvedStage = (Resolve-Path $Release).Path
    $ExpectedRoot = (Resolve-Path (Join-Path $Project "build")).Path
    if (!$ResolvedStage.StartsWith($ExpectedRoot)) { throw "Unsafe staging path" }
    Remove-Item -LiteralPath $ResolvedStage -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $Release | Out-Null
New-Item -ItemType Directory -Force -Path "$Release\runtime\Lib\site-packages" | Out-Null
New-Item -ItemType Directory -Force -Path "$Release\data\logs","$Release\data\exports","$Release\data\backups" | Out-Null

& robocopy $BasePython "$Release\runtime" /E /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "Runtime copy failed: $LASTEXITCODE" }
& robocopy "$Venv\Lib\site-packages" "$Release\runtime\Lib\site-packages" /E /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "Package copy failed: $LASTEXITCODE" }
& robocopy "$Project\app" "$Release\app" /E /XD __pycache__ /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "App copy failed: $LASTEXITCODE" }
& robocopy "$Project\server" "$Release\server" /E /XD __pycache__ logs /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "Server copy failed: $LASTEXITCODE" }

& "$Venv\Scripts\pyinstaller.exe" --noconfirm --clean --onefile --windowed --name "DouyinLeadSystem" --distpath $Release --workpath "$Project\build\launcher" --specpath "$Project\build" "$Project\launcher.py"
$Readme = Get-ChildItem -LiteralPath $Project -Filter "*.txt" | Where-Object { $_.Name -ne "version.txt" } | Select-Object -First 1
Copy-Item $Readme.FullName "$Release\README.txt" -Force
Set-Content -Path "$Release\version.txt" -Encoding UTF8 -Value "Douyin Lead System Portable`r`nVersion: 1.2.5`r`nPython: 3.10.18`r`nData: data"

$Zip = Join-Path $OutputDir "DouyinLeadSystem-Portable-v1.2.5.zip"
if (Test-Path $Zip) { Remove-Item -LiteralPath $Zip -Force }
& tar.exe -a -cf $Zip -C (Split-Path $Release -Parent) (Split-Path $Release -Leaf)
if ($LASTEXITCODE -ne 0) { throw "ZIP creation failed: $LASTEXITCODE" }
Write-Output $Release
Write-Output $Zip
