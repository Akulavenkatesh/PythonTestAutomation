#!/bin/sh

# Fail fast, exit on first error
set -e

#######################
# KEYCHAIN ACCESS
#######################
echo "Enable Keychain access"
security list-keychains
security unlock-keychain -p admin /users/ranganathan.veluswamy/Library/Keychains/login.keychain

#######################
# ENVIRONMENT VARIABLES
#######################
BUILD_NUMBER=${BUILD_NUMBER:="000"}
BUILD_INFIX='Hive.InternalProd.AutomatedTesting'

PLIST_FILE='Hive/Hive-Info.plist'
IPA_FILE='build/Hive.ipa'

RELEASE_NOTES='Please note this app is currently in development and not all of the functionality and features are live. We are continuing to update periodically, so keep downloading the latest version onto your smartphone.'

echo "====================="
echo "Environment Variables"
echo "====================="
printenv

###########################################################
# PLIST CONFIGURATION
###########################################################
echo "====================="
echo "Plist Tweaks"
echo "====================="

cd -- "$(dirname "$0")"
cd /Users/admin/Documents/IOS/myHomeIOS/


iosbuild plist:buildnumber              --file "$PLIST_FILE" \
                                        --infix $BUILD_INFIX \
                                        --buildnumber $BUILD_NUMBER

iosbuild plist:configure                --file "$PLIST_FILE" \
                                        CFBundleDisplayName='Hive Auto' \
                                        RHCServerURL='http://api.internalprod.zoo.alertme.com:8080/api' \
                                        HVServerURL='https://api.internalprod.zoo.alertme.com'


###########################################################
# BUILD
###########################################################
echo "====================="
echo "Build"
echo "====================="
ipa build                               --workspace Hive.xcworkspace \
                                        --scheme Hive \
                                        --configuration Debug \
                                        --destination build \
                                        --verbose

ideviceinstaller -i /Users/admin/Documents/IOS/myHomeIOS/Build/Hive.ipa

cp /Users/admin/Documents/IOS/myHomeIOS/Build/Hive.ipa /Users/admin/Documents/workspace/HiveTestAutomation/02_Manager_Tier/EnviromentFile/Apps/iOS/isopInternProd/

cd -- "$(dirname "$0")"
cd /Users/admin/Documents/workspace/HiveTestAutomation/01_BDD_Tier/features
python appium_server.py
behave --tags=BasicSmokeTest