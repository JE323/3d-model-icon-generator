param (
    [string]$file = "",
    [string]$output = ""
)

#Write-Host ("File specified: " + $file)
#Write-Host ("Output specified: " + $output)

class ProcessSettings {
    #parsed variables from json file
    [string] $blenderLocation
    [string] $scriptLocation
    [string] $logLocation
    [string] $renderFile

    #processed variables
    [string]$isolatedFilename
    [string]$isolatedFilenameWithHashes
    [string]$isolatedFilenameNumbered
    [string]$fileExtension
    [string]$outputFilepath
    [string]$outputFilepathWithHashes
    [string]$outputFilepathNumbered

    [string]$stdLog
    [string]$errorLog
    [string]$finalLog

    [string]$modelLocation

    [string]$absoluteRenderFile

    [void]Init([string]$file, [string]$output){
        $this.modelLocation = Join-Path -Path (Get-Location) -ChildPath ($file) -Resolve
        $modelLeaf = Split-Path $this.modelLocation -Leaf
        $this.isolatedFilename = $modelLeaf.Split(".")[0]
        $this.fileExtension = $modelLeaf.Split(".")[1]
        $this.isolatedFilenameWithHashes = $this.isolatedFilename + "_##"
        $this.isolatedFilenameNumbered = $this.isolatedFilename + "_01"

        $outputBaseLocation = Join-Path -Path (Get-Location) -ChildPath $output -Resolve
        $this.outputFilepath = (Join-Path -Path $outputBaseLocation -ChildPath $this.isolatedFilename)
        $this.outputFilepathWithHashes = (Join-Path -Path $outputBaseLocation -ChildPath $this.isolatedFilenameWithHashes)
        $this.outputFilepathNumbered = (Join-Path -Path $outputBaseLocation -ChildPath $this.isolatedFilenameNumbered)

        $logBaseLocation = Join-Path -Path (Get-Location) -ChildPath $this.logLocation -Resolve
        $this.stdLog = Join-Path -Path $logBaseLocation -ChildPath "\outputStd.log" -Resolve
        $this.errorLog = Join-Path -Path $logBaseLocation -ChildPath "\outputError.log" -Resolve
        $this.finalLog = Join-Path -Path $logBaseLocation -ChildPath "\output.log" -Resolve

        $this.absoluteRenderFile = $this.GenerateAbsolutePath($this.renderFile)
    }

    [array]GenerateProcessInformation(){
        $argumentArray = ('-b', $this.absoluteRenderFile, '-o', $this.outputFilepathWithHashes, '-P', `
        $this.scriptLocation, '-F', "PNG", '-f', '1', '--', '-file', $this.modelLocation)

        return $argumentArray
    }

    [string]GenerateAbsolutePath([string] $filepath){
        #if its already absolute
        if ($filepath -like ":\\"){
            return $filepath
        }
        return (Join-Path -Path (Get-Location) -ChildPath $filepath)
    }
}

$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir  = Split-Path -Parent $ScriptPath
Set-Location $scriptDir

#convert settings from json file

$processSettings = [ProcessSettings](Get-Content "$($scriptDir)\processSettings.json" | Out-String | ConvertFrom-Json)
$processSettings.Init($file, $output)
$startTime = Get-Date -Format g

Try
{
    Start-Process -FilePath $processSettings.blenderLocation -ArgumentList $processSettings.GenerateProcessInformation() `
-RedirectStandardOutput $processSettings.stdLog -RedirectStandardError $processSettings.errorLog -Wait
}
Catch
{
    Write-Host ("Error was thrown!")
    Write-Error $_.ScriptStackTrace
}
Finally
{
    $endTime = Get-Date -Format g
    $newHeader = [string]::Format("`r`nNew Process - Started: {0} - Finished: {1}", $startTime, $endTime)
    $newHeader | Out-File $processSettings.finalLog -Append
}

Get-Content $processSettings.errorLog, $processSettings.stdLog | Out-File $processSettings.finalLog -Append

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
