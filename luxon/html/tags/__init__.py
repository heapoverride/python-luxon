from __future__ import annotations
from luxon.html import *

class Html(Tag):
    """Represents the root (top-level element) of an HTML document"""
    def __init__(self):
        """Construct a Html element"""
        super().__init__("html")
        self.before = "<!DOCTYPE html>\n"

class Head(Tag):
    """Defines the head section of an HTML document"""
    def __init__(self):
        """Construct a Head element"""
        super().__init__("head")

class Title(Tag):
    """Defines the title or name of an HTML document"""
    def __init__(self, title: str|Text = None):
        """Construct a Title element"""
        super().__init__("title")
        if title: self.add(title)

class Meta(Tag):
    """Defines the metadata of an HTML document"""
    def __init__(self):
        """Construct a Meta element"""
        super().__init__("meta")

class Style(Tag):
    """Defines the style information for an HTML document"""
    def __init__(self, source: str = None):
        """Construct a Style element\n
        If source is provided, this element will produce a `<link>` tag instead of `<style>` tag

        Args:
            source (str, optional): Source stylesheet to link. Defaults to None.
        """
        if source:
            super().__init__("link")
            self.nobody = True
            self.set("rel", "stylesheet")
            self.set("href", source)
        else:
            super().__init__("style")

    def add_style(self, css_text: str):
        """Add CSS text

        Args:
            css_text (str): CSS text

        Returns:
            self
        """
        if self.name != "style": return self

        css_text = Text(css_text)
        css_text.escape = False
        self.add(css_text)
        return self

class Link(Tag):
    """Represents a relationship between current document and an external resource"""
    def __init__(self, relation: str, target: str, media_type: str = None):
        """Construct a Link element
        
        Args:
            relation (str): Specifies the relationship between the current document and the linked document
            target (str): Specifies the location of the linked document
            media_type (str): Specifies the media type of the linked document
        """
        super().__init__("link")
        self.nobody = True
        self.set("rel", relation)
        self.set("href", target)
        if media_type: self.set("type", media_type)

class Body(Tag):
    """Defines the body section of an HTML document"""
    def __init__(self):
        """Construct a Body element"""
        super().__init__("body")

class Header(Tag):
    """Defines the header of a section or webpage"""
    def __init__(self):
        """Construct a Header element"""
        super().__init__("header")

class Main(Tag):
    """Represents the main content of an HTML document"""
    def __init__(self):
        """Construct a Main element"""
        super().__init__("main")

class Footer(Tag):
    """Defines the footer section of a webpage"""
    def __init__(self):
        """Construct a Footer element"""
        super().__init__("footer")

class Span(Tag):
    """Used for styling and grouping inline"""
    def __init__(self, *content: str|Tag):
        """Construct a Span element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("span")
        self.add(*content)

class Div(Tag):
    """Defines a division or section within HTML document"""
    def __init__(self, *content: str|Tag):
        """Construct a Div element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("div")
        self.add(*content)

class Article(Tag):
    """Defines self-contained content"""
    def __init__(self, *content: str|Tag):
        """Construct an Article element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("article")
        self.add(*content)

class Aside(Tag):
    """Defines content aside from main content\n 
    Mainly represented as sidebar
    """
    def __init__(self):
        """Construct an Aside element"""
        super().__init__("aside")

class Details(Tag):
    """Defines additional details which user can either view or hide"""
    def __init__(self, *content: str|Tag):
        """Construct a Details element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("details")
        self.add(*content)

class Figcaption(Tag):
    """Used to add a caption or explanation for the Figure element"""
    def __init__(self, *content: str|Tag):
        """Construct a Figcaption element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("figcaption")
        self.add(*content)

class Caption(Tag):
    """Used to define a caption for a table"""
    def __init__(self, *content: str|Tag):
        """Construct a Caption element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("caption")
        self.add(*content)

class Cite(Tag):
    """Used to define the title of the work, book, website etc."""
    def __init__(self, *content: str|Tag):
        """Construct a Cite element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("cite")
        self.add(*content)

class Figure(Tag):
    """Used to define the self-contained content"""
    def __init__(self):
        """Construct a Figure element"""
        super().__init__("figure")

class Mark(Tag):
    """Represents a highlighted text"""
    def __init__(self, *content: str|Tag):
        """Construct a Mark element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("mark")
        self.add(*content)

