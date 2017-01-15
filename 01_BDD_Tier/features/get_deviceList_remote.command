#!/usr/bin/expect

ssh ranganathan.veluswamy@10.19.0.146 "ls"
match_max 100000
expect "*?assword:*"
send "password-1\r"
send -- "\r"
expect eof
#send pwd
#send "/Users/ranganathan.veluswamy/Desktop/Ranga/RnD/Appium/android-sdk-macosx/platform-tools/adb devices"