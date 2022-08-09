from luxon.html.tags import *

class Document(Html):
    def __init__(self, title: str):
        super().__init__()

        # head
        self.head = Head()
        self.add(self.head)

        # head > title
        self.head.add(Title(title))

        # head > link
        self.head.add(Style("/assets/styles/base.css"))

        # body
        self.body = Body()
        self.add(self.body)

        # body > header
        self.header = Header()
        self.body.add(self.header)

        # body > nav
        self.nav = Nav().add(
            A("Home", "/").set("data-page", "home"),
            A("About", "/about").set("data-page", "about")
        )
        self.body.add(self.nav)

        # body > main
        self.main = Main()
        self.body.add(self.main)
        
        # body > footer
        self.footer = Footer()
        self.body.add(self.footer)