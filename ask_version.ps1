# PowerShell script to prompt for a version number and push to git with a versioned commit message

$version = Read-Host "Enter version number for this commit"
if ([string]::IsNullOrWhiteSpace($version)) {
    Write-Host "No version entered. Aborting."
    exit 1
}

$commitMessage = "Release version $version"

try {
    git add -A
    git commit -m "$commitMessage"
    git push
    Write-Host "Successfully pushed with commit message: $commitMessage"
} catch {
    Write-Host "Git command failed: $_"
    exit 1
}
