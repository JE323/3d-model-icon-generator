param (
    [Parameter(Mandatory, 
    ValueFromPipelineByPropertyName,
    HelpMessage = "Enter the model file to have an icon generated of.")]
    [Alias("Model")]
    [ValidateNotNullOrEmpty()]
    [string]$file,

    [Parameter(HelpMessage = "Enter the directory to be used for the output icon location. If not specified the same loation as the provide model will be used.")]
    [Alias("Folder", "Directory")]
    [ValidateNotNullOrEmpty()]
    [string]$output
)

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

    [array]$processInformation

    FileProcessing([Settings]$settings, [string]$file, [string]$output){
        $this.modelLocation = $this.GenerateAbsolutePath($file)
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
        
        if ($output){
            $outputBaseLocation = $this.GenerateAbsolutePath($output)
        } else {
            $outputBaseLocation = Split-Path $this.modelLocation -Parent
        }
        $this.outputFilepath = (Join-Path -Path $outputBaseLocation -ChildPath $this.isolatedFilename)
        $this.outputFilepathWithHashes = (Join-Path -Path $outputBaseLocation -ChildPath $this.isolatedFilenameWithHashes)
        $this.outputFilepathNumbered = (Join-Path -Path $outputBaseLocation -ChildPath $this.isolatedFilenameNumbered)

        $logBaseLocation = $this.GenerateAbsolutePath($settings.logLocation)
        if(!(Test-Path -Path $logBaseLocation )){
            New-Item -Path $logBaseLocation -ItemType Directory 
        }
        $this.stdLog = $this.GeneratePathJoin($logBaseLocation, "\outputStd.log")
        $this.errorLog = $this.GeneratePathJoin($logBaseLocation, "\outputError.log")
        $this.finalLog = $this.GeneratePathJoin($logBaseLocation, "\output.log")

        $this.absoluteRenderFile = $this.GenerateAbsolutePath($settings.renderFile)
        if (-not (Test-Path $this.absoluteRenderFile)){
            throw "ERROR: Render file is not found!"
        }

        $this.processInformation = ('-b', $this.absoluteRenderFile, '-o', $this.outputFilepathWithHashes, '-P', `
        $this.GenerateAbsolutePath($settings.scriptLocation), '-F', "PNG", '-f', '1', '--', '-file', $this.modelLocation)

        Write-Host "File Processing Validated!"
    }

    [string]GenerateAbsolutePath([string] $filepath){
        #if its already absolute
        if ($filepath -like "*:\*"){
            return $filepath
        }
        
        $FileName = Join-Path -Path (Get-Location) -ChildPath $filepath -Resolve -ErrorAction SilentlyContinue -ErrorVariable error

        if ($FileName) {
            Write-Host("File: " + $FileName)
            return $FileName
        }
        
        Write-Host("Invalid file: " + $error[0].TargetObject)
        return $error[0].TargetObject
    }

    [string]GeneratePathJoin([string] $base, [string] $leaf){
        $FileName = Join-Path -Path $base -ChildPath $leaf -Resolve -ErrorAction SilentlyContinue -ErrorVariable error
        if ($FileName) {
            return $FileName
        }
        return $error[0].TargetObject
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

#start the render process 
$startTime = Get-Date -Format g
Try
{
    Start-Process -FilePath $settings.blenderLocation -ArgumentList $fileProcessing.processInformation `
-RedirectStandardOutput $fileProcessing.stdLog -RedirectStandardError $fileProcessing.errorLog -Wait
}
Catch
{
    throw $_.ScriptStackTrace
}
Finally
{
    $endTime = Get-Date -Format g
    $newHeader = [string]::Format("`r`nNew Process - Started: {0} - Finished: {1}", $startTime, $endTime)
    $newHeader | Out-File $fileProcessing.finalLog -Append
    Get-Content $fileProcessing.errorLog, $fileProcessing.stdLog | Out-File $fileProcessing.finalLog -Append
}

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
