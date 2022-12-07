#!/bin/bash

help()
{
   # Display Help
   echo "Usage: sisyphus [OPTIONS]"
   echo "For iOS: sisyphus [-t|d|v|a|x|u|s|c]"
   echo "For Android: sisyphus [-t|d|v|a|i|s|c]"
   echo
   echo "options:"
   echo "t     Connetion types: webc/android/ios."
   echo "h     Print this Help."
   echo "d     Device name, for android would be ip:port, for ios would be device name in ipone setting."
   echo "v     OS version of android/ios."
   echo "a     App package name in android, or app bundle id in ios."
   echo "x     For ios only, should be xcode organization identifier."
   echo "u     For ios only, udid of iphone"
   echo "i     For Android only, the app init activity"
   echo "s     Appium server ip"
   echo "c     Tase case name"
}

if [[ $# -eq 0 ]] ; then
  help
  exit 0
fi

while getopts ":ht:d:v:a:x:u:s:c:i:" opt; do
  case $opt in
    t) type=("$OPTARG");;
    d) device=("$OPTARG");;
    v) version=("$OPTARG");;
    a) app=("$OPTARG");;
    x) xcode_org_id=("$OPTARG");;
    u) udid=("$OPTARG");;
    s) server_ip=("$OPTARG");;
    c) case=("$OPTARG");;
    i) init=("$OPTARG");;
    h) help
       exit;;
    *) echo 'invalid argumants' ;;
  esac
done
shift $((OPTIND -1))

if [ "$type" = "ios" ]
then
cat << EOF > ~/sisyphus/yamls/ios.yaml
appiumServer:
  'http://$server_ip:4723/wd/hub'
deviceName:
  '$device'
platformVersion:
  '$version'
platformName:
  'iOS'
bundleId:
  '$app'
automationName:
  'XCUITest'
xcodeOrgId:
  '$xcode_org_id'
xcodeSigningId:
  'iPhone Developer'
udid:
  '$udid'
webviewConnectTimeout:
  '90000'
reportURL:
  'http://$server_ip:8080/'
pathFile:
  'ios_testcase/$case.yaml'
EOF

python3 ~/sisyphus/boulder/shove.py -t $type
fi

if [ "$type" = "android" ]
then
cat << EOF > ~/sisyphus/yamls/android.yaml
appiumServer:
  'http://$server_ip:4723/wd/hub'
deviceName:
  '$device'
platformVersion:
  '$version'
platformName:
  'Android'
appPackage:
  '$app'
appActivity:
  '$init'
autoGrantPermissions: True
chromedriverExecutable:
  '/root/sisyphus/chromedriver'
reportURL:
  'http://$server_ip:8080/'
pathFile:
  'android_testcase/$case.yaml'
EOF

python3 ~/sisyphus/boulder/shove.py -t $type
fi