class Nav(Tag):
    """Represents section of page to represent navigation links"""
    def __init__(self):
        """Construct a Nav element"""
        super().__init__("nav")

class Section(Tag):
    """Defines a generic section for a document"""
    def __init__(self):
        """Construct a Section element"""
        super().__init__("section")

class Summary(Tag):
    """Defines summary which can be used with Details"""
    def __init__(self, *content: str|Tag):
        """Construct a Summary element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("summary")
        self.add(*content)

class Time(Tag):
    """Define date/time within an HTML document"""
    def __init__(self, *content: str|Tag):
        """Construct a Time element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("time")
        self.add(*content)

class A(Tag):
    """Creates a hyperlink or link"""
    def __init__(self, text: str|Tag, target: str, new_window: bool = False):
        """Construct an A (hyperlink) element
        
        Args:
            text (str|Tag): Hyperlink body
            target (str): Specifies the URL of the page the link goes to
        """
        super().__init__("a")
        self.add(text)
        self.set("href", target)
        if new_window:
            self.set("target", "_blank")

class Area(Tag):
    """Defines the area of an image map"""
    def __init__(self):
        """Construct a Area element"""
        super().__init__("area")

class Blockquote(Tag):
    """Used to define a content which is taken from another source"""
    def __init__(self, *content: str|Tag):
        """Construct a Blockquote element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("blockquote")
        self.add(*content)

class Br(Tag):
    """Produces a line break in text (carriage-return)"""
    def __init__(self):
        """Construct a Br element"""
        super().__init__("br")
        self.nobody = True

class Hr(Tag):
    """Produces a horizontal line"""
    def __init__(self):
        """Construct a Hr element"""
        super().__init__("hr")
        self.nobody = True

class Button(Tag):
    """Used to represent a clickable button"""
    def __init__(self, text: str|Tag):
        """Construct a Button element
        
        Args:
            text (str|Tag): Button body
        """
        super().__init__("button")
        self.add(text)

class Canvas(Tag):
    """Used to provide a graphics space within a web document"""
    def __init__(self):
        """Construct a Canvas element"""
        super().__init__("canvas")

class Code(Tag):
    """Used to display a part of programming code in an HTML document"""
    def __init__(self, *content: str|Tag):
        """Construct a Code element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("code")
        self.add(*content)

class Col(Tag):
    """Defines a column within a Table which represent common properties of columns and used with the Colgroup"""
    def __init__(self):
        """Construct a Col element"""
        super().__init__("col")

class Colgroup(Tag):
    """Used to define group of columns in a table"""
    def __init__(self):
        """Construct a Colgroup element"""
        super().__init__("colgroup")

class Data(Tag):
    """Used to link the content with the machine-readable translation"""
    def __init__(self):
        """Construct a Data element"""
        super().__init__("data")

class Datalist(Tag):
    """Used to provide a predefined list for input option"""
    def __init__(self):
        """Construct a Datalist element"""
        super().__init__("datalist")

class Dialog(Tag):
    """Defines a dialog box or other interactive components"""
    def __init__(self):
        """Construct a Dialog element"""
        super().__init__("dialog")

class Embed(Tag):
    """Used as embedded container for external file/application/media"""
    def __init__(self):
        """Construct an Embed element"""
        super().__init__("embed")

class Fieldset(Tag):
    """Used to group related elements/labels within a web form"""
    def __init__(self):
        """Construct a Fieldset element"""
        super().__init__("fieldset")

    def add_legend(self, *content: str|Tag):
        """Add a Legend to this Fieldset element

        Args:
            *content (str|Tag): Content

        Returns:
            self
        """
        self.add(Legend(*content))
        return self

