# 静かな入力方法

静かな入力方法は、Mac OS Xの入力方法切り替えです。アプリケーションに応じて入力方法を自動的に切り替えることができます。

[English](README.md) | [中文](README-zh.md) | [日本語](README-ja.md)

## 基本的なインストール方法

| 方法      | コマンド                                                                                           |
|:----------|:--------------------------------------------------------------------------------------------------|
| **curl**  | `sh -c "$(curl -fsSL https://raw.githubusercontent.com/Yufeikang/quiet_input_method/master/install.sh)"` |
| **wget**  | `sh -c "$(wget -O- https://raw.githubusercontent.com/Yufeikang/quiet_input_method/master/install.sh)"`   |
| **fetch** | `sh -c "$(fetch -o - https://raw.githubusercontent.com/Yufeikang/quiet_input_method/master/install.sh)"` |

## 手動インストール

1. `git`がインストールされていることを確認してください。もしインストールされていなければ、先にインストールしてください。

2. ターミナルを開き、プロジェクトをクローンしたいディレクトリに移動します。例えば：

   ```
   cd ~/my_custom_directory
   ```

3. デフォルトのアドレスを使用してプロジェクトのGitHubリポジトリをクローンします：

   ```
   git clone --depth=1 --branch master https://github.com/Yufeikang/quiet_input_method.git
   ```

   これにより、`quiet_input_method`という名前のディレクトリが作成されます。

4. クローンしたディレクトリに移動します：

   ```
   cd quiet_input_method
   ```

5. `sed`コマンドを使って、`launch.plist`ファイルの`SRC_DIR`を現在のディレクトリの値に置き換え、ファイルを`~/Library/LaunchAgents/quiet_input_method.plist`に保存します。

   ```
   sed -e "s/SRC_DIR/$(pwd | sed 's/\//\\\//g')/g" launch.plist > ~/Library/LaunchAgents/quiet_input_method.plist
   ```

6. `launchctl`コマンドを使って`quiet_input_method.plist`ファイルを読み込みます：

   ```
   launchctl load ~/Library/LaunchAgents/quiet_input_method.plist
   ```

これらの手順が完了すると、静かな入力方法がインストールされ、正常に設定されるはずです。

## 設定例

ファイル ~/.quiet.json

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

## 更新と再起動

```
sh ./update.sh
```
