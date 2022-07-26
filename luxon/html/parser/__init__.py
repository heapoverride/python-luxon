from enum import IntEnum
from luxon.html.tags import *

class Parser:
    def __parse(html: str, 
        matches: tuple[tuple[tuple[int,int],tuple[int,int]]],
        begin: int = None, end: int = None, 
        parent: Tag = None) -> Tag|list[Tag]:
        """Parse HTML source code and return a tag or list of tags

        Args:
            html (str): HTML source code
            begin (int, optional): Begin index
            end (int, optional): End index

        Raises:
            Exception: Invalid HTML source code

        Returns:
            Tag|list[Tag]: Tag or list of tags
        """
        if not begin: begin = 0
        if not end: end = len(html)

        state: Parser.State = Parser.State.TEXT
        opens: list[tuple[int, int]] = [] # For storing encountered open tag positions
        closes: list[tuple[int, int]] = [] # For storing encountered close tag positions
        stack: list[Tag] = [] # For storing data
        tags: list[Tag] = []
        temp: str = ""
        tag: Tag = None

        # Parser logic
        pos = begin
        while pos < end:
            # debug help
            print(type(parent), repr(html[pos]), state, stack, opens)

            if state == Parser.State.TEXT:
                # Handle text
                if html[pos] == "<":
                    # Open or close tag begins
                    if pos < end-1 and html[pos+1] != "/":
                        # Open tag begins
                        opens.append((pos, -1))
                        state = Parser.State.TAG_OPEN
                    else:
                        # Close tag begins
                        closes.append((pos, -1))
                        state = Parser.State.TAG_CLOSE
                        pos += 1
                else:
                    # Build text
                    temp += html[pos]

            elif state == Parser.State.TAG_OPEN:
                # Read tag name
                if html[pos] in (" ", "/", ">"):
                    # Tag name ends
                    if temp != "":
                        tag = Parser.__create_tag(temp)
                        temp = ""

                    if html[pos] == "/":
                        # Tag has no body
                        tag.nobody = True
                        opens.pop()

                    elif html[pos] == ">":
                        # Open tag ends
                        if tag.nobody == False:
                            opens.append((opens.pop()[0], pos))
                        tags.append(tag)
                        state = Parser.State.TEXT
                else:
                    # Build tag name
                    temp += html[pos]

            elif state == Parser.State.TAG_CLOSE:
                # Read tag name
                if html[pos] == ">":
                    # Tag name ends
                    # TODO: Do something with tag name
                    closes.append((closes.pop()[0], pos))
                    temp = ""

                    # Recursively parse child elements
                    # TODO: We should properly check for close tag
                    # and we must perform some checks for <script> and <style> tags
                    # to prevent issues with "<>" characters in embedded CSS or JavaScript
                    #tag.add(Parser.__parse(html, begin=body_begin, end=pos+1, parent=tag))
                    open_end = opens.pop()[1]
                    close_begin = closes.pop()[0]

                    if len(opens) == 0 and len(closes) == 0:
                        tag.add(Parser.__parse(html, matches, 
                            begin=open_end+1, end=close_begin, 
                            parent=tag))

                    state = Parser.State.TEXT
                else:
                    # Build tag name
                    temp += html[pos]

            # Advance position
            pos += 1

        # Check for errors
        if len(stack) != 0:
            raise Exception("Invalid HTML source code")

        # Check if we have remaining text in temp 
        # and if we do, we add new text node
        if temp.strip(" \t\n\r") != "":
            text = Text(temp)
            tags.append(text)

        # Return a single tag or list of tags
        # depending on how many tags were parsed
        return tags[0] if len(tags) == 1 else tags

    @staticmethod
    def parse(html: str):
        """Parse HTML source code and return a tag or list of tags

        Args:
            html (str): HTML source code

        Returns:
            Tag|list[Tag]: Tag or list of tags
        """
        matches = Parser.__match(html)
        print(matches) # debug
        #return Parser.__parse(str(html), matches)

    @staticmethod
    def __match(html: str, begin: int = None, end: int = None) -> tuple[tuple[tuple[int,int],tuple[int,int]]]:
        """Find open and close tags and their start and end positions.
        This should only be called once for every parse()

        Args:
            html (str): HTML source code

        Returns:
            tuple[tuple[tuple[int,int],tuple[int,int]]]: Matches
        """
        if not begin: begin = 0
        if not end: end = len(html)

        state: Parser.State = Parser.State.TEXT
        opens: list[tuple(int, int)] = []
        closes: list[tuple(int, int)] = []
        matches: list[tuple[tuple[int,int],tuple[int,int]]] = []
        nobody: bool = False

        pos = begin
        while pos < end:
            # Debug
            #print(f"{pos}: {repr(html[pos])} {state.name}")

            if state == Parser.State.TEXT:
                # Text content
                if html[pos] == "<":
                    if pos < end-1 and html[pos+1] == "/":
                        # Close tag begins
                        closes.append((pos, -1))
                        pos += 1
                        state = Parser.State.TAG_CLOSE
                    else:
                        # Open tag begins
                        opens.append((pos, -1))
                        state = Parser.State.TAG_OPEN
            
            elif state == Parser.State.TAG_OPEN:
                # Open tag
                if html[pos] in (" ", "/", ">"):
                    # Tag name ends
                    if html[pos] == " ":
                        # Attribute begins
                        state = Parser.State.TAG_ATT
                    elif html[pos] == "/":
                        # Tag ends without body
                        nobody = True
                    elif html[pos] == ">":
                        # Open tag ends
                        open_begin = opens.pop()[0]
                        
                        if nobody:
                            matches.append(((open_begin, pos), (-1, pos)))
                        else:
                            opens.append((open_begin, pos))

                        state = Parser.State.TEXT

            elif state == Parser.State.TAG_ATT:
                if html[pos] in ("/", ">"):
                    # Attribute ends
                    pos -= 1
                    state = Parser.State.TAG_OPEN

            elif state == Parser.State.TAG_CLOSE:
                # Close tag
                if html[pos] == ">":
                    # Close tag ends
                    close_begin = closes.pop()[0]
                    matches.append((opens.pop(), (close_begin, pos)))
                    state = Parser.State.TEXT

            # Advance position
            pos += 1

        return tuple(matches)

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