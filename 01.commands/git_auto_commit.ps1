git pull
git add .
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "Automatic sync and commit at $timestamp"
git push