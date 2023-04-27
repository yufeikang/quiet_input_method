# Quiet Input Method

Quiet Input Method is a input method switcher on Mac OS X. It can automatically switch input method according to the application.

## Basic Installation

| Method    | Command                                                                                           |
|:----------|:--------------------------------------------------------------------------------------------------|
| **curl**  | `sh -c "$(curl -fsSL https://raw.githubusercontent.com/Yufeikang/quiet_input_method/master/install.sh)"` |
| **wget**  | `sh -c "$(wget -O- https://raw.githubusercontent.com/Yufeikang/quiet_input_method/master/install.sh)"`   |
| **fetch** | `sh -c "$(fetch -o - https://raw.githubusercontent.com/Yufeikang/quiet_input_method/master/install.sh)"` |

## Config Example

 file ~/.quiet.json

```
{
  "default": "en",
  "ignore_apps": ["Google Chrome", "Safari"],
  "apps":
    [
      { "name": "WeChat", "input_source": "zh-CN" },
      { "id": "jp.naver.line.mac", "input_source": "ja-JP" },
    ],
}

```
