#! /usr/bin/env python
# coding: utf-8

"""
auto switch keyboard between different applications
if you want to change the app list, modify the var 'ignore_list'
"""

import ctypes
import ctypes.util
import os
import time
from pathlib import Path

import AppKit
import Cocoa
import CoreFoundation
import Foundation
import objc
from AppKit import (
    NSWorkspace,
    NSWorkspaceApplicationKey,
    NSWorkspaceDidActivateApplicationNotification,
)
from Foundation import NSObject
from PyObjCTools import AppHelper

current_dir = Path(__file__).parent.absolute()

info = AppKit.NSBundle.mainBundle().infoDictionary()
info["LSBackgroundOnly"] = "1"
# set icon
icon_file = (current_dir / "icon.icns").as_posix()
icon = Cocoa.NSImage.alloc().initWithContentsOfFile_(icon_file)

Cocoa.NSApplication.sharedApplication().setApplicationIconImage_(icon)


def send_notification(title, subtitle, info_text, delay=0, sound=False, userInfo={}):
    NSUserNotification = objc.lookUpClass("NSUserNotification")
    NSUserNotificationCenter = objc.lookUpClass("NSUserNotificationCenter")
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(info_text)
    notification.setUserInfo_(userInfo)
    notification.setContentImage_(icon)
    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setDeliveryDate_(
        Foundation.NSDate.dateWithTimeInterval_sinceDate_(
            delay, Foundation.NSDate.date()
        )
    )
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(
        notification
    )


# add your custom apps here, check the bundle id in /Application/xx.app/Contents/info.plist

home = Path().home()
config = home / ".quiet"


app_list = [
    "com.googlecode.iterm2",
    "com.runningwithcrayons.Alfred-2",
]

app_dict = {"com.tencent.xinWeChat": "zh-CN"}

if os.path.exists(config):
    with open(config, "r+") as f:
        for l in f.readlines():
            app_list.append(l.replace("\n", "".replace("\r", "")))

for app in app_list:
    if app.find(":") != -1:
        app, lang = app.split(":")
        app_dict[app] = lang if lang else "en"
    else:
        app_dict[app] = "en"
app_list = list(app_dict.keys())

carbon = ctypes.cdll.LoadLibrary(ctypes.util.find_library("Carbon"))

_objc = ctypes.PyDLL(objc._objc.__file__)

# PyObject *PyObjCObject_New(id objc_object, int flags, int retain)
try:
    _objc.PyObjCObject_New.restype = ctypes.py_object
    _objc.PyObjCObject_New.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
except AttributeError:
    msg = "PyObjCObject_New is not available on this system, this is issue , please downgrade pyobjc to 7.3: pip install --upgrade pyobjc==7.3"
    send_notification("Error", None, msg, sound=True)
    raise Exception(msg)


def objc_object(id):
    return _objc.PyObjCObject_New(id, 0, 1)


# kTISPropertyLocalizedName
kTISPropertyUnicodeKeyLayoutData_p = ctypes.c_void_p.in_dll(
    carbon, "kTISPropertyInputSourceIsEnabled"
)
kTISPropertyInputSourceLanguages_p = ctypes.c_void_p.in_dll(
    carbon, "kTISPropertyInputSourceLanguages"
)
kTISPropertyInputSourceType_p = ctypes.c_void_p.in_dll(
    carbon, "kTISPropertyInputSourceType"
)
kTISPropertyLocalizedName_p = ctypes.c_void_p.in_dll(
    carbon, "kTISPropertyLocalizedName"
)

kTISPropertyInputSourceCategory = objc_object(
    ctypes.c_void_p.in_dll(carbon, "kTISPropertyInputSourceCategory")
)
kTISCategoryKeyboardInputSource = objc_object(
    ctypes.c_void_p.in_dll(carbon, "kTISCategoryKeyboardInputSource")
)


# TISCreateInputSourceList
carbon.TISCreateInputSourceList.restype = ctypes.c_void_p
carbon.TISCreateInputSourceList.argtypes = [ctypes.c_void_p, ctypes.c_bool]

carbon.TISSelectInputSource.restype = ctypes.c_void_p
carbon.TISSelectInputSource.argtypes = [ctypes.c_void_p]

carbon.TISGetInputSourceProperty.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
carbon.TISGetInputSourceProperty.restype = ctypes.c_void_p

carbon.TISCopyInputSourceForLanguage.argtypes = [ctypes.c_void_p]
carbon.TISCopyInputSourceForLanguage.restype = ctypes.c_void_p


def get_avaliable_languages():
    single_langs = [
        x
        for x in [
            objc_object(
                carbon.TISGetInputSourceProperty(
                    CoreFoundation.CFArrayGetValueAtIndex(
                        objc_object(s), x
                    ).__c_void_p__(),
                    kTISPropertyInputSourceLanguages_p,
                )
            )
            for x in range(
                CoreFoundation.CFArrayGetCount(
                    objc_object(carbon.TISCreateInputSourceList(None, 0))
                )
            )
        ]
        if x.count() == 1
    ]
    res = set()
    list(map(lambda y: res.add(y[0]), single_langs))
    return res


def select_kb(lang):
    cur = carbon.TISCopyInputSourceForLanguage(
        CoreFoundation.CFSTR(lang).__c_void_p__()
    )
    carbon.TISSelectInputSource(cur)


class Observer(NSObject):
    def handle_(self, noti):
        info = noti.userInfo().objectForKey_(NSWorkspaceApplicationKey)
        bundleIdentifier = info.bundleIdentifier()
        if bundleIdentifier in app_list:
            print(
                "%s : %s active to %s"
                % (
                    time.asctime(time.localtime(time.time())),
                    bundleIdentifier,
                    app_dict[bundleIdentifier],
                )
            )
            select_kb(app_dict[bundleIdentifier])


def main():
    send_notification("Running", None, "Auto Switch Input Source is running ...")
    nc = NSWorkspace.sharedWorkspace().notificationCenter()
    observer = Observer.new()
    nc.addObserver_selector_name_object_(
        observer, "handle:", NSWorkspaceDidActivateApplicationNotification, None
    )
    AppHelper.runConsoleEventLoop(installInterrupt=True)


main()
