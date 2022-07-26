from enum import IntEnum
from luxon.html.tags import *

class Parser:
    @staticmethod
    def __parse(html: str, begin: int = None, end: int = None) -> Tag|list[Tag]:
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

        opens: list[tuple(int, int)] = []
        closes: list[tuple(int, int)] = []
        matches: list[tuple[tuple[int,int],tuple[int,int]]] = []

        state: Parser.State = Parser.State.TEXT
        stack: list[Tag|str|int] = []
        tags: list[Tag] = []
        temp: str = ""
        tag: Tag = None

        # Parser logic
        pos = begin
        while pos < end:
            if state == Parser.State.TEXT:
                # Text content
                if html[pos] == "<":
                    # Add text element
                    if pos < end-1 and html[pos+1] == "/":
                        # Close tag begins
                        closes.append((pos, -1))
                        pos += 1
                        state = Parser.State.TAG_CLOSE

                        # Add text element (we know a tag is set because this is is a close tag)
                        if temp != "":
                            text = Text(temp)
                            temp = ""
                            tag.add(text)
                    else:
                        # Open tag begins
                        opens.append((pos, -1))
                        state = Parser.State.TAG_OPEN

                        # Add text element to parent element or tags
                        if temp != "":
                            text = Text(temp)
                            temp = ""
                            if tag != None:
                                tag.add(text)
                            else:
                                tags.append(text)

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

                        if tag.nobody:
                            matches.append(((open_begin, pos), (-1, pos)))
                            tags.append(tag)
                        else:
                            opens.append((open_begin, pos))

                        stack.append((open_begin, tag))
                        state = Parser.State.TEXT
                else:
                    # Build tag name
                    temp += html[pos]

            elif state == Parser.State.TAG_ATT:
                if html[pos] in ("/", ">"):
                    # Attribute ends
                    pos -= 1
                    state = Parser.State.TAG_OPEN

            elif state == Parser.State.TAG_CLOSE:
                # Close tag
                if html[pos] == ">":
                    # Close tag ends
                    open_begin, open_tag = stack.pop()
                    tag = open_tag
                    close_begin = closes.pop()[0]
                    matches.append((opens.pop(), (close_begin, pos)))
                    
                    if len(stack) == 0:
                        # Has no parent tag
                        tags.append(open_tag)
                    else:
                        # Has parent tag
                        stack[-1][1].add(tag)

                    state = Parser.State.TEXT

            # Show debug help
            #print(f"{pos}:  symbol={repr(html[pos])}  state={state.name}  tag={type(tag)}")
            #print(stack)

            # Advance position
            pos += 1

        # Check for errors (stack should be empty here)
        if len(stack) != 0:
            raise Exception("Invalid HTML source code")

        # Check if we have remaining text in temp 
        # and if we do, we add new text node
        if temp != "":
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