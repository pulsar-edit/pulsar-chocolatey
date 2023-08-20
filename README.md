# pulsar-chocolatey

Pulsar editor Chocolatey package's source files.

## Content

The package contains:

- init.py: a python script to automatically initialize/update some package's files given the desired Pulsar editor version
- pulsar: the main package sources' folder


## Prerequisites

### Chocolatey package manager

Chocolatey is needed to generate and test the package locally. To install it (if not already installed), start Windows PowerShell as administrator and run the command

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### Python

The initialization script is written in Python. Python3 for Windows is needed to run it. If not already installed, download latest release from [Python website](https://www.python.org/downloads/windows/) and install it.

Once installed, add `requests` module using PIP

```
pip install requests
````

## Usage

### Automated Releases

This PR is intended to allow publishing a new Chocolatey release of Pulsar, without ever opening a terminal.
By using the simple steps laid out below:

1. Create a new issue.
  * This issue should contain the exact version you want to publish as it's title. Nothing else. ex. `1.108.0`
  * This issue should receive the label `release` (Best practice to add it after creating the issue)
2. A new PR will be created labeled `[<NEW_VERSION>] Draft Release`
3. Let automatic tests finish on this PR. Reviewing the workflow summary page will show what version of Pulsar these changes install. Make sure this matches what version you've intended to publish.
4. If all tests pass, merge the automatic PR.
5. With the PR now merged to `main` go ahead and trigger the GitHub Action `auto_publish`. This Action should run and if successful will publish a new version of Pulsar to Chocolatey.

### Manual Releases

#### init.py

The script will download the Pulsar installer given the input version, and edit a couple of source files accordingly, namely:

- pulsar.nuspec: the main package reference file. init.py script will update the version number
- tools\chocolateyinstall.ps1: Chocolatey install script. init.py will update the installer .exe filename and checksum
- tools\VERIFICATION.txt: a file with some info used by package validators. init.py generates the file, declaring the setup file name and checksum, and adds the URL where the validator can find the original installer and checksum.

Example usage:

```
python init.py 1.103.0
```

One must input the last version available on the website, otherwise the script will fail (it won't be able to download the installer).

Once the script terminates, the package is ready to be generated.

#### Package generation

Once the sources are updated, navigate to `pulsar` folder and run:

```
choco pack
```

Chocolatey will generate the file `pulsar\pulsar.<version>.nupkg`.

Test the package locally. From the command line shell, navigate to the directory where the *.nupkg file is located, then type:

```
choco install pulsar --source .
```

Check that the commands executes without errors, and Pulsar gets installed on your system.

Try to uninstall it, too

```
choco uninstall pulsar
```

If everything is ok, request to publish it on Chocolatey website.

```
choco push pulsar.1.103.0.nupkg --source https://push.chocolatey.org/
```

---

## To do

- update package with 'latest' release; wait for a static URL to download installer; no more input parameter (version) needed
- parse version of 'latest' installer (from filename or from embedded data)
- have a static URL for latest version checksums, to check installer file after download
