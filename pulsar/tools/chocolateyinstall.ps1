
$ErrorActionPreference = 'Stop'
$toolsDir   = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"
$fileLocation = Join-Path $toolsDir 'Windows.Pulsar.Setup.1.104.0.exe'

$packageArgs = @{
  packageName    = $env:ChocolateyPackageName
  unzipLocation  = $toolsDir
  fileType       = 'exe'
  file           = $fileLocation
  softwareName   = 'Pulsar'
  checksum       = '253449889bdeb5c6b48ed7deb8e6b4e853da1624b06fe2a53c0663e508392ab7'
  checksumType   = 'sha256'
  silentArgs     = '/S'
  validExitCodes = @(0)
}

Install-ChocolateyInstallPackage @packageArgs
