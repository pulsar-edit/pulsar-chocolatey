import re
import sys
import os
import argparse
import codecs
import shutil
import requests
import hashlib

# Class defining methods to edit package's source files given desired Pulsar version
class PackageFilesEditor():
	# Constants
	PACKAGE_SOURCES_PATH = "./pulsar/"
	NUSPEC_FILE = PACKAGE_SOURCES_PATH + "pulsar.nuspec"
	INSTALL_SCRIPT_PATH = PACKAGE_SOURCES_PATH + "tools/chocolateyinstall.ps1"
	INSTALLER_PATH = PACKAGE_SOURCES_PATH + "tools/"
	VERIFICATION_FILE_PATH = INSTALLER_PATH + "VERIFICATION.txt"
	
	# Class properties
	pulsarVersion_ = 0
	installerUrl_ = "https://github.com/pulsar-edit/pulsar/releases/download/"
	installerFileName_ = ""
	installerChecksum_ = ""
	
	# Class initializer
	def __init__(self, pulsarVersion):
		self.pulsarVersion_ = pulsarVersion
		self.installerFileName_ = "Windows.Pulsar.Setup." + pulsarVersion + ".exe"
		self.installerUrl_ = self.installerUrl_ + "v" + pulsarVersion + "/" + self.installerFileName_
	
	# Main function run from main
	def run(self):
		print("Init configuration files to generate package for version " + self.pulsarVersion_)
		
		self.downloadInstaller()
		
		self.editNuspecPackage()
		self.editInstallScript()
		self.generateVerificationFile()
		
		print("Package sources initialized")
		
	
	def downloadInstaller(self):
		print("Download installer for version " + self.pulsarVersion_ + "...")
		
		response = requests.get(self.installerUrl_)
		if(response.status_code != 200):
			print("Error " + str(response.status_code) + " while downloading install file")
			sys.exit(1)
		
		open(self.INSTALLER_PATH + self.installerFileName_, "wb").write(response.content)
		
		print("DONE")
		
		print("Compute SHA256 checksum...")
		
		with open(self.INSTALLER_PATH + self.installerFileName_, "rb") as f:
			bytes = f.read() # read entire file as bytes
			self.installerChecksum_ = hashlib.sha256(bytes).hexdigest();
			
		print("DONE")
	
	def editNuspecPackage(self):
		print("Edit " + self.NUSPEC_FILE + "file...")
		nuspecFileOriginal = codecs.open(self.NUSPEC_FILE, "r", "utf-8")
		nuspecFileNew = codecs.open("tmp", "w", "utf-8")
		for line in nuspecFileOriginal:
			if "<version>" in line:
				nuspecFileNew.write("    <version>" + self.pulsarVersion_ + "</version>" + os.linesep)
			else:
				nuspecFileNew.write(line)
		nuspecFileOriginal.close()
		nuspecFileNew.close()
		
		shutil.copy2("tmp", self.NUSPEC_FILE)
		os.remove("tmp")
		
		print("DONE")
		
	def editInstallScript(self):
		print("Edit " + self.INSTALL_SCRIPT_PATH + "file...")
		installScriptOriginal = codecs.open(self.INSTALL_SCRIPT_PATH, "r", "utf-8")
		installScriptNew = codecs.open("tmp", "w", "utf-8")
		for line in installScriptOriginal:
			if ".exe" in line:
				installScriptNew.write("$fileLocation = Join-Path $toolsDir '" + self.installerFileName_ + "'" + os.linesep)
			elif "checksum" in line and not "Type" in line:
				installScriptNew.write("  checksum       = '" + self.installerChecksum_ + "'" + os.linesep)
			else:
				installScriptNew.write(line)
		installScriptOriginal.close()
		installScriptNew.close()
		
		shutil.copy2("tmp", self.INSTALL_SCRIPT_PATH)
		os.remove("tmp")
		
		print("DONE")
		
	def generateVerificationFile(self):
		print("Generate verification file...");
		verificationFile = codecs.open(self.VERIFICATION_FILE_PATH, "w", "utf-8")
		
		verificationFile.write("VERIFICATION" + os.linesep)
		verificationFile.write(os.linesep)
		verificationFile.write("Installer file: " + self.installerFileName_ + os.linesep)
		verificationFile.write("Checksum: " + self.installerChecksum_ + os.linesep)
		verificationFile.write("Checksum type: SHA256" + os.linesep)
		verificationFile.write("Original installer and checksums can be found at: https://github.com/pulsar-edit/pulsar/releases/tag/v" + self.pulsarVersion_ + os.linesep)
		
		verificationFile.close()
		
		print("DONE")
	
# Main function
if __name__ == '__main__':
	# Command line arguments parsing
	parser = argparse.ArgumentParser(description="Init Chocolatey Pulsar package configuration files", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("version", help="Pulsar version")
	args = parser.parse_args()
	
	# Run files edit
	packageFilesEditor = PackageFilesEditor(args.version)
	packageFilesEditor.run()
	
	print("Navigate to pulsar folder and generate package with 'choco pack' command")
		