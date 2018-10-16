# autoSwitchIputMothod
自动切换mac输入法-安静模式

> 此脚本可以自动切换指定程序输入法到en状态，即方便开发者使用的安静模式

## 将脚本设置为开机自启动的方法

#### 1.在目录`~/Library/LaunchAgents`下创建文件 xx.xx.plist,内容如下
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC -//Apple Computer//DTD PLIST 1.0//EN
http://www.apple.com/DTDs/PropertyList-1.0.dtd >
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>此处为应用名字</string>
    <key>ProgramArguments</key>
    <array>
         <string>python</string>
	 <string>你的脚本路径/autoSwitch.py</string>
    </array>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>你的日志路径keyAutoSwitch.log</string>
    <key>StandardOutPath</key>
    <string>你的日志路径KeyAutoSwitch.log</string>
    <key>WorkingDirectory</key>
    <string>/tmp/</string>
</dict>
</plist>
```
替换掉路径部分
#### 2. 配置
在用户目录`~`,创建文件 `.need_sw_app`
将需要使用安静模式的app的bundleId添加到该文件中即可，
如：
```
com.jetbrains.PhpStorm
com.jetbrains.pycharm
com.microsoft.VSCode
com.apple.TextEdit
com.google.Chrome
com.jetbrains.WebStorm
```

> PS：查询bundleID的方法
`osascript -e 'id of app "Chrome"'`
#### 3. 加载
```
launchctl load ~/Library/LaunchAgents/xx.xx.plist
```
#### 4. 卸载
```
launchctl unload ~/Library/LaunchAgents/xx.xx.plist
```
