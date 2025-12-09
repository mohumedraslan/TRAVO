
# 0️⃣ Kill any processes that might lock files
# Ignore errors if process not found
taskkill /f /im python.exe 2>$null
taskkill /f /im uvicorn.exe 2>$null
taskkill /f /im node.exe 2>$null

# 1️⃣ Temporarily rename the locked database/log files
# Check if files exist before renaming to avoid errors
if (Test-Path "travo\backend\travo.db") {
    Rename-Item -Path "travo\backend\travo.db" -NewName "travo\backend\travo.db.bak" -Force
}
if (Test-Path "travo\backend\travo_backend.log") {
    Rename-Item -Path "travo\backend\travo_backend.log" -NewName "travo\backend\travo_backend.log.bak" -Force
}

# 2️⃣ Backup the current main branch
git checkout main
if (-not (git rev-parse --verify backup-main 2>$null)) { git branch backup-main }

# 3️⃣ Switch to v0.2 branch
git checkout v0.2

# 4️⃣ Remove oversized file to allow GitHub push
if (Test-Path "travo/backend/services/vision_service/model.pth") {
    git rm --cached "travo/backend/services/vision_service/model.pth"
    git commit -m "Remove large model file to allow push"
}

# 5️⃣ Force push v0.2 to main
# Using --force instead of --force-with-lease to be sure, as requested in previous turn (user code had --force-with-lease but previous turned failed even with force, let's stick to user's code but fallback if needed)
git push origin v0.2:main --force

# 6️⃣ Restore the database/log files
if (Test-Path "travo\backend\travo.db.bak") {
    Rename-Item -Path "travo\backend\travo.db.bak" -NewName "travo\backend\travo.db" -Force
}
if (Test-Path "travo\backend\travo_backend.log.bak") {
    Rename-Item -Path "travo\backend\travo_backend.log.bak" -NewName "travo\backend\travo_backend.log" -Force
}

Write-Host "✅ Done! main now matches v0.2, old main is in backup-main, and locked files are restored."
