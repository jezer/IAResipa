# PowerShell script to compile the library and generate a wheel file

# Navigate to the project root directory
Set-Location -Path (Join-Path -Path $PSScriptRoot -ChildPath "..")

# Clean up previous builds
Remove-Item -Path "build", "dist", "*.egg-info" -Recurse -ErrorAction SilentlyContinue

# Run the setup script to build the library (sdist and bdist_wheel)
python setup.py sdist bdist_wheel

Write-Host "Library compiled successfully. Wheel file(s) and source distribution created in the 'dist/' directory."