from luxon.html import *

"""
Represents the root (top-level element) of an HTML document
"""
class Html(Tag):
    def __init__(self):
        super().__init__("html")
        self.before = "<!DOCTYPE html>"

"""
Defines the head section of an HTML document
"""
class Head(Tag):
    def __init__(self):
        super().__init__("head")

"""
Defines the title or name of an HTML document
"""
class Title(Tag):
    def __init__(self, title: str|Text = None):
        super().__init__("title")
        if title != None:
            self.add(title)

"""
Defines the metadata of an HTML document
"""
class Meta(Tag):
    def __init__(self):
        super().__init__("meta")

"""
Defines the style information for an HTML document
"""
class Style(Tag):
    def __init__(self, source: str = None):
        if source != None:
            super().__init__("link")
            self.set("rel", "stylesheet")
            self.set("href", source)
        else:
            super().__init__("source")

"""
Represents a relationship between current document and an external resource
"""
class Link(Tag):
    def __init__(self, relation: str, target: str, media_type: str = None):
        super().__init__("link")
        self.set("rel", relation)
        self.set("href", target)
        if media_type != None:
            self.set("type", media_type)

"""
Defines the body section of an HTML document
"""
class Body(Tag):
    def __init__(self):
        super().__init__("body")

"""
Defines the header of a section or webpage
"""
class Header(Tag):
    def __init__(self):
        super().__init__("header")

"""
Represents the main content of an HTML document
"""
class Main(Tag):
    def __init__(self):
        super().__init__("main")

"""
Defines the footer section of a webpage
"""
class Footer(Tag):
    def __init__(self):
        super().__init__("footer")

"""
Used for styling and grouping inline
"""
class Span(Tag):
    def __init__(self):
        super().__init__("span")

"""
Defines a division or section within HTML document
"""
class Div(Tag):
    def __init__(self):
        super().__init__("div")

"""
Defines ordered list of items
"""
class Ol(Tag):
    def __init__(self):
        super().__init__("ol")

"""
Defines unordered list of items
"""
class Ul(Tag):
    def __init__(self):
        super().__init__("ul")

"""
Used to represent items in list
"""
class Li(Tag):
    def __init__(self, content: Tag|str):
        super().__init__("li")
        self.add(content)

"""
Used to insert an image within an HTML document
"""
class Img(Tag):
    def __init__(self, src: str):
        super().__init__("img")
        self.nobody = True
        self.set("src", src)

"""
Comments are not displayed in the browsers but they're visible in the source code
"""
class Comment(Tag):
    def __init__(self, comment: str):
        super().__init__(None)
        self.set_text(comment)
        self.before = "<!-- "
        self.after = " -->"