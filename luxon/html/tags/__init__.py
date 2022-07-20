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
            self.nobody = True
            self.set("rel", "stylesheet")
            self.set("href", source)
        else:
            super().__init__("style")

    def set_style(self, css_text: str):
        if self.name != "style": return self

        css_text = Text(css_text)
        css_text.escape = False
        self.tags = [css_text]
        return self

"""
Represents a relationship between current document and an external resource
"""
class Link(Tag):
    def __init__(self, relation: str, target: str, media_type: str = None):
        super().__init__("link")
        self.nobody = True
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
Defines self-contained content
"""
class Article(Tag):
    def __init__(self):
        super().__init__("article")

"""
Defines content aside from main content
Mainly represented as sidebar
"""
class Aside(Tag):
    def __init__(self):
        super().__init__("aside")

"""
Defines additional details which user can either view or hide
"""
class Details(Tag):
    def __init__(self):
        super().__init__("details")

"""
Used to add a caption or explanation for the Figure element
"""
class Figcaption(Tag):
    def __init__(self):
        super().__init__("figcaption")

"""
Used to define a caption for a table
"""
class Caption(Tag):
    def __init__(self):
        super().__init__("caption")

"""
Used to define the title of the work, book, website, ...
"""
class Cite(Tag):
    def __init__(self):
        super().__init__("cite")

"""
Used to define the self-contained content
"""
class Figure(Tag):
    def __init__(self):
        super().__init__("figure")

"""
Represents a highlighted text
"""
class Mark(Tag):
    def __init__(self):
        super().__init__("mark")

"""
Represents section of page to represent navigation links
"""
class Nav(Tag):
    def __init__(self):
        super().__init__("nav")

"""
Defines a generic section for a document
"""
class Section(Tag):
    def __init__(self):
        super().__init__("section")

"""
Defines summary which can be used with Details
"""
class Summary(Tag):
    def __init__(self):
        super().__init__("summary")

"""
Define data/time within an HTML document
"""
class Time(Tag):
    def __init__(self):
        super().__init__("time")

"""
Creates a hyperlink or link
"""
class A(Tag):
    def __init__(self, text: str|Tag, target: str, new_window: bool = False):
        super().__init__("a")
        self.add(text)
        self.set("href", target)
        if new_window:
            self.set("target", "_blank")

"""
Defines the area of an image map
"""
class Area(Tag):
    def __init__(self):
        super().__init__("area")

"""
Used to define a content which is taken from another source
"""
class Blockquote(Tag):
    def __init__(self):
        super().__init__("blockquote")

"""
Produces a line break in text (carriage-return)
"""
class Br(Tag):
    def __init__(self):
        super().__init__("br")
        self.nobody = True

"""
Produces a horizontal line
"""
class Hr(Tag):
    def __init__(self):
        super().__init__("hr")
        self.nobody = True

"""
Used to represent a clickable button
"""
class Button(Tag):
    def __init__(self, text: str|Tag):
        super().__init__("button")
        self.add(text)

"""
Used to provide a graphics space within a web document
"""
class Canvas(Tag):
    def __init__(self):
        super().__init__("canvas")

"""
Used to display a part of programming code in an HTML document
"""
class Code(Tag):
    def __init__(self):
        super().__init__("code")

"""
Ddefines a column within a Table which represent common properties of columns and used with the Colgroup
"""
class Col(Tag):
    def __init__(self):
        super().__init__("col")

"""
Used to define group of columns in a table
"""
class Colgroup(Tag):
    def __init__(self):
        super().__init__("colgroup")

"""
Used to link the content with the machine-readable translation
"""
class Data(Tag):
    def __init__(self):
        super().__init__("data")

"""
Used to provide a predefined list for input option
"""
class Datalist(Tag):
    def __init__(self):
        super().__init__("datalist")

"""
Defines a dialog box or other interactive components
"""
class Dialog(Tag):
    def __init__(self):
        super().__init__("dialog")

"""
Used as embedded container for external file/application/media
"""
class Embed(Tag):
    def __init__(self):
        super().__init__("embed")

"""
Used to group related elements/labels within a web form
"""
class Fieldset(Tag):
    def __init__(self):
        super().__init__("fieldset")

"""
Defines a caption for content of Fieldset
"""
class Legend(Tag):
    def __init__(self):
        super().__init__("legend")

"""
Used to define an HTML form
"""
class Form(Tag):
    def __init__(self, method: str = None, action: str = None, multipart: bool = False):
        super().__init__("form")
        if method == None:
            method = "POST"
        self.set("method", method.upper())
        
        if action != None: self.set("action", action)
        if multipart: self.set("enctype", "multipart/form-data")

"""
Defines an input field within an HTML form
"""
class Input(Tag):
    def __init__(self, type: str):
        super().__init__("input")
        self.set("type", type.lower())
        self.nobody = True

"""
Used to define multiple line input, such as comment, feedback, and review
"""
class Textarea(Tag):
    def __init__(self):
        super().__init__("textarea")

"""
Used to declare the JavaScript within HTML document
"""
class Script(Tag):
    def __init__(self, source: str = None):
        super().__init__("script")
        if source != None: self.set("src", source)

    def set_code(self, code: str):
        code = Text(code)
        code.escape = False
        self.tags = [code]
        return self

"""
Represents a control which provides a menu of options
"""
class Select(Tag):
    def __init__(self):
        super().__init__("select")

"""
Used to define options or items in a drop-down list (Select)
"""
class Option(Tag):
    def __init__(self):
        super().__init__("option")

"""
Defines an inline frame which can embed other content
"""
class Iframe(Tag):
    def __init__(self, source: str = None):
        super().__init__("iframe")
        if source != None:
            self.set("src", source)

"""
Used to present data in tabular form or to create a table within HTML document
"""
class Table(Tag):
    def __init__(self):
        super().__init__("table")

"""
Defines the header of an HTML table
It is used along with Tbody and Tfoot
"""
class Thead(Tag):
    def __init__(self):
        super().__init__("thead")

"""
Represents the body content of an HTML table and used along with Thead and Tfoot
"""
class Tbody(Tag):
    def __init__(self):
        super().__init__("tbody")

"""
Defines the footer content of an HTML table
"""
class Tfoot(Tag):
    def __init__(self):
        super().__init__("tfoot")

"""
Defines the head cell of an HTML table
Used with Thead
"""
class Th(Tag):
    def __init__(self):
        super().__init__("th")

"""
Defines the row cells in an HTML table
"""
class Tr(Tag):
    def __init__(self):
        super().__init__("tr")

"""
Used to define cells of an HTML table which contains table data
"""
class Td(Tag):
    def __init__(self):
        super().__init__("td")

"""
Defines multiple media recourses for different media element such as Picture, Video, and Audio
"""
class Source(Tag):
    def __init__(self, source: str, type: str):
        super().__init__("source")
        self.set("src", source)
        self.set("type", type)
        self.nobody = True

"""
Defines more than one source elements and one image element
"""
class Picture(Tag):
    def __init__(self):
        super().__init__("picture")

"""
Used to embed audio content in HTML document
"""
class Audio(Tag):
    def __init__(self, source: str = None, autoplay: bool = False, controls: bool = False, loop: bool = False, muted: bool = False, preload: str = None):
        super().__init__("audio")
        if source: self.set("src", source)
        if autoplay: self.set("autoplay", True)
        if controls: self.set("controls", True)
        if loop: self.set("loop", True)
        if muted: self.set("muted", True)
        if preload: self.set("preload", preload)

"""
Used to embed a video content with an HTML document
"""
class Video(Tag):
    def __init__(self, source: str = None, width: int = None, height: int = None, poster: str = None, autoplay: bool = False, controls: bool = False, loop: bool = False, muted: bool = False, preload: str = None):
        super().__init__("video")
        if source: self.set("src", source)
        if width: self.set("width", str(width))
        if height: self.set("height", str(height))
        if poster: self.set("poster", poster)
        if autoplay: self.set("autoplay", True)
        if controls: self.set("controls", True)
        if loop: self.set("loop", True)
        if muted: self.set("muted", True)
        if preload: self.set("preload", preload)

"""
Heading 1
"""
class H1(Tag):
    def __init__(self): 
        super().__init__("h1")

"""
Heading 2
"""
class H2(Tag):
    def __init__(self): 
        super().__init__("h2")

"""
Heading 3
"""
class H3(Tag):
    def __init__(self): 
        super().__init__("h3")

"""
Heading 4
"""
class H4(Tag):
    def __init__(self): 
        super().__init__("h4")

"""
Heading 5
"""
class H5(Tag):
    def __init__(self): 
        super().__init__("h5")

"""
Heading 6
"""
class H6(Tag):
    def __init__(self): 
        super().__init__("h6")

"""
Used to define text tracks for Audio and Video
"""
class Track(Tag):
    def __init__(self):
        super().__init__("track")

"""
Used to make text font one size smaller than document's base font size
"""
class Small(Tag):
    def __init__(self):
        super().__init__("small")

"""
Defines preformatted text in an HTML document
"""
class Pre(Tag):
    def __init__(self, text: str):
        super().__init__("pre")
        self.add(text)

"""
Represents a paragraph in an HTML document
"""
class P(Tag):
    def __init__(self):
        super().__init__("p")

"""
Provides an alternative content if a script type is not supported in browser
"""
class Noscript(Tag):
    def __init__(self):
        super().__init__("noscript")

"""
Used to define important text
"""
class Strong(Tag):
    def __init__(self):
        super().__init__("strong")

"""
Used to represent a text in some different voice
"""
class I(Tag):
    def __init__(self):
        super().__init__("i")

"""
Used to render enclosed text with an underline
"""
class U(Tag):
    def __init__(self):
        super().__init__("u")

"""
Used to make a text bold
"""
class B(Tag):
    def __init__(self):
        super().__init__("b")

"""
Used to emphasis the content applied within this element
"""
class Em(Tag):
    def __init__(self):
        super().__init__("em")

"""
Defines a text label for Input of Form
"""
class Label(Tag):
    def __init__(self, text: str, for_id: str = None):
        super().__init__("label")
        if text: self.add(text)
        if for_id: self.set("for", for_id)

"""
Defines a text which displays as a subscript text
"""
class Sub(Tag):
    def __init__(self):
        super().__init__("sub")

"""
Defines a text which displays as a superscript text
"""
class Sup(Tag):
    def __init__(self):
        super().__init__("sup")

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