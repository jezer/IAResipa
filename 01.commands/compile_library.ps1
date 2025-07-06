# PowerShell script to compile the library and generate a wheel file

$libraryName = "resipaia"
$version = "1.0.0"  # Update this version as needed
$date = Get-Date -Format "yyyy_MM_dd_HH_mm"
$wheelFileName = "${libraryName}_${version}_${date}.whl"

# Navigate to the project directory
Set-Location -Path (Join-Path -Path $PSScriptRoot -ChildPath "..")

# Run the setup script to build the library
python setup.py bdist_wheel

# Move the generated wheel file to the desired location
$generatedWheelPath = Join-Path -Path "dist" -ChildPath "*.whl"
$destinationPath = Join-Path -Path "dist" -ChildPath $wheelFileName

# Rename the generated wheel file
Get-ChildItem -Path $generatedWheelPath | Rename-Item -NewName $wheelFileName

Write-Host "Library compiled successfully. Wheel file created: $destinationPath"