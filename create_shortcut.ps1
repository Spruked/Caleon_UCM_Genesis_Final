# Create desktop shortcut for UCM startup
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$([Environment]::GetFolderPath('Desktop'))\Start UCM.lnk")
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-ExecutionPolicy Bypass -File ""$PSScriptRoot\start_ucm.ps1"""
$Shortcut.WorkingDirectory = "$PSScriptRoot"
$Shortcut.IconLocation = "powershell.exe,0"
$Shortcut.Description = "Start UCM Cognitive Architecture"
$Shortcut.Save()

Write-Host "Desktop shortcut created successfully!"
Write-Host "Location: $([Environment]::GetFolderPath('Desktop'))\Start UCM.lnk"