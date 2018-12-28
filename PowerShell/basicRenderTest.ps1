class ProcessSettings {
    [string] $blenderLocation
    [string] $renderLocation
    [string] $scriptLocation
    [string] $renderFormat

    [string] $file
    [string] $camType
    [string] $renderSize
    [int] $pixBorder
    [string] $camRot
    [int] $samples
    [string] $bgColour
    [int] $vignette

    [string] $logFileLocation

    [array]GenerateProcessInformation(){
        $argumentArray = ('-b', '--factory-startup', '-o', $this.renderLocation, '-P', $this.scriptLocation, '-F', $this.renderFormat, '-f', '1', '--', '-file', $this.file, '-camType', $this.camType, '-renderSize', $this.renderSize, '-pixBorder', $this.pixBorder, '-camRot', $this.camRot, '-samples', $this.samples, '-bgColour', $this.bgColour, '-vignette', $this.vignette)
        return $argumentArray
    }
}

#convert settings from json file
$settings = [ProcessSettings](Get-Content "$(Get-Location)/processSettings.json" | Out-String | ConvertFrom-Json)



Set-Location 'G:\BlenderProjects\blender-icon-generator\PowerShell'

$startTime = Get-Date -Format g

$stdLog = "G:\BlenderProjects\blender-icon-generator\PowerShell\Log\outputStd.log"
$errorLog = "G:\BlenderProjects\blender-icon-generator\PowerShell\Log\outputError.log"

Start-Process -FilePath "C:\\Program Files\\Blender Foundation\\Blender\\blender.exe" -ArgumentList $settings.GenerateProcessInformation() -RedirectStandardOutput $stdLog -RedirectStandardError $errorLog -Wait

$endTime = Get-Date -Format g

$newHeader = [string]::Format("`r`nNew Process - Started: {0} - Finished: {1}", $startTime, $endTime)

$newHeader | Out-File $settings.logFileLocation -Append

Get-Content $errorLog, $stdLog | Out-File $settings.logFileLocation -Append

Write-Host "Process Complete"

#Read-Host -Prompt "Press Enter to continue"