$ErrorActionPreference = 'Stop'
$url = 'https://github.com/pulsar-edit/pulsar/releases/download/v1.115.0/Windows.Pulsar.Setup.1.115.0.exe'

$packageArgs = @{
  packageName    = $env:ChocolateyPackageName
  unzipLocation  = $toolsDir
  fileType       = 'exe'
  url            = $url
  softwareName   = 'Pulsar'
  checksum       = '2c069d113496e0077dd375034beef758fdd8fb609a0c9de60e7474ec3631b6ef'
  checksumType   = 'sha256'
  silentArgs     = '/S'
  validExitCodes = @(0)
}

Install-ChocolateyPackage @packageArgs
