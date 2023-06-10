import AppKit
import Carbon
import Foundation

func getInputMethodList() -> [String] {
  let list = TISCreateInputSourceList(nil, false).takeRetainedValue() as! [TISInputSource]
  var inputMethodList = [String]()
  for source in list {
    if let name = TISGetInputSourceProperty(source, kTISPropertyInputSourceID) {
      let sourceName = Unmanaged<CFString>.fromOpaque(name).takeUnretainedValue() as String
      inputMethodList.append(sourceName)
    }
  }
  return inputMethodList
}

func getSelectedInputMethod() -> String {
  let currentSource = TISCopyCurrentKeyboardInputSource().takeRetainedValue()
  let name = TISGetInputSourceProperty(currentSource, kTISPropertyInputSourceID)
  let sourceName = Unmanaged<CFString>.fromOpaque(name!).takeUnretainedValue() as String
  return sourceName
}

func switchInputMethod(to inputMethod: String) {
  let inputSources = TISCreateInputSourceList(nil, false).takeRetainedValue() as! [TISInputSource]
  for inputSource in inputSources {
    if let inputSourceID = TISGetInputSourceProperty(inputSource, kTISPropertyInputSourceID) {
      let inputSourceIDString =
        Unmanaged<CFString>.fromOpaque(inputSourceID).takeUnretainedValue() as String
      if inputSourceIDString.range(of: inputMethod, options: .caseInsensitive) != nil {
        print("Switching to \(inputSourceIDString)")
        TISSelectInputSource(inputSource)
        return
      }
    }
  }
  print("Not found \(inputMethod), maybe not installed?")

}

// Check if config.json file exists
let fileManager = FileManager.default
let configFilePath =
  "\(ProcessInfo.processInfo.environment["HOME"]!)/.quiet_input_method/.quiet.json"
var configData: Data?
if fileManager.fileExists(atPath: configFilePath) {
  configData = fileManager.contents(atPath: configFilePath)
}

// Default config
var DEFAULT_CONFIG = """
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
  """

// Convert json to dict
func jsonToDict(jsonData: Data) -> [String: Any] {
  let dict =
    try? JSONSerialization.jsonObject(with: jsonData, options: .mutableContainers) as! [String: Any]
  return dict ?? [:]
}

// Load config from file or use default config
var config = jsonToDict(jsonData: configData ?? DEFAULT_CONFIG.data(using: .utf8)!)

func getInputMethodByConfig(appName: String) -> String {
  for (key, value) in config["appConfig"] as! [String: [String]] {

    let appList = value
    if appList.contains(appName) {
      return key
    }
  }
  // if default config exists, use it
  if let defaultInputMethod = config["default"] as? String {
    return defaultInputMethod
  }
  return "Unknown"
}

// Listen for app switch events and print the current app
let workspace = NSWorkspace.shared
var currentApp: NSRunningApplication?

workspace.notificationCenter.addObserver(
  forName: NSWorkspace.didActivateApplicationNotification, object: nil, queue: nil
) { notification in
  if let app = notification.userInfo?[NSWorkspace.applicationUserInfoKey] as? NSRunningApplication {
    if app != currentApp {
      currentApp = app
      let appName = app.localizedName ?? "Unknown"
      let inputMethod = getInputMethodByConfig(appName: appName)
      if inputMethod == "Unknown" {
        return
      }
      print("Current app: \(app.localizedName ?? "Unknown") to \(inputMethod)")
      switchInputMethod(to: inputMethod)
    }
  }
}

print("Listening for app switch events...")

// list all input methods
for inputMethod in getInputMethodList() {
  print(inputMethod)
}

RunLoop.main.run()
