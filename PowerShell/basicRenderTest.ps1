class ProcessSettings {
    #parsed variables from json file
    [string] $blenderLocation
    [string] $scriptLocation

    [string] $fileLocation
    [string] $filename
    [string] $renderLocation

    [string] $camType
    [string] $renderSize
    [int] $pixBorder
    [string] $camRot
    [int] $samples
    [string] $bgColour
    [int] $vignette

    [string] $logFileLocation

    #processed variables
    [string]$isolatedFilename
    [string]$isolatedFilenameWithHashes
    [string]$isolatedFilenameNumbered

    [string]$outputFilepath
    [string]$outputFilepathWithHashes
    [string]$outputFilepathNumbered

    [void]Init(){
        $this.isolatedFilename = $this.filename.Split(".")[0]
        $this.isolatedFilenameWithHashes = $this.isolatedFilename + "_##"
        $this.isolatedFilenameNumbered = $this.isolatedFilename + "_01"

        $this.outputFilepath = (Join-Path -Path $this.renderLocation -ChildPath $this.isolatedFilename)
        $this.outputFilepathWithHashes = (Join-Path -Path $this.renderLocation -ChildPath $this.isolatedFilenameWithHashes)
        $this.outputFilepathNumbered = (Join-Path -Path $this.renderLocation -ChildPath $this.isolatedFilenameNumbered)
    }

    [array]GenerateProcessInformation(){
        $argumentArray = ('-b', '--factory-startup', '-o', $this.outputFilepathWithHashes, '-P', $this.scriptLocation, '-F', "PNG", '-f', '1', '--', '-file', (Join-Path -Path $this.fileLocation -ChildPath $this.filename), '-camType', $this.camType, '-renderSize', $this.renderSize, '-pixBorder', $this.pixBorder, '-camRot', $this.camRot, '-samples', $this.samples, '-bgColour', $this.bgColour, '-vignette', $this.vignette)
        return $argumentArray
    }
}

Set-Location 'G:\BlenderProjects\blender-icon-generator\PowerShell'

#convert settings from json file
$settings = [ProcessSettings](Get-Content "$(Get-Location)\processSettings.json" | Out-String | ConvertFrom-Json)
$settings.Init()

$startTime = Get-Date -Format g

$stdLog = "G:\BlenderProjects\blender-icon-generator\PowerShell\outputStd.log"
$errorLog = "G:\BlenderProjects\blender-icon-generator\PowerShell\outputError.log"

Start-Process -FilePath "C:\\Program Files\\Blender Foundation\\Blender\\blender.exe" -ArgumentList $settings.GenerateProcessInformation() -RedirectStandardOutput $stdLog -RedirectStandardError $errorLog -Wait

$endTime = Get-Date -Format g

$newHeader = [string]::Format("`r`nNew Process - Started: {0} - Finished: {1}", $startTime, $endTime)

$newHeader | Out-File $settings.logFileLocation -Append

Get-Content $errorLog, $stdLog | Out-File $settings.logFileLocation -Append

#$newfilepathName = Join-Path -Path $settings.renderLocation -ChildPath ([string]::Join(".", ($newFileName, $settings.GetFileType())))

#Write-Host ("Isolated Filename: {0} `nWith hashes: {1} `nWith numbers: {2}`nFull Path: {3}`n" -f $settings.isolatedFilename, $settings.isolatedFilenameWithHashes, $settings.isolatedFilenameNumbered, $settings.outputFilepathNumbered)
Try
{
    Remove-Item ($settings.outputFilepath + ".png") -ErrorAction Stop
    Write-Warning ("File already found - output was overwritten")
}
Catch
{
    Write-Host ("No file found - new render was created.")
}
Rename-Item -Path ($settings.outputFilepathNumbered + ".png") -NewName ($settings.isolatedFilename + ".png")

Write-Host "Process Complete"

#Read-Host -Prompt "Press Enter to continue"