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

}


Write-Host $(Get-Location)