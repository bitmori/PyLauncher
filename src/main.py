import rumps
import os
import launchd

class AwesomeStatusBarApp(rumps.App):
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
    for job in launchd.jobs():
        print(job.label, job.pid)
        # print(job.plistfilename)
    # icon_path = "../assets/menubarIconTemplate@2x.png"
    # AwesomeStatusBarApp("Awesome App", icon=icon_path, template=True).run()
