#! /usr/bin/env python
# coding: utf-8

"""
auto switch keyboard input source for mac os
"""

import ctypes
import ctypes.util
import json
import logging
import os
from functools import lru_cache
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

logger = logging.getLogger("quiet")

home = Path().home()
config_file = home / ".quiet.json"


class Config(object):
    def __init__(self):
        self._config = {
            "default": None,
            "apps": [
                {
                    "name": "Code",
                    "input_source": "en",
                },
                {
                    "id": "com.microsoft.VSCode",
                    "input_source": "en",
                },
                {
                    "name": "Wechat",
                    "input_source": "zh-CN",
                },
            ],
            "ignore_apps": [
                "com.apple.Safari",
                "Google Chrome",
            ],
        }
        if config_file.exists():
            logger.info("load config from %s", config_file)
            self._config = json.loads(config_file.read_text())
            logger.debug("config: %s", self._config)
        else:
            logger.info(
                "config file not found, use default config, and save to %s", config_file
            )
            config_file.write_text(json.dumps(self._config, indent=4))

    @lru_cache()
    def get_input_source(self, app_name, app_id):
        for ignored_app in self._config.get("ignore_apps"):
            if app_name == ignored_app or app_id == ignored_app:
                return None

        for app in self._config.get("apps"):
            if app_name == app.get("name") or app_id == app.get("id"):
                return app.get("input_source")
        return self._config.get("default")

    @property
    def config(self):
        return self._config


user_config = Config()


logging.basicConfig(
    level=user_config.config.get("log_level", logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger.info("start")

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


def select_kb(lang):
    logger.debug(f"select_kb: {lang}")
    cur = carbon.TISCopyInputSourceForLanguage(
        CoreFoundation.CFSTR(lang).__c_void_p__()
    )
    carbon.TISSelectInputSource(cur)


class Observer(NSObject):
    def handle_(self, noti):
        info = noti.userInfo().objectForKey_(NSWorkspaceApplicationKey)
        bundle_identifier = info.bundleIdentifier()
        logger.debug(f"handle: {info.localizedName()}[{bundle_identifier}]")
        input_source = user_config.get_input_source(
            info.localizedName(), bundle_identifier
        )
        if input_source:
            select_kb(input_source)


def main():
    send_notification("Running", None, "Auto Switch Input Source is running ...")
    nc = NSWorkspace.sharedWorkspace().notificationCenter()
    observer = Observer.new()
    nc.addObserver_selector_name_object_(
        observer, "handle:", NSWorkspaceDidActivateApplicationNotification, None
    )
    AppHelper.runConsoleEventLoop(installInterrupt=True)


main()
