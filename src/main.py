import glob
import os
import plistlib

import launchd
import rumps
import subprocess

from AppKit import NSAttributedString
from PyObjCTools.Conversion import propertyListFromPythonCollection
from Cocoa import (NSFont, NSFontAttributeName,
                   NSColor, NSForegroundColorAttributeName)
from launchd.cmd import launchctl

ICON_PATH = "../assets/menubarIconTemplate@2x.png"
USER_AGENTS = os.path.expanduser('~/Library/LaunchAgents')

FONT = NSFont.fontWithName_size_("Hack Nerd Font", 14.0)
color = {"red": NSColor.redColor(), "blue": NSColor.blueColor(), "green": NSColor.greenColor()}
r_attr = propertyListFromPythonCollection({
    # NSFontAttributeName: FONT,
    NSForegroundColorAttributeName: color['red']},
    conversionHelper=lambda x: x)
g_attr = propertyListFromPythonCollection({
    # NSFontAttributeName: FONT,
    NSForegroundColorAttributeName: color['green']},
    conversionHelper=lambda x: x)
b_attr = propertyListFromPythonCollection({
    # NSFontAttributeName: FONT,
    NSForegroundColorAttributeName: color['blue']},
    conversionHelper=lambda x: x)

def insert_log_menu_items(ar: rumps.MenuItem, ag):
    log = ag['StandardOutPath']
    log_cb = lambda x: subprocess.call(["open", "-a", "Console", log])
    err = ag['StandardErrorPath']
    err_cb = lambda x: subprocess.call(["open", "-a", "Console", err])
    ar.add(rumps.separator)
    ar.add(rumps.MenuItem("View Log", callback=log_cb if log else None))
    ar.add(rumps.MenuItem("View Error Log", callback=err_cb if err else None))
    ar.add(rumps.separator)


def insert_unload_reload(ar: rumps.MenuItem, j: launchd.LaunchdJob):
    print(j.plistfilename)
    ar.add(rumps.MenuItem("Unload", callback=lambda x: launchd.unload(j.plistfilename)))
    ar.add(rumps.MenuItem("Reload", callback=lambda x: launchd.unload(j.plistfilename) and launchd.load(j.plistfilename)))


def agent_to_menu_item(agent) -> rumps.MenuItem:
    ag = plistlib.readPlist(agent)
    label = ag['Label']
    ar = rumps.MenuItem("")
    aj = launchd.LaunchdJob(label)
    exist = aj.exists()
    if exist:
        pid = aj.pid
        status = aj.laststatus
        if pid == -1 and status == 0:
            ar_title = NSAttributedString.alloc().initWithString_attributes_(label, b_attr)
            ar._menuitem.setAttributedTitle_(ar_title)
            insert_unload_reload(ar, aj)
            ar.add(rumps.MenuItem("Start", callback=lambda x: launchctl("start", label)))
            insert_log_menu_items(ar, ag)
            ar.add("Idle")
            ar.add("No Errors")
        elif pid > 0 and status == 0:
            ar_title = NSAttributedString.alloc().initWithString_attributes_(label, g_attr)
            ar._menuitem.setAttributedTitle_(ar_title)
            insert_unload_reload(ar, aj)
            ar.add(rumps.MenuItem("Stop", callback=lambda x: launchctl("stop", label)))
            insert_log_menu_items(ar, ag)
            ar.add(f"Running ({pid})")
            ar.add("No Errors")
        elif status != 0:
            ar_title = NSAttributedString.alloc().initWithString_attributes_(label, r_attr)
            ar._menuitem.setAttributedTitle_(ar_title)
            insert_unload_reload(ar, aj)
            ar.add(rumps.MenuItem("Start", callback=lambda x: launchctl("start", label)))
            insert_log_menu_items(ar, ag)
            ar.add("Stopped")
            ar.add(f"Error ({status})")
    else:
        ar.title = label
        sub_load = rumps.MenuItem(title="Load",
                                  callback=lambda x: launchd.load(f"{USER_AGENTS}/{label}.plist"))
        ar.add(sub_load)
        insert_log_menu_items(ar, ag)
        ar.add("Unloaded")
    return ar


class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__("Awesome App", icon=ICON_PATH, template=True)
        prefix = "unison"
        agents = glob.glob(f"{USER_AGENTS}/{prefix}*.plist")
        items = map(agent_to_menu_item, agents)
        # self.menu.add(rumps.MenuItem("TEST", callback=lambda sender: print(sender)))
        self.menu = items
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Refresh"))
        # rumps.Timer()


if __name__ == "__main__":
    AwesomeStatusBarApp().run()
