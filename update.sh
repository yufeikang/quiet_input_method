#!/bin/bash

git pull origin master

DIR=${DIR:-~/.quiet_input_method}
sed -e "s/SRC_DIR/${DIR//\//\\/}/g" $DIR/launch.plist >~/Library/LaunchAgents/quiet_input_method.plist

launchctl unload ~/Library/LaunchAgents/quiet_input_method.plist
launchctl load ~/Library/LaunchAgents/quiet_input_method.plist