class Legend(Tag):
    """Defines a caption for content of Fieldset"""
    def __init__(self, *content: str|Tag):
        """Construct a Legend element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("legend")
        self.add(*content)

class Form(Tag):
    """Used to define an HTML form"""
    def __init__(self, method: str = None, action: str = None, multipart: bool = False):
        """Construct a Form element

        Args:
            method (str, optional): HTTP method to use when submitting this form. Defaults to None (POST).
            action (str, optional): URI where the request will be sent. Defaults to None.
            multipart (bool, optional): Send multipart form data. Defaults to False.
        """
        super().__init__("form")
        if method == None:
            method = "POST"
        self.set("method", method.upper())
        
        if action: self.set("action", action)
        if multipart: self.set("enctype", "multipart/form-data")

class Input(Tag):
    """Defines an input field within an HTML form"""
    def __init__(self, type: str, id: str = None, name: str = None, value: str = None):
        """Construct a Input element
        
        Args:
            type (str): Input type
            id (str, optional): ID attribute. Defaults to None.
            name (str, optional): Name attribute. Defaults to None.
            value (str, optional): Value attribute. Defaults to None.
        """
        super().__init__("input")
        self.set("type", type.lower())
        self.nobody = True
        if id: self.set_id(id)
        if name: self.set_name(name)
        if value: self.set_value(value)

class Textarea(Tag):
    """Used to define multiple line input, such as comment, feedback, and review"""
    def __init__(self, id: str = None, name: str = None, width: int = None, height: int = None):
        """Construct a Textarea element
        
        Args:
            id (str, optional): ID attribute. Defaults to None.
            name (str, optional): Name attribute. Defaults to None.
            width (int, optional): Textarea width (characters). Defaults to None.
            height (int, optional): Textarea height (lines). Defaults to None.
        """
        super().__init__("textarea")
        if id: self.set_id(id)
        if name: self.set_name(name)
        if width: self.set("width", str(width))
        if height: self.set("height", str(height))

class Script(Tag):
    """Used to declare the JavaScript within HTML document"""
    def __init__(self, source: str = None):
        """Construct a Script element

        Args:
            source (str, optional): Source JavaScript file. Defaults to None.
        """
        super().__init__("script")
        if source: self.set("src", source)

    def add_code(self, code: str):
        """Add code to this Script element

        Args:
            code (str): Code. Most likely JavaScript.

        Returns:
            self
        """
        code = Text(code)
        code.escape = False
        self.add(code)
        return self

class Select(Tag):
    """Represents a control which provides a menu of options"""
    def __init__(self, id: str = None, name: str = None):
        """Construct a Select element
        
        Args:
            id (str, optional): ID attribute. Defaults to None.
            name (str, optional): Name attribute. Defaults to None.
        """
        super().__init__("select")
        if id: self.set_id(id)
        if name: self.set_name(name)

    def add_option(self, text: str, value: str = None, disabled: bool = False):
        """Add an Option to this Select element

        Args:
            text (str): Displayed text
            value (str, optional): Option value. Defaults to None.
            disabled (bool, optional): Disabled option. Defaults to False.

        Returns:
            self
        """
        self.add(Option(text, value, disabled=disabled))
        return self

class Option(Tag):
    """Used to define options or items in a drop-down list (Select)"""
    def __init__(self, text: str, value: str = None, disabled: bool = False):
        """Construct an Option element

        Args:
            text (str): Displayed text
            value (str, optional): Option value. Defaults to None.
            disabled (bool, optional): Disabled option. Defaults to False.
        """
        super().__init__("option")
        self.add(text)
        if value: self.set_value(value)
        if disabled: self.set("disabled")

class Iframe(Tag):
    """Defines an inline frame which can embed other content"""
    def __init__(self, source: str = None):
        """Construct an Iframe element

        Args:
            source (str, optional): Specifies the address of the document to embed. Defaults to None.
        """
        super().__init__("iframe")
        if source: self.set("src", source)

class Table(Tag):
    """Used to present data in tabular form or to create a table within HTML document"""
    def __init__(self):
        """Construct a Table element"""
        super().__init__("table")

    def add_header_row(self, *columns: str|Tag):
        """Add a header row to this Table element

        Args:
            *columns (str|Tag): Header columns

        Returns:
            self
        """
        self.add(Tr().add_headers(*columns))
        return self

    def add_row(self, *columns: str|Tag):
        """Add a row to this Table element

        Args:
            *columns (str|Tag): Columns

        Returns:
            self
        """
        self.add(Tr().add_columns(*columns))
        return self

    def add_thead(self, *rows: list[str|Tag]):
        """Add a head section with rows to this Table element

        Args:
            *rows (str|Tag): Table rows

        Returns:
            self
        """
        thead = Thead()
        for row in rows: 
            thead.add_row(*row)
        self.add(thead)
        return self

    def add_tbody(self, *rows: list[str|Tag]):
        """Add a body section with rows to this Table element

        Args:
            *rows (str|Tag): Table rows

        Returns:
            self
        """
        tbody = Tbody()
        for row in rows: 
            tbody.add_row(*row)
        self.add(tbody)
        return self

    def add_tfoot(self, *rows: list[str|Tag]):
        """Add a footer section with rows to this Table element

        Args:
            *rows (str|Tag): Table rows

        Returns:
            self
        """
        tfoot = Tfoot()
        for row in rows: 
            tfoot.add_row(*row)
        self.add(tfoot)
        return self

class Thead(Tag):
    """Defines the header of an HTML table\n 
    It is used along with Tbody and Tfoot"""
    def __init__(self):
        """Construct a Thead element"""
        super().__init__("thead")

    def add_row(self, *columns: str|Tag):
        """Add a row of columns to this table head section

        Args:
            *columns (str|Tag): Columns

        Returns:
            self
        """
        self.add(Tr().add_headers(*columns))
        return self

class Tbody(Tag):
    """Represents the body content of an HTML table and used along with Thead and Tfoot"""
    def __init__(self):
        """Construct a Tbody element"""
        super().__init__("tbody")

    def add_row(self, *columns: str|Tag):
        """Add a row of columns to this table body section

        Args:
            *columns (str|Tag): Columns

        Returns:
            self
        """
        self.add(Tr().add_columns(*columns))
        return self

class Tfoot(Tag):
    """Defines the footer content of an HTML table"""
    def __init__(self):
        """Construct a Tfoot element"""
        super().__init__("tfoot")

    def add_row(self, *columns: str|Tag):
        """Add a row of columns to this table footer section

        Args:
            *columns (str|Tag): Columns

        Returns:
            self
        """
        self.add(Tr().add_columns(*columns))
        return self

class Tr(Tag):
    """Defines the row cells in an HTML table"""
    def __init__(self):
        """Construct a Tr element"""
        super().__init__("tr")

    def add_headers(self, *columns: str|Tag):
        """Add header columns to this table row

        Args:
            *columns (str|Tag): Columns

        Returns:
            self
        """
        self.add([Th(x) for x in columns])
        return self

    def add_columns(self, *columns: str|Tag):
        """Add columns to this table row

        Args:
            *columns (str|Tag): Columns

        Returns:
            self
        """
        self.add([Td(x) for x in columns])
        return self

class Th(Tag):
    """Defines the head cell of an HTML table\n 
    Used with Thead"""
    def __init__(self, *content: str|Tag):
        """Construct a Th element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("th")
        self.add(*content)

