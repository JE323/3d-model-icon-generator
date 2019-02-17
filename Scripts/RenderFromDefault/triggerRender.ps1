class ProcessSettings {
    #parsed variables from json file
    [string] $blenderLocation
    [string] $scriptLocation

    [string] $fileLocation
    [string] $filename
    [string] $renderLocation
    [string] $renderSettings

    [string] $logFileLocation

    #processed variables
    [string]$isolatedFilename
    [string]$isolatedFilenameWithHashes
    [string]$isolatedFilenameNumbered

    [string]$outputFilepath
    [string]$outputFilepathWithHashes
    [string]$outputFilepathNumbered

    [string]$absoluteRenderSettings

    [void]Init(){
        $this.isolatedFilename = $this.filename.Split(".")[0]
        $this.isolatedFilenameWithHashes = $this.isolatedFilename + "_##"
        $this.isolatedFilenameNumbered = $this.isolatedFilename + "_01"

        $this.outputFilepath = (Join-Path -Path $this.renderLocation -ChildPath $this.isolatedFilename)
        $this.outputFilepathWithHashes = (Join-Path -Path $this.renderLocation -ChildPath $this.isolatedFilenameWithHashes)
        $this.outputFilepathNumbered = (Join-Path -Path $this.renderLocation -ChildPath $this.isolatedFilenameNumbered)
      
        $this.absoluteRenderSettings = (Join-Path -Path (Get-Location) -ChildPath $this.renderSettings)
    }

    [array]GenerateProcessInformation(){
        $argumentArray = ('-b', '--factory-startup', '-o', $this.outputFilepathWithHashes, '-P', $this.scriptLocation, '-F', "PNG", '-f', '1', '--', '-file', (Join-Path -Path $this.fileLocation -ChildPath $this.filename), '-settings', $this.absoluteRenderSettings)
        return $argumentArray
    }
}

Set-Location 'G:\BlenderProjects\ModelThumbnailGenerator\blender-icon-generator\Scripts\RenderFromDefault'

#convert settings from json file
$processSettings = [ProcessSettings](Get-Content "$(Get-Location)\processSettings.json" | Out-String | ConvertFrom-Json)
$processSettings.Init()

$startTime = Get-Date -Format g

$stdLog = "G:\\BlenderProjects\\ModelThumbnailGenerator\\blender-icon-generator\\Scripts\\RenderFromDefault\\Logs\\outputStd.log"
$errorLog = "G:\\BlenderProjects\\ModelThumbnailGenerator\\blender-icon-generator\\Scripts\\RenderFromDefault\\Logs\\outputError.log"

Start-Process -FilePath "C:\\Program Files\\Blender Foundation\\Blender\\blender.exe" -ArgumentList $processSettings.GenerateProcessInformation() -RedirectStandardOutput $stdLog -RedirectStandardError $errorLog -Wait

$endTime = Get-Date -Format g

$newHeader = [string]::Format("`r`nNew Process - Started: {0} - Finished: {1}", $startTime, $endTime)

$newHeader | Out-File $processSettings.logFileLocation -Append

Get-Content $errorLog, $stdLog | Out-File $processSettings.logFileLocation -Append

#$newfilepathName = Join-Path -Path $processSettings.renderLocation -ChildPath ([string]::Join(".", ($newFileName, $processSettings.GetFileType())))

#Write-Host ("Isolated Filename: {0} `nWith hashes: {1} `nWith numbers: {2}`nFull Path: {3}`n" -f $processSettings.isolatedFilename, $processSettings.isolatedFilenameWithHashes, $processSettings.isolatedFilenameNumbered, $processSettings.outputFilepathNumbered)
Try
{
    Remove-Item ($processSettings.outputFilepath + ".png") -ErrorAction Stop
    Write-Warning ("File already found - output was overwritten")
}
Catch
{
    Write-Host ("No file found - new render was created.")
}
Rename-Item -Path ($processSettings.outputFilepathNumbered + ".png") -NewName ($processSettings.isolatedFilename + ".png")

Write-Host "Process Complete"

#Read-Host -Prompt "Press Enter to continue"