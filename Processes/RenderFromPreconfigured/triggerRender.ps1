param (
    [string]$file = "",
    [string]$output = ""
)

#Write-Host ("File specified: " + $file)
#Write-Host ("Output specified: " + $output)

class Settings {
    #parsed variables from json file
    [string] $blenderLocation
    [string] $scriptLocation
    [string] $logLocation
    [string] $renderFile

    [void] Validate(){
        if (-not (Test-Path $this.blenderLocation)){
            throw "ERROR: Blender Location is invalid!"
        }
        if (-not ($this.scriptLocation)){
            throw "ERROR: Script location is either not specified or invalid!"
        }
        if (-not ($this.logLocation)){
            throw "ERROR: Log location is either not specified or invalid!"
        }
        if (-not ($this.renderFile)){
            throw "ERROR: Render file is either not specified or invalid!"
        }
    }
}

class FileProcessing {
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

    [array]$generateProcessInformation

    FileProcessing([Settings]$settings, [string]$file, [string]$output){
        $this.modelLocation = Join-Path -Path (Get-Location) -ChildPath ($file) -Resolve
        if (-not (Test-Path $this.modelLocation)){
            throw "ERROR: Model location is not found!"
        }

        if (-not (Test-Path $this.GenerateAbsolutePath($settings.scriptLocation))){
            throw "ERROR: Script file is not found!"
        }

        $modelLeaf = Split-Path $this.modelLocation -Leaf
        $this.isolatedFilename = $modelLeaf.Split(".")[0]
        $this.fileExtension = $modelLeaf.Split(".")[1]
        $this.isolatedFilenameWithHashes = $this.isolatedFilename + "_##"
        $this.isolatedFilenameNumbered = $this.isolatedFilename + "_01"

        $outputBaseLocation = Join-Path -Path (Get-Location) -ChildPath $output -Resolve
        $this.outputFilepath = (Join-Path -Path $outputBaseLocation -ChildPath $this.isolatedFilename)
        $this.outputFilepathWithHashes = (Join-Path -Path $outputBaseLocation -ChildPath $this.isolatedFilenameWithHashes)
        $this.outputFilepathNumbered = (Join-Path -Path $outputBaseLocation -ChildPath $this.isolatedFilenameNumbered)

        $logBaseLocation = Join-Path -Path (Get-Location) -ChildPath $settings.logLocation -Resolve
        $this.stdLog = Join-Path -Path $logBaseLocation -ChildPath "\outputStd.log" -Resolve
        $this.errorLog = Join-Path -Path $logBaseLocation -ChildPath "\outputError.log" -Resolve
        $this.finalLog = Join-Path -Path $logBaseLocation -ChildPath "\output.log" -Resolve

        $this.absoluteRenderFile = $this.GenerateAbsolutePath($settings.renderFile)
        if (-not (Test-Path $this.absoluteRenderFile)){
            throw "ERROR: Render file is not found!"
        }

        $this.generateProcessInformation = ('-b', $this.absoluteRenderFile, '-o', $this.outputFilepathWithHashes, '-P', `
        $settings.scriptLocation, '-F', "PNG", '-f', '1', '--', '-file', $this.modelLocation)

        Write-Host "File Processing Validated!"
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
$settings = [Settings](Get-Content "$($scriptDir)\processSettings.json" | Out-String | ConvertFrom-Json)
$settings.Validate()    

#generate all the new file processing locations
$fileProcessing = [fileProcessing]::New($settings, $file, $output)
exit

#start the render process 
$startTime = Get-Date -Format g
Try
{
    Start-Process -FilePath $fileProcessing.blenderLocation -ArgumentList $fileProcessing.generateProcessInformation `
-RedirectStandardOutput $fileProcessing.stdLog -RedirectStandardError $fileProcessing.errorLog -Wait
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
    $newHeader | Out-File $fileProcessing.finalLog -Append
}

Get-Content $fileProcessing.errorLog, $fileProcessing.stdLog | Out-File $fileProcessing.finalLog -Append

Try
{
    Remove-Item ($fileProcessing.outputFilepath + ".png") -ErrorAction Stop
    Write-Warning ("File already found - output was overwritten")
}
Catch
{
    Write-Host ("No file found - new render was created.")
}
Rename-Item -Path ($fileProcessing.outputFilepathNumbered + ".png") -NewName ($fileProcessing.isolatedFilename + ".png")

Write-Host "Process Complete"