class Td(Tag):
    """Used to define cells of an HTML table which contains table data"""
    def __init__(self, *content: str|Tag):
        """Construct a Td element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("td")
        self.add(*content)

class Source(Tag):
    """Defines multiple media recourses for different media element such as Picture, Video, and Audio"""
    def __init__(self, source: str|list[str], mime_type: str = None, media_query: str = None):
        """Construct a Source element

        Args:
            source (str | list[str]): Source or list of sources to include
            mime_type (str, optional): Specifies the MIME-type of the resource. Defaults to None.
            media_query (str, optional): Accepts any valid media query that would normally be defined in CSS. Defaults to None.
        """
        super().__init__("source")
        self.nobody = True

        if type(source) == str:
            self.set("src", source)
        elif type(source) == list:
            self.set("srcset", ",".join(source))

        if mime_type: self.set("type", mime_type)
        if media_query: self.set("media", media_query)

class Picture(Tag):
    """Defines more than one source elements and one image element"""
    def __init__(self):
        """Construct a Picture element"""
        super().__init__("picture")

    def add_source(self, sources: list[str], media_query: str):
        """Add source or source list to this picture element

        Args:
            sources (list[str]): Source or list of sources to include
            media_query (str): Accepts any valid media query that would normally be defined in CSS

        Returns:
            self
        """
        self.add(Source(sources, media_query=media_query))
        return self

    def add_image(self, source: str, alt: str = None):
        """Add an image to this picture element

        Args:
            source (str): Specifies the path to the image
            alt (str, optional): Specifies an alternate text for an image. Defaults to None.

        Returns:
            self
        """
        self.add(Img(source, alt))
        return self

class Audio(Tag):
    """Used to embed audio content in HTML document"""
    def __init__(self, source: str = None, autoplay: bool = False, controls: bool = False, loop: bool = False, muted: bool = False, preload: str = None):
        """Construct an Audio element

        Args:
            source (str, optional): Specifies the URL of the audio file. Defaults to None.
            autoplay (bool, optional): Specifies that the audio will start playing as soon as it is ready. Defaults to False.
            controls (bool, optional): Specifies that audio controls should be displayed. Defaults to False.
            loop (bool, optional): Specifies that the audio will start over again, every time it is finished. Defaults to False.
            muted (bool, optional): Specifies that the audio output should be muted. Defaults to False.
            preload (str, optional): Specifies if and how the audio should be loaded when the page loads. Defaults to None.
        """
        super().__init__("audio")
        if source: self.set("src", source)
        if autoplay: self.set("autoplay", True)
        if controls: self.set("controls", True)
        if loop: self.set("loop", True)
        if muted: self.set("muted", True)
        if preload: self.set("preload", preload)

    def add_source(self, source: str, mime_type: str):
        """Add source to this audio element

        Args:
            source (str): Source to include
            mime_type (str): Specifies the MIME-type of the resource. Defaults to None.

        Returns:
            self
        """
        self.add(Source(source, mime_type))
        return self

class Video(Tag):
    """Used to embed a video content with an HTML document"""
    def __init__(self, source: str = None, width: int = None, height: int = None, poster: str = None, autoplay: bool = False, controls: bool = False, loop: bool = False, muted: bool = False, preload: str = None):
        """Construct a Video element

        Args:
            source (str, optional): Specifies the URL of the video file. Defaults to None.
            width (int, optional): Sets the width of the video player. Defaults to None.
            height (int, optional): Sets the height of the video player. Defaults to None.
            poster (str, optional): Specifies an image to be shown while the video is downloading, or until the user hits the play button. Defaults to None.
            autoplay (bool, optional): Specifies that the video will start playing as soon as it is ready. Defaults to False.
            controls (bool, optional): Specifies that video controls should be displayed. Defaults to False.
            loop (bool, optional): Specifies that the video will start over again, every time it is finished. Defaults to False.
            muted (bool, optional): Specifies that the audio output of the video should be muted. Defaults to False.
            preload (str, optional): Specifies if and how the author thinks the video should be loaded when the page loads. Defaults to None.
        """
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
        """Add source to this video element

        Args:
            source (str): Source to include
            mime_type (str): Specifies the MIME-type of the resource. Defaults to None.

        Returns:
            self
        """
        self.add(Source(source, type))
        return self

class H1(Tag):
    """Heading 1"""
    def __init__(self, *content: str|Tag): 
        """Construct a H1 element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("h1")
        self.add(*content)

class H2(Tag):
    """Heading 2"""
    def __init__(self, *content: str|Tag): 
        """Construct a H2 element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("h2")
        self.add(*content)

class H3(Tag):
    """Heading 3"""
    def __init__(self, *content: str|Tag): 
        """Construct a H3 element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("h3")
        self.add(*content)

class H4(Tag):
    """Heading 4"""
    def __init__(self, *content: str|Tag): 
        """Construct a H4 element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("h4")
        self.add(*content)

class H5(Tag):
    """Heading 5"""
    def __init__(self, *content: str|Tag): 
        """Construct a H5 element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("h5")
        self.add(*content)
        
class H6(Tag):
    """Heading 6"""
    def __init__(self, *content: str|Tag): 
        """Construct a H6 element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("h6")
        self.add(*content)

class Track(Tag):
    """Used to define text tracks for Audio and Video"""
    def __init__(self, source: str, kind: str, lang: str, label: str):
        """Construct a Track element

        Args:
            source (str): Specifies the URL of the track file
            kind (str): Specifies the kind of text track (e.g. subtitles)
            lang (str): Specifies the language of the track text data (required if kind="subtitles")
            label (str): Specifies the title of the text track
        """
        super().__init__("track")
        if source: self.set("src", source)
        if kind: self.set("kind", kind)
        if lang: self.set("srclang", lang)
        if label: self.set("label", label)

class Small(Tag):
    """Used to make text font one size smaller than document's base font size"""
    def __init__(self, *content: str|Tag):
        """Construct a Small element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("small")
        self.add(*content)

class Pre(Tag):
    """Defines preformatted text in an HTML document"""
    def __init__(self, text: str):
        """Construct a Pre element
        
        Args:
            text (str): Preformatted text
        """
        super().__init__("pre")
        self.add(text)

class P(Tag):
    """Represents a paragraph in an HTML document"""
    def __init__(self, *content: str|Tag):
        """Construct a P element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("p")
        self.add(*content)

class Noscript(Tag):
    """Provides an alternative content if a script type is not supported in browser"""
    def __init__(self, *content: str|Tag):
        """Construct a Noscript element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("noscript")
        self.add(*content)

class Strong(Tag):
    """Used to define important text"""
    def __init__(self, *content: str|Tag):
        """Construct a Strong element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("strong")
        self.add(*content)

class I(Tag):
    """Used to represent a text in some different voice"""
    def __init__(self, *content: str|Tag):
        """Construct an I element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("i")
        self.add(*content)

class U(Tag):
    """Used to render enclosed text with an underline"""
    def __init__(self, *content: str|Tag):
        """Construct an U element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("u")
        self.add(*content)

class B(Tag):
    """Used to make a text bold"""
    def __init__(self, *content: str|Tag):
        """Construct a B element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("b")
        self.add(*content)

class Em(Tag):
    """Used to emphasis the content applied within this element"""
    def __init__(self, *content: str|Tag):
        """Construct an Em element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("em")
        self.add(*content)

class Label(Tag):
    """Defines a text label for Input of Form"""
    def __init__(self, text: str, for_id: str = None):
        """Construct a Label element

        Args:
            text (str): Label text
            for_id (str, optional): ID of the element this label is associated with. Defaults to None.
        """
        super().__init__("label")
        if text: self.add(text)
        if for_id: self.set("for", for_id)

class Sub(Tag):
    """Defines a text which displays as a subscript text"""
    def __init__(self, *content: str|Tag):
        """Construct a Sub element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("sub")
        self.add(*content)

class Sup(Tag):
    """Defines a text which displays as a superscript text"""
    def __init__(self, *content: str|Tag):
        """Construct a Sup element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("sup")
        self.add(*content)

class Ol(Tag):
    """Defines ordered list of items"""
    def __init__(self, *items: str|Tag):
        """Construct an Ol element

        Args:
            *items (str|Tag): List items
        """
        super().__init__("ol")
        self.add(*[Li(x) for x in items])

    def add_item(self, *content: str|Tag):
        """Add an item to this ordered list

        Args:
            *content (str|Tag): Content

        Returns:
            self
        """
        self.add(Li(*content))
        return self

class Ul(Tag):
    """Defines unordered list of items"""
    def __init__(self, *items: str|Tag):
        """Construct an Ul element

        Args:
            *items (str|Tag): List items
        """
        super().__init__("ul")
        self.add(*[Li(x) for x in items])

    def add_item(self, *content: str|Tag):
        """Add an item to this unordered list

        Args:
            *content (str|Tag): Content

        Returns:
            self
        """
        self.add(Li(*content))
        return self

class Li(Tag):
    """Used to represent items in list"""
    def __init__(self, *content: str|Tag):
        """Construct a Li element
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__("li")
        self.add(*content)

class Img(Tag):
    """Used to insert an image within an HTML document"""
    def __init__(self, src: str, alt: str = None):
        """Construct an Img element

        Args:
            src (str): Specifies the path to the image
            alt (str, optional): Specifies an alternate text for an image. Defaults to None.
        """
        super().__init__("img")
        self.nobody = True
        self.set("src", src)
        if alt: self.set("alt", alt)

class Comment(Tag):
    """Comments are not displayed in the browsers but they're visible in the source code"""
    def __init__(self, comment: str):
        """Construct a Comment element

        Args:
            comment (str): Comment
        """
        super().__init__(None)
        self.set_text(comment)
        self.before = "<!-- "
        self.after = " -->"