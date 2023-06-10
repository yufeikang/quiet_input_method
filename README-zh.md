# 安静输入法

安静输入法是 Mac OS X 上的输入法切换器。 它可以根据应用自动切换输入法。

[English](README.md) | [中文](README-zh.md) | [日本語](README-ja.md)

## 基本安装

| 方法      | 命令                                                                                            |
|:----------|:--------------------------------------------------------------------------------------------------|
| **curl**  | `sh -c "$(curl -fsSL https://raw.githubusercontent.com/Yufeikang/quiet_input_method/master/install.sh)"` |
| **wget**  | `sh -c "$(wget -O- https://raw.githubusercontent.com/Yufeikang/quiet_input_method/master/install.sh)"`   |
| **fetch** | `sh -c "$(fetch -o - https://raw.githubusercontent.com/Yufeikang/quiet_input_method/master/install.sh)"` |

## 手动安装

1. 确保已安装 `git` 。 如果没有，请先安装。

2. 打开终端并导航到要克隆项目的目录。 例如：

   ```
   cd ~/my_custom_directory
   ```

3. 使用默认地址克隆项目的 GitHub 仓库：

   ```
   git clone --depth=1 --branch master https://github.com/Yufeikang/quiet_input_method.git
   ```

   这将创建一个名为 `quiet_input_method` 的目录。

4. 切换到克隆的目录：

   ```
   cd quiet_input_method
   ```

5. 使用 `sed` 命令将当前目录的值替换为 `launch.plist` 文件中的 `SRC_DIR` ，然后将文件保存到
`~/Library/LaunchAgents/quiet_input_method.plist` 中。

   ```
   sed -e "s/SRC_DIR/$(pwd | sed 's/\//\\\//g')/g" launch.plist > ~/Library/LaunchAgents/quiet_input_method.plist
   ```

6. 使用 `launchctl` 命令加载 `quiet_input_method.plist` 文件：

   ```
   launchctl load ~/Library/LaunchAgents/quiet_input_method.plist
   ```

完成这些步骤后，静音输入法应安装并配置成功。

## 配置示例

 文件 ~/.quiet.json

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

## 更新和重启

```
sh ./update.sh
```
