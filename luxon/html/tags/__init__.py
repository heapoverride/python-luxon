from __future__ import annotations
from luxon.html import *

"""
Represents the root (top-level element) of an HTML document
"""
class Html(Tag):
    def __init__(self):
        super().__init__("html")
        self.before = "<!DOCTYPE html>\n"

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
        if title: self.add(title)

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
        if source:
            super().__init__("link")
            self.nobody = True
            self.set("rel", "stylesheet")
            self.set("href", source)
        else:
            super().__init__("style")

    def add_style(self, css_text: str):
        if self.name != "style": return self

        css_text = Text(css_text)
        css_text.escape = False
        self.add(css_text)
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
        if media_type: self.set("type", media_type)

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
    def __init__(self, *content: str|Tag):
        super().__init__("span")
        self.add(*content)

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
    def __init__(self, *content: str|Tag):
        super().__init__("details")
        self.add(*content)

"""
Used to add a caption or explanation for the Figure element
"""
class Figcaption(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("figcaption")
        self.add(*content)

"""
Used to define a caption for a table
"""
class Caption(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("caption")
        self.add(*content)

"""
Used to define the title of the work, book, website, ...
"""
class Cite(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("cite")
        self.add(*content)

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
    def __init__(self, *content: str|Tag):
        super().__init__("mark")
        self.add(*content)

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
    def __init__(self, *content: str|Tag):
        super().__init__("summary")
        self.add(*content)

"""
Define data/time within an HTML document
"""
class Time(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("time")
        self.add(*content)

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
    def __init__(self, *content: str|Tag):
        super().__init__("blockquote")
        self.add(*content)

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
    def __init__(self, *content: str|Tag):
        super().__init__("code")
        self.add(*content)

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

    def add_legend(self, *content: str|Tag):
        self.add(Legend(*content))

"""
Defines a caption for content of Fieldset
"""
class Legend(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("legend")
        self.add(*content)

"""
Used to define an HTML form
"""
class Form(Tag):
    def __init__(self, method: str = None, action: str = None, multipart: bool = False):
        super().__init__("form")
        if method == None:
            method = "POST"
        self.set("method", method.upper())
        
        if action: self.set("action", action)
        if multipart: self.set("enctype", "multipart/form-data")

"""
Defines an input field within an HTML form
"""
class Input(Tag):
    def __init__(self, type: str, id: str = None, name: str = None, value: str = None):
        super().__init__("input")
        self.set("type", type.lower())
        self.nobody = True
        if id: self.set_id(id)
        if name: self.set_name(name)
        if value: self.set_value(value)

"""
Used to define multiple line input, such as comment, feedback, and review
"""
class Textarea(Tag):
    def __init__(self, id: str = None, name: str = None, width: int = None, height: int = None):
        super().__init__("textarea")
        if id: self.set_id(id)
        if name: self.set_name(name)
        if width: self.set("width", str(width))
        if height: self.set("height", str(height))
"""
Used to declare the JavaScript within HTML document
"""
class Script(Tag):
    def __init__(self, source: str = None):
        super().__init__("script")
        if source: self.set("src", source)

    def add_code(self, code: str):
        code = Text(code)
        code.escape = False
        self.add(code)
        return self

"""
Represents a control which provides a menu of options
"""
class Select(Tag):
    def __init__(self, id: str = None, name: str = None):
        super().__init__("select")
        if id: self.set_id(id)
        if name: self.set_name(name)

"""
Used to define options or items in a drop-down list (Select)
"""
class Option(Tag):
    def __init__(self, text: str, value: str = None):
        super().__init__("option")
        self.add(text)
        if value: self.set_value(value)

"""
Defines an inline frame which can embed other content
"""
class Iframe(Tag):
    def __init__(self, source: str = None):
        super().__init__("iframe")
        if source: self.set("src", source)

"""
Used to present data in tabular form or to create a table within HTML document
"""
class Table(Tag):
    def __init__(self):
        super().__init__("table")

    def add_header_row(self, *cells: str|Tag):
        self.add(Tr().add_headers(*cells))
        return self

    def add_row(self, *cells: str|Tag):
        self.add(Tr().add_columns(*cells))
        return self

    def add_thead(self, *rows: list[str|Tag]):
        thead = Thead()
        for row in rows: 
            thead.add_row(*row)
        self.add(thead)
        return self

    def add_tbody(self, *rows: list[str|Tag]):
        tbody = Tbody()
        for row in rows: 
            tbody.add_row(*row)
        self.add(tbody)
        return self

    def add_tfoot(self, *rows: list[str|Tag]):
        tfoot = Tfoot()
        for row in rows: 
            tfoot.add_row(*row)
        self.add(tfoot)
        return self

"""
Defines the header of an HTML table
It is used along with Tbody and Tfoot
"""
class Thead(Tag):
    def __init__(self):
        super().__init__("thead")

    def add_row(self, *columns: str|Tag):
        self.add(Tr().add_headers(*columns))
        return self

"""
Represents the body content of an HTML table and used along with Thead and Tfoot
"""
class Tbody(Tag):
    def __init__(self):
        super().__init__("tbody")

    def add_row(self, *columns: str|Tag):
        self.add(Tr().add_columns(*columns))
        return self

"""
Defines the footer content of an HTML table
"""
class Tfoot(Tag):
    def __init__(self):
        super().__init__("tfoot")

    def add_row(self, *columns: str|Tag) -> Tr:
        row = Tr().add_columns(*columns)
        self.add(row)
        return row

"""
Defines the row cells in an HTML table
"""
class Tr(Tag):
    def __init__(self):
        super().__init__("tr")

    def add_headers(self, *columns: str|Tag):
        self.add([Th(x) for x in columns])
        return self

    def add_columns(self, *columns: str|Tag):
        self.add([Td(x) for x in columns])
        return self

"""
Defines the head cell of an HTML table
Used with Thead
"""
class Th(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("th")
        self.add(*content)

"""
Used to define cells of an HTML table which contains table data
"""
class Td(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("td")
        self.add(*content)

"""
Defines multiple media recourses for different media element such as Picture, Video, and Audio
"""
class Source(Tag):
    def __init__(self, source: str|list[str], mime_type: str = None, media_query: str = None):
        super().__init__("source")
        self.nobody = True

        if type(source) == str:
            self.set("src", source)
        elif type(source) == list:
            self.set("srcset", ",".join(source))

        if mime_type: self.set("type", mime_type)
        if media_query: self.set("media", media_query)

"""
Defines more than one source elements and one image element
"""
class Picture(Tag):
    def __init__(self):
        super().__init__("picture")

    def add_source(self, sources: list[str], media_query: str):
        self.add(Source(sources, media_query=media_query))
        return self

    def add_image(self, source: str, alt: str = None):
        self.add(Img(source, alt))
        return self

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

    def add_source(self, source: str, type: str):
        self.add(Source(source, type))
        return self

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

    def add_source(self, source: str, type: str):
        self.add(Source(source, type))
        return self

"""
Heading 1
"""
class H1(Tag):
    def __init__(self, *content: str|Tag): 
        super().__init__("h1")
        self.add(*content)

"""
Heading 2
"""
class H2(Tag):
    def __init__(self, *content: str|Tag): 
        super().__init__("h2")
        self.add(*content)

"""
Heading 3
"""
class H3(Tag):
    def __init__(self, *content: str|Tag): 
        super().__init__("h3")
        self.add(*content)

"""
Heading 4
"""
class H4(Tag):
    def __init__(self, *content: str|Tag): 
        super().__init__("h4")
        self.add(*content)

"""
Heading 5
"""
class H5(Tag):
    def __init__(self, *content: str|Tag): 
        super().__init__("h5")
        self.add(*content)

"""
Heading 6
"""
class H6(Tag):
    def __init__(self, *content: str|Tag): 
        super().__init__("h6")
        self.add(*content)

"""
Used to define text tracks for Audio and Video
"""
class Track(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("track")

"""
Used to make text font one size smaller than document's base font size
"""
class Small(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("small")
        self.add(*content)

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
    def __init__(self, *content: str|Tag):
        super().__init__("p")
        self.add(*content)

"""
Provides an alternative content if a script type is not supported in browser
"""
class Noscript(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("noscript")
        self.add(*content)

"""
Used to define important text
"""
class Strong(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("strong")
        self.add(*content)

"""
Used to represent a text in some different voice
"""
class I(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("i")
        self.add(*content)

"""
Used to render enclosed text with an underline
"""
class U(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("u")
        self.add(*content)

"""
Used to make a text bold
"""
class B(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("b")
        self.add(*content)

"""
Used to emphasis the content applied within this element
"""
class Em(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("em")
        self.add(*content)

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
    def __init__(self, *content: str|Tag):
        super().__init__("sub")
        self.add(*content)

"""
Defines a text which displays as a superscript text
"""
class Sup(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("sup")
        self.add(*content)

"""
Defines ordered list of items
"""
class Ol(Tag):
    def __init__(self):
        super().__init__("ol")

    def add_item(self, *content: str|Tag):
        self.add(Li(*content))
        return self

"""
Defines unordered list of items
"""
class Ul(Tag):
    def __init__(self):
        super().__init__("ul")

    def add_item(self, *content: str|Tag):
        self.add(Li(*content))
        return self

"""
Used to represent items in list
"""
class Li(Tag):
    def __init__(self, *content: str|Tag):
        super().__init__("li")
        self.add(*content)

"""
Used to insert an image within an HTML document
"""
class Img(Tag):
    def __init__(self, src: str, alt: str = None):
        super().__init__("img")
        self.nobody = True
        self.set("src", src)
        if alt: self.set("alt", alt)

"""
Comments are not displayed in the browsers but they're visible in the source code
"""
class Comment(Tag):
    def __init__(self, comment: str):
        super().__init__(None)
        self.set_text(comment)
        self.before = "<!-- "
        self.after = " -->"