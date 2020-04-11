class ProcessSettings {
    #parsed variables from json file
    [string] $blenderLocation
    [string] $scriptLocation

    [string] $fileLocation
    [string] $filename
    [string] $renderLocation

    [string] $logFilesLocation

    [string] $renderFile

    #processed variables
    [string]$isolatedFilename
    [string]$isolatedFilenameWithHashes
    [string]$isolatedFilenameNumbered
    [string]$outputFilepath
    [string]$outputFilepathWithHashes
    [string]$outputFilepathNumbered

    [string]$absoluteScriptLocation

    [string]$absoluteLogsLocation
    [string]$stdLog
    [string]$errorLog
    [string]$finalLog

    [string]$absoluteRenderFile

    [void]Init([string] $relToAbs){
        $this.isolatedFilename = $this.filename.Split(".")[0]
        $this.isolatedFilenameWithHashes = $this.isolatedFilename + "_##"
        $this.isolatedFilenameNumbered = $this.isolatedFilename + "_01"

        $this.outputFilepath = (Join-Path -Path $this.renderLocation -ChildPath $this.isolatedFilename)
        $this.outputFilepathWithHashes = (Join-Path -Path $this.renderLocation -ChildPath $this.isolatedFilenameWithHashes)
        $this.outputFilepathNumbered = (Join-Path -Path $this.renderLocation -ChildPath $this.isolatedFilenameNumbered)
        
        $this.absoluteScriptLocation = $this.GenerateAbsolutePath($this.scriptLocation, $relToAbs)
        $this.absoluteLogsLocation = $this.GenerateAbsolutePath($this.logFilesLocation, $relToAbs)

        $this.stdLog = "$($this.absoluteLogsLocation)\outputStd.log"
        $this.errorLog = "$($this.absoluteLogsLocation)\outputError.log"
        $this.finalLog = "$($this.absoluteLogsLocation)\output.log"

        $this.absoluteRenderFile = $this.GenerateAbsolutePath($this.renderFile, $relToAbs)
    }

    [array]GenerateProcessInformation(){
        $argumentArray = ('-b', $this.absoluteRenderFile, '-o', $this.outputFilepathWithHashes, '-P', `
        $this.absoluteScriptLocation, '-F', "PNG", '-f', '1', '--', '-file', (Join-Path -Path $this.fileLocation -ChildPath $this.filename))

        return $argumentArray
    }

    [string]GenerateAbsolutePath([string] $filepath, [string] $relToAbs){
        if ($filepath.StartsWith("\")){
            return (Join-Path -Path ($relToAbs) -ChildPath $filepath)
        }
        return $filepath
    }
}

$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir  = Split-Path -Parent $ScriptPath
Set-Location $scriptDir

#convert settings from json file
$processSettings = [ProcessSettings](Get-Content "$($scriptDir)\processSettings.json" | Out-String | ConvertFrom-Json)
$processSettings.Init($scriptDir)

$startTime = Get-Date -Format g

Write-Host $processSettings.GenerateProcessInformation()

Start-Process -FilePath $processSettings.blenderLocation -ArgumentList $processSettings.GenerateProcessInformation() `
-RedirectStandardOutput $processSettings.stdLog -RedirectStandardError $processSettings.errorLog -Wait

$endTime = Get-Date -Format g

$newHeader = [string]::Format("`r`nNew Process - Started: {0} - Finished: {1}", $startTime, $endTime)
$newHeader | Out-File $processSettings.finalLog -Append

Get-Content $processSettings.errorLog, $processSettings.stdLog | Out-File $processSettings.finalLog -Append

#Write-Host ("Isolated Filename: {0} `nWith hashes: {1} `nWith numbers: {2}`nFull Path: {3}`n" `
#-f $processSettings.isolatedFilename, $processSettings.isolatedFilenameWithHashes, `
#$processSettings.isolatedFilenameNumbered, $processSettings.outputFilepathNumbered)
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
