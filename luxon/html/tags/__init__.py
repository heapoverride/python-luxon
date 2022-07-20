from luxon.html import *

class Html(Tag):
    def __init__(self):
        super().__init__("html")
        self.before = "<!DOCTYPE html>"

class Head(Tag):
    def __init__(self):
        super().__init__("head")

class Title(Tag):
    def __init__(self, title: str|Text = None):
        super().__init__("title")
        if title != None:
            self.add(title)

class Link(Tag):
    def __init__(self):
        super().__init__("link")

class Meta(Tag):
    def __init__(self):
        super().__init__("meta")

class Body(Tag):
    def __init__(self):
        super().__init__("body")

class Header(Tag):
    def __init__(self):
        super().__init__("header")

class Main(Tag):
    def __init__(self):
        super().__init__("main")

class Footer(Tag):
    def __init__(self):
        super().__init__("footer")

class Span(Tag):
    def __init__(self):
        super().__init__("span")

class Div(Tag):
    def __init__(self):
        super().__init__("div")

class Ol(Tag):
    def __init__(self):
        super().__init__("ol")

class Ul(Tag):
    def __init__(self):
        super().__init__("ul")

class Li(Tag):
    def __init__(self, content: Tag|str):
        super().__init__("li")
        self.add(content)

class Img(Tag):
    def __init__(self, src: str):
        super().__init__("img")
        self.nobody = True
        self.set("src", src)