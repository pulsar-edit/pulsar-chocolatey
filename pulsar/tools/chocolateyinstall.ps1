$ErrorActionPreference = 'Stop'
$url = 'https://github.com/pulsar-edit/pulsar/releases/download/v1.113.0/Windows.Pulsar.Setup.1.113.0.exe'

$packageArgs = @{
  packageName    = $env:ChocolateyPackageName
  unzipLocation  = $toolsDir
  fileType       = 'exe'
  url            = $url
  softwareName   = 'Pulsar'
  checksum       = '74fe5fad563b6eaec53668431db2dfa854021c4b0126c311363bcda6d47adf4f'
  checksumType   = 'sha256'
  silentArgs     = '/S'
  validExitCodes = @(0)
}

Install-ChocolateyPackage @packageArgs
