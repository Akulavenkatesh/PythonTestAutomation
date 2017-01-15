import subprocess
import time


striOSAppiumConnectionString = "/Applications/Appium.app/Contents/Resources/node/bin/node \
                                                /Applications/Appium.app/Contents/Resources/node_modules/appium/bin/appium.js \
                                                --address 127.0.0.1 --command-timeout \"7200\" --debug-log-spacing \
                                                --no-reset \
                                                 --native-instruments-lib --log-level \"error\""
                                                 
                                    
                                    
subprocess.call('killall node', shell=True)               
subprocess.Popen(striOSAppiumConnectionString, shell=True)
time.sleep(5)