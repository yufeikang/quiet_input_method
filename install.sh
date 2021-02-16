#!/bin/sh

set -e

# Default settings
DIR=${DIR:-~/.quiet_input_method}
REPO=${REPO:-Yufeikang/quiet_input_method}
REMOTE=${REMOTE:-https://github.com/${REPO}.git}
BRANCH=${BRANCH:-master}


command_exists() {
	command -v "$@" >/dev/null 2>&1
}

fmt_error() {
  echo ${RED}"Error: $@" >&2
}

fmt_underline() {
  echo "$(printf '\033[4m')$@$(printf '\033[24m')"
}

fmt_code() {
  echo "\`$(printf '\033[38;5;247m')$@\`"
}

setup_color() {
	# Only use colors if connected to a terminal
	if [ -t 1 ]; then
		RED=$(printf '\033[31m')
		GREEN=$(printf '\033[32m')
		YELLOW=$(printf '\033[33m')
		BLUE=$(printf '\033[34m')
		BOLD=$(printf '\033[1m')
		RESET=$(printf '\033[m')
	else
		RED=""
		GREEN=""
		YELLOW=""
		BLUE=""
		BOLD=""
		RESET=""
	fi
}

setup_src() {
  umask g-w,o-w

  echo "${BLUE}Cloning ..."

  command_exists git || {
    fmt_error "git is not installed"
    exit 1
  }

  git clone -c core.eol=lf -c core.autocrlf=false \
    -c fsck.zeroPaddedFilemode=ignore \
    -c fetch.fsck.zeroPaddedFilemode=ignore \
    -c receive.fsck.zeroPaddedFilemode=ignore \
    --depth=1 --branch "$BRANCH" "$REMOTE" "$DIR" || {
    fmt_error "git clone of repo failed"
    exit 1
  }

  echo
}

setup_launch() {
  sed -e  "s/SRC_DIR/${DIR//\//\\/}/g" $DIR/launch.plist > ~/Library/LaunchAgents/quiet_input_method.plist
  launchctl load ~/Library/LaunchAgents/quiet_input_method.plist
}

main() {
  setup_color

  if [ -d "$DIR" ]; then
    echo "${YELLOW}The \$DIR folder already exists ($DIR)"
  fi
    

  setup_src
  setup_launch

  printf "$GREEN"

}

main "$@"
