from enum import IntEnum
from luxon.html.tags import *
from html import unescape
import re

class Parser:
    @staticmethod
    def __parse(html: str, begin: int = None, end: int = None) -> Tag:
        """Parse HTML source code

        Args:
            html (str): HTML source code
            begin (int, optional): Begin index
            end (int, optional): End index

        Raises:
            Exception: Invalid HTML source code

        Returns:
            Tag
        """
        if not begin: begin = 0
        if not end: end = len(html)

        opens: list[tuple(int,int)] = []
        closes: list[tuple(int,int)] = []
        matches: list[tuple[tuple[int,int],tuple[int,int]]] = []

        state: Parser.State = Parser.State.TEXT
        stack: list[Tag|tuple[int,Tag]|str|int] = []
        tags: list[Tag] = []
        temp: str = ""
        tag: Tag = None

        # These tags must not have a body
        void_tags = (
            "area", "base", "br", "col", "command", "embed", "hr", "img", "input", 
            "keygen", "link", "meta", "param", "source", "track", "wbr")

        # Parser logic
        pos = begin
        while pos < end:
            if state == Parser.State.TEXT:
                # Text content
                if html[pos] == "<":
                    if pos < end-1 and html[pos+1] == "/":
                        # Close tag begins
                        closes.append((pos, -1))
                        pos += 1
                        state = Parser.State.TAG_CLOSE
                    elif pos < end-1 and html[pos+1] == "!":
                        if pos < end-3 and html[pos+2] == "-" and html[pos+3] == "-": # '<!--'
                            # Comment begins
                            state = Parser.State.COMMENT
                            pos += 3
                        else:
                            # Doctype declaration begins
                            state = Parser.State.DOCTYPE
                            pos += 1
                    else:
                        # Open tag begins
                        opens.append((pos, -1))
                        state = Parser.State.TAG_OPEN

                    # Add text element to parent element or tags
                    if state != Parser.State.TEXT and temp != "":
                        if temp.strip(" \t\n\r") != "":
                            text = Parser.__create_text(temp, parent=tag)
                            if tag != None:
                                tag.add(text)
                            else:
                                tags.append(text)

                        temp = ""
                else:
                    # Build text content
                    temp += html[pos]
            
            elif state == Parser.State.TAG_OPEN:
                # Open tag
                if html[pos] in (" ", "/", ">"):
                    # Tag name ends
                    if temp != "":
                        tag = Parser.__create_tag(temp)
                        temp = ""

                    if html[pos] == " ":
                        # Attribute begins
                        state = Parser.State.TAG_ATT
                    elif html[pos] == "/":
                        # Tag ends without body
                        tag.nobody = True
                    elif html[pos] == ">":
                        # Open tag ends
                        open_begin = opens.pop()[0]
                        state = Parser.State.TEXT

                        if tag.tagname in void_tags:
                            # Void tags must not have a body
                            tag.nobody = True

                        if tag.nobody:
                            # Has no body
                            matches.append(((open_begin, pos), (-1, pos)))
                            
                            parent: Tag = None
                            if len(stack) != 0:
                                parent = stack[-1][1]

                            if parent != None:
                                parent.add(tag)
                            else:
                                tags.append(tag)

                            tag = parent
                        else:
                            # Has body
                            opens.append((open_begin, pos))
                            stack.append((open_begin, tag))

                            if type(tag) in (Style, Script):
                                # Do not parse <style> and <script> element bodies
                                state = Parser.State.NO_PARSE
                else:
                    # Build tag name
                    if html[pos].isalnum():
                        temp += html[pos]

            elif state == Parser.State.TAG_ATT:
                if html[pos] in (" ", "=", "/", ">"):
                    # Attribute ends
                    if html[pos] == "=":
                        # Attribute value begins
                        stack.append(temp)
                        temp = ""
                        state = Parser.State.TAG_ATT_VALUE
                    else:
                        # Open tag ends
                        pos -= 1
                        state = Parser.State.TAG_OPEN

                        # Set attribute
                        if temp != "":
                            tag.set(temp)
                            temp = ""
                else:
                    # Build attribute name
                    if html[pos].isalnum() or html[pos] == "-":
                        temp += html[pos]

            elif state == Parser.State.TAG_ATT_VALUE:
                # Attribute value
                if html[pos] in (" ", "/", ">"):
                    # Attribute value ends
                    tag.set(stack.pop(), temp)
                    temp = ""
                    pos -= 1
                    state = Parser.State.TAG_ATT
                elif html[pos] in ("\"", "'"):
                    # Attribute value in quotes
                    pos -= 1
                    state = Parser.State.TAG_ATT_VALUE_QUOTED
                else:
                    # Build attribute value
                    if html[pos].isalnum():
                        temp += html[pos]

            elif state == Parser.State.TAG_ATT_VALUE_QUOTED:
                # Attribute value in quotes
                quote = html[pos]
                pos += 1

                while html[pos] != quote:
                    temp += html[pos]
                    pos += 1
                
                tag.set(stack.pop(), temp)
                temp = ""
                state = Parser.State.TAG_ATT

            elif state == Parser.State.TAG_CLOSE:
                # Close tag
                if html[pos] == ">":
                    # Close tag ends (ignore if tag not set)
                    if tag != None:
                        open_begin, open_tag = stack.pop()
                        close_begin = closes.pop()[0]
                        matches.append((opens.pop(), (close_begin, pos)))

                        parent: Tag = None
                        if len(stack) != 0:
                            parent = stack[-1][1]

                        if parent != None:
                            parent.add(tag)
                        else:
                            tags.append(tag)

                        tag = parent

                    state = Parser.State.TEXT

            elif state == Parser.State.DOCTYPE:
                # We don't care about doctype at this point
                if html[pos] == ">":
                    # Doctype declaration ends
                    state = Parser.State.TEXT

            elif state == Parser.State.COMMENT:
                # Comment
                if pos < end-2 and html[pos:pos+3] == "-->":
                    # Comment ends
                    if temp != "":
                        comment = Comment(temp.strip())
                        comment.escape = False # Don't escape text in comments
                        temp = ""
                        if tag != None:
                            tag.add(comment)
                        else:
                            tags.append(comment)

                    state = Parser.State.TEXT
                    pos += 2
                else:
                    # Build comment
                    temp += html[pos]

            elif state == Parser.State.NO_PARSE:
                # No parse
                close_tag = f"</{tag.tagname}>"

                if pos < end+len(close_tag)+1 and html[pos:pos+len(close_tag)] == close_tag:
                    # Matching closing tag and add text
                    text = Text(temp)
                    text.escape = False
                    temp = ""
                    tag.add(text)
                    pos -= 1
                    state = Parser.State.TEXT
                else:
                    temp += html[pos]

            # Show debug help
            #print(f"\n{pos}:  symbol={repr(html[pos])}  state={state.name}  tag={type(tag)}")
            #print(stack)

            # Advance position
            pos += 1

        # Check for errors (stack should be empty here)
        if len(stack) != 0:
            raise Exception("Invalid HTML source code")

        # Check if we have remaining text in temp 
        # and if we do, we add new text node
        if temp != "" and temp.strip(" \t\n\r") != "":
            tags.append(Parser.__create_text(temp, parent=tag))

        return tags[0] if len(tags) == 1 else Root(*tags)

    @staticmethod
    def parse(html: str) -> Tag:
        """Parse HTML source code

        Args:
            html (str): HTML source code

        Raises:
            Exception: Invalid HTML source code

        Returns:
            Tag
        """
        return Parser.__parse(str(html))

    class State(IntEnum):
        TEXT = 0
        DOCTYPE = 1
        COMMENT = 2
        TAG_OPEN = 3
        TAG_ATT = 4
        TAG_ATT_VALUE = 5
        TAG_ATT_VALUE_QUOTED = 6
        TAG_BODY = 7
        TAG_CLOSE = 8
        NO_PARSE = 9

    @staticmethod
    def __find(func: Callable[[tuple[tuple[int,int],tuple[int,int]]], bool],
        matches: list[tuple[tuple[int,int],tuple[int,int]]]) -> tuple[tuple[int,int],tuple[int,int]]|None:
        """Find a match from list of matches

        Args:
            func (Callable[[tuple[tuple[int,int],tuple[int,int]]], bool]): Lambda expression or named function
            matches (list[tuple[tuple[int,int],tuple[int,int]]]): List of matches

        Returns:
            tuple[tuple[int,int],tuple[int,int]]|None: Found match or None
        """
        for match in matches:
            # match = ((open_begin, open_end), (close_begin, close_end))
            if func(match): return match

        return None

    @staticmethod
    def __get_known_type(tagname: str) -> type|None:
        """Return a known type from tag name

        Args:
            tagname (str): Tag name

        Returns:
            type
        """
        match tagname.lower():
            case "html": return Html
            case "head": return Head
            case "title": return Title
            case "meta": return Meta
            case "style": return Style
            case "link": return Link
            case "body": return Body
            case "header": return Header
            case "main": return Main
            case "footer": return Footer
            case "span": return Span
            case "div": return Div
            case "article": return Article
            case "aside": return Aside
            case "details": return Details
            case "figcaption": return Figcaption
            case "caption": return Caption
            case "cite": return Cite
            case "figure": return Figure
            case "mark": return Mark
            case "nav": return Nav
            case "section": return Section
            case "summary": return Summary
            case "time": return Time
            case "a": return A
            case "area": return Area
            case "blockquote": return Blockquote
            case "br": return Br
            case "hr": return Hr
            case "button": return Button
            case "canvas": return Canvas
            case "code": return Code
            case "col": return Col
            case "colgroup": return Colgroup
            case "data": return Data
            case "datalist": return Datalist
            case "dialog": return Dialog
            case "embed": return Embed
            case "fieldset": return Fieldset
            case "legend": return Legend
            case "form": return Form
            case "input": return Input
            case "textarea": return Textarea
            case "script": return Script
            case "select": return Select
            case "option": return Option
            case "iframe": return Iframe
            case "table": return Table
            case "thead": return Thead
            case "tbody": return Tbody
            case "tfoot": return Tfoot
            case "tr": return Tr
            case "th": return Th
            case "td": return Td
            case "source": return Source
            case "picture": return Picture
            case "audio": return Audio
            case "video": return Video
            case "h1": return H1
            case "h2": return H2
            case "h3": return H3
            case "h4": return H4
            case "h5": return H5
            case "h6": return H6
            case "track": return Track
            case "small": return Small
            case "pre": return Pre
            case "p": return P
            case "noscript": return Noscript
            case "strong": return Strong
            case "i": return I
            case "u": return U
            case "b": return B
            case "em": return Em
            case "label": return Label
            case "sub": return Sub
            case "sup": return Sup
            case "ol": return Ol
            case "ul": return Ul
            case "li": return Li
            case "img": return Img

        return None

    @staticmethod
    def __trim(text: str):
        length = len(text)
        text = re.sub(TRIM_PATTERN, " ", text)

        if length != len(text):
            return Parser.__trim(text)

        return text

    @staticmethod
    def __create_text(text: str, parent: Tag = None):
        if type(parent) != Pre:
            text = Parser.__trim(text)

        return Text(unescape(text))

    @staticmethod
    def __create_tag(tagname: str):
        """Create an instance of known tag

        Args:
            tagname (str): Tag name

        Returns:
            Tag
        """
        known_type = Parser.__get_known_type(tagname)

        match tagname:
            case "html":
                return Html()

        tag = Tag(tagname)
        if known_type != None:
            tag.__class__ = known_type
        return tag

TRIM_PATTERN = re.compile(r"\s\s|\n|\r")