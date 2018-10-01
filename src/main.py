import rumps
import os
import launchd

from job import job_type

ICON_PATH = "../assets/menubarIconTemplate@2x.png"

class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__("Awesome App", icon=ICON_PATH, template=True)
        self.menu = ["Preferences", "Silly button", "Say hi"]
        self.menu.add(rumps.MenuItem("TEST", callback=lambda sender: print(sender)))
        self.menu.add(rumps.separator)

    @rumps.clicked("Preferences")
    def prefs(self, _):
        rumps.alert("jk! no preferences available!")

    @rumps.clicked("Silly button")
    def onoff(self, sender):
        sender.state = not sender.state

    @rumps.clicked("Say hi")
    def sayhi(self, _):
        rumps.notification("Awesome title", "amazing subtitle", "hi!!1")


if __name__ == "__main__":
    # for job in launchd.jobs():
    #     print(job.label, job.pid)
    #     print(job.plistfilename, job_type(job))
    AwesomeStatusBarApp().run()
