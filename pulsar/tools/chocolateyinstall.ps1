$ErrorActionPreference = 'Stop'
$url = 'https://github.com/pulsar-edit/pulsar/releases/download/v1.114.0/Windows.Pulsar.Setup.1.114.0.exe'

$packageArgs = @{
  packageName    = $env:ChocolateyPackageName
  unzipLocation  = $toolsDir
  fileType       = 'exe'
  url            = $url
  softwareName   = 'Pulsar'
  checksum       = '65f447565aa13a35fb39a0f4bc6d27c0e189fe8d76c89b4a0f8e50f82bd4925a'
  checksumType   = 'sha256'
  silentArgs     = '/S'
  validExitCodes = @(0)
}

Install-ChocolateyPackage @packageArgs
