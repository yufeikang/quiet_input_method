# Quiet Input Method

Quiet Input Method is a input method switcher on Mac OS X. It can automatically switch input method according to the application.

[English](README.md) | [中文](README-zh.md) | [日本語](README-ja.md)

## Basic Installation

| Method    | Command                                                                                           |
|:----------|:--------------------------------------------------------------------------------------------------|
| **curl**  | `sh -c "$(curl -fsSL https://raw.githubusercontent.com/Yufeikang/quiet_input_method/master/install.sh)"` |
| **wget**  | `sh -c "$(wget -O- https://raw.githubusercontent.com/Yufeikang/quiet_input_method/master/install.sh)"`   |
| **fetch** | `sh -c "$(fetch -o - https://raw.githubusercontent.com/Yufeikang/quiet_input_method/master/install.sh)"` |

## Manual Installation

1. Make sure `git` is installed. If it's not, please install it first.

2. Open the terminal and navigate to the directory where you want to clone the project. For example:

   ```
   cd ~/my_custom_directory
   ```

3. Clone the project's GitHub repository using the default address:

   ```
   git clone --depth=1 --branch master https://github.com/Yufeikang/quiet_input_method.git
   ```

   This will create a directory named `quiet_input_method`.

4. Change to the cloned directory:

   ```
   cd quiet_input_method
   ```

5. Use the `sed` command to replace `SRC_DIR` in the `launch.plist` file with the current directory's value and save the file to `~/Library/LaunchAgents/quiet_input_method.plist`.

   ```
   sed -e "s/SRC_DIR/$(pwd | sed 's/\//\\\//g')/g" launch.plist > ~/Library/LaunchAgents/quiet_input_method.plist
   ```

6. Use the `launchctl` command to load the `quiet_input_method.plist` file:

   ```
   launchctl load ~/Library/LaunchAgents/quiet_input_method.plist
   ```

After completing these steps, the quiet_input_method should be installed and configured successfully.

## Config Example

 file ~/.quiet.json

```
  {
    "default": "abc",
    "appConfig": {
      "Shuangpin": [
        "Telegram",
        "WeChat"
      ],
      "abc": [
        "Code"
      ]
    }
  }
```

## Update & restart

```
sh ./update.sh
```
