$ErrorActionPreference = 'Stop'
$url = 'https://github.com/pulsar-edit/pulsar/releases/download/v1.129.0/Windows.Pulsar.Setup.1.129.0.exe'

$packageArgs = @{
  packageName    = $env:ChocolateyPackageName
  unzipLocation  = $toolsDir
  fileType       = 'exe'
  url            = $url
  softwareName   = 'Pulsar'
  checksum       = '16d00fa5a3375f3e715a80d177f3f4c997ce5a4cef3ab05f5c248b7c343ca4b0'
  checksumType   = 'sha256'
  silentArgs     = '/S'
  validExitCodes = @(0)
}

Install-ChocolateyPackage @packageArgs
