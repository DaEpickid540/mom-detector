# Mom Detector — Startup Command

Open **PowerShell as Administrator** (right-click Start → "Windows PowerShell (Admin)") and run this:

> ⚠️ Replace the path on line 1 with wherever you actually saved `mom_detector.py`

```powershell
$pyPath = "C:\Users\YourName\Documents\mom_detector\mom_detector.py"
$batPath = "$env:APPDATA\mom_detector_launch.bat"
Set-Content $batPath "@echo off`npythonw `"$pyPath`""
$action   = New-ScheduledTaskAction -Execute $batPath
$trigger  = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -Hidden
Register-ScheduledTask -TaskName "MomDetector" -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -Force
Start-ScheduledTask -TaskName "MomDetector"
Write-Host "Done! Mom Detector is running."
```

---

## Verify it's running

```
netstat -an | findstr 5555
```

You should see a line containing `0.0.0.0:5555`. If you do, you're good.

---

## Other useful commands

**Start it manually (if it ever stops):**

```powershell
Start-ScheduledTask -TaskName "MomDetector"
```

**Stop it:**

```powershell
Stop-ScheduledTask -TaskName "MomDetector"
```

**Remove it entirely:**

```powershell
Unregister-ScheduledTask -TaskName "MomDetector" -Confirm:$false
```
