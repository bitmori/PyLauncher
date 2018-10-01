import rumps
import os
import launchd
import job

ICON_PATH = "../assets/menubarIconTemplate@2x.png"

class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        super(AwesomeStatusBarApp, self).__init__("Awesome App", icon=ICON_PATH, template=True)
        agents = job.get_user_agents()
        self.from_agents_to_menu_items(agents)
        # self.menu.add(rumps.MenuItem("TEST", callback=lambda sender: print(sender)))
        self.menu.add(rumps.separator)

    def from_agents_to_menu_items(self, agents):
        self.menu = [
            a.label for a in agents
        ]


if __name__ == "__main__":
    AwesomeStatusBarApp().run()
