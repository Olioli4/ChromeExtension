# PowerShell script to organize project files into a standard structure

# Define folder structure
$folders = @(
    "src",
    "test",
    "docs",
    "assets",
    "automation"
)

# Create folders if they don't exist
foreach ($folder in $folders) {
    if (-not (Test-Path -Path $folder)) {
        New-Item -ItemType Directory -Path $folder | Out-Null
    }
}

# Move Python source files to src/
$srcFiles = @("main.py", "Functions.py", "form_widgets.py", "toggle_image_widget.py")
foreach ($file in $srcFiles) {
    if (Test-Path -Path $file) {
        Move-Item -Path $file -Destination src/ -Force
    }
}

# Move test files to test/ (example: test_main.py, test_functions.py)
Get-ChildItem -Path . -Filter "test_*.py" | ForEach-Object {
    Move-Item -Path $_.FullName -Destination test/ -Force
}

# Move documentation files to docs/ (example: architecture.md, usage.md)
Get-ChildItem -Path . -Include "architecture.md", "usage.md" -File | ForEach-Object {
    Move-Item -Path $_.FullName -Destination docs/ -Force
}

# Move all PNGs and static resources from Assets/ to assets/
if (Test-Path -Path "Assets") {
    Get-ChildItem -Path Assets -File | ForEach-Object {
        Move-Item -Path $_.FullName -Destination assets/ -Force
    }
    Remove-Item -Path Assets -Recurse -Force
}

# Move automation scripts to automation/
$automationFiles = @("setup-vscode-instructions.ps1")
foreach ($file in $automationFiles) {
    if (Test-Path -Path $file) {
        Move-Item -Path $file -Destination automation/ -Force
    }
}

# .vscode folder, README.md, Instructions.instructions.md remain at root
Write-Host "Project files have been organized into the standard structure."
