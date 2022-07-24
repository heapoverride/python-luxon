from enum import IntEnum
from luxon.html.tags import *

class Parser:
    @staticmethod
    def __match_tags(html: str) -> list[tuple[int, int]]:
        """Match opening (HTML) tags to their closing tags 
        and return matches as a tuple of tuples

        Args:
            html (str): HTML source code

        Raises:
            Exception: Invalid HTML source code

        Returns:
            tuple[tuple[int, int]]: Matches
        """
        matches: list[tuple[int, int]] = []
        stack = []
        i, length = 0, len(html)

        while i < length:
            # debug help
            #print(f"i={i} ({repr(html[i])})   length={length}   stack={stack}   matches={matches}")

            if html[i] == "<" and i < length-1 and html[i+1] not in ("!", "-"):
                if i < length-1 and html[i+1] == "/":
                    # closing tag
                    item = stack.pop()
                    item[1] = i
                    matches.append(tuple(item))
                    i += 1

                else:
                    # opening tag
                    stack.append([i, -1])

            elif html[i] == "/" and i < length-1 and html[i+1] == ">":
                # closing tag
                item = stack.pop()
                #item[1] = i
                matches.append(tuple(item))
                i += 1

            i += 1

        if len(stack) != 0:
            raise Exception("Invalid HTML source code")

        return matches

    @staticmethod
    def __find_closing_index(opening_index: int, matches: tuple[tuple[int, int]]) -> int:
        """Find closing tag's index from opening tag's index using matches from __match_tags method

        Args:
            opening_index (int): Opening tag's index
            matches (tuple[tuple[int, int]]): Matches from __match_tags method

        Returns:
            int: Closing tag's index (returns -1 if not found or if tag doesn't have a body)
        """
        for match in matches:
            if match[0] == opening_index:
                return match[1]

        return -1

    @staticmethod
    def __get_known_type(tagname: str) -> type:
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

        return Tag(tagname)

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
        tag.__class__ = known_type
        return tag
        

    class State(IntEnum):
        TEXT = 0
        DOCTYPE = 1
        COMMENT = 2
        TAG_NAME = 3
        TAG_ATT = 4
        TAG_ATT_VALUE = 5
        TAG_ATT_VALUE_QUOTED = 6
        TAG_BODY = 7
        TAG_CLOSE = 8

    @staticmethod
    def __parse(html: str, begin: int = None, end: int = None, matches: tuple[tuple[int, int]] = None) -> Tag|list[Tag]:
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
        if not matches: matches = Parser.__match_tags(html)

        state: Parser.State = Parser.State.TEXT
        stack: list[str|int] = []
        open_index: int = 0
        close_index: int = 0
        tags: list[Tag] = []
        temp: str = ""
        tag: Tag = None

        # Parser logic
        pos = begin
        while pos < end:
            if state == Parser.State.TEXT:
                if html[pos] == "<":
                    # Opening tag
                    temp = temp.strip()
                    if temp != "":
                        # Add text element
                        tags.append(Text(temp))
                        temp = ""
                        
                    if pos < end-1 and html[pos+1] == "!":
                        if pos < end-3 and html[pos+2] == "-" and html[pos+3] == "-":
                            pos += 3
                            state = Parser.State.COMMENT
                        else:
                            state = Parser.State.DOCTYPE
                    else:
                        close_index = Parser.__find_closing_index(pos, matches)
                        state = Parser.State.TAG_NAME
                else:
                    # Append text
                    temp += html[pos]

            elif state == Parser.State.DOCTYPE:
                if html[pos] == ">":
                    state = Parser.State.TEXT

            elif state == Parser.State.COMMENT:
                if html[pos] == "-" and pos < end-2 and html[pos+1] == "-" and html[pos+2] == ">":
                    # Add comment element
                    if temp != "":
                        tags.append(Comment(temp.strip()))
                        temp = ""

                    pos += 2
                    state = Parser.State.TEXT
                else:
                    temp += html[pos]

            elif state == Parser.State.TAG_NAME:
                if html[pos] in (" ", ">"):
                    # End of tag name
                    if temp != "":
                        tag = Parser.__create_tag(temp)
                        tags.append(tag)
                        temp = ""

                    if html[pos] == " ":
                        # Tag has attributes
                        state = Parser.State.TAG_ATT
                    elif html[pos] == ">":
                        # End of opening tag
                        state = Parser.State.TAG_BODY

                elif html[pos] == "/" and pos < end-1 and html[pos+1] == ">":
                    # End of tag
                    if temp != "":
                        tag = Parser.__create_tag(temp)
                        tags.append(tag)
                        temp = ""

                    # Tag doesn't have a body
                    tag.nobody = True

                    pos += 1
                    state = Parser.State.TEXT

                else:
                    # Append tag name
                    temp += html[pos]

            elif state == Parser.State.TAG_ATT:
                if html[pos] in ("/", ">"):
                    # End of attributes
                    if temp != "":
                        tag.set(temp)
                        temp = ""

                    pos -= 1
                    state = Parser.State.TAG_NAME

                elif html[pos] in (" ", "="):
                    # End of attribute name
                    if temp != "":
                        if html[pos] == " ":
                            tag.set(temp)
                            temp = ""
                            pos -= 1
                            state = Parser.State.TAG_ATT

                        elif html[pos] == "=":
                            stack.append(temp)
                            temp = ""
                            state = Parser.State.TAG_ATT_VALUE
                else:
                    temp += html[pos]

            elif state == Parser.State.TAG_ATT_VALUE:
                if html[pos] in ("\"", "'"):
                    # Beginning of a quoted value
                    pos -= 1
                    state = Parser.State.TAG_ATT_VALUE_QUOTED
                elif html[pos] in (" ", "/", ">"):
                    # End of attribute value
                    # Set attribute value
                    att_name = stack.pop().lower()

                    if att_name == "class":
                        tag.set_classes(*temp.split(" "))
                    else:
                        tag.set(att_name, temp)

                    temp = ""
                    pos -= 1
                    state = Parser.State.TAG_ATT
                else:
                    # Append attribute value
                    temp += html[pos]

            elif state == Parser.State.TAG_ATT_VALUE_QUOTED:
                quote = html[pos]
                pos += 1
                
                while pos < end:
                    if html[pos] != quote:
                        temp += html[pos]
                    else: break
                    pos += 1

                state = Parser.State.TAG_ATT_VALUE

            elif state == Parser.State.TAG_BODY:
                # Recursively parse child elements
                tag.add(Parser.__parse(html, begin=pos, end=close_index, matches=matches))
                pos = close_index - 1
                state = Parser.State.TAG_CLOSE

            elif state == Parser.State.TAG_CLOSE:
                if html[pos] == ">":
                    # End of closing tag
                    state = Parser.State.TEXT

            # Advance position
            pos += 1

        # Check for errors
        if len(stack) != 0:
            raise Exception("Invalid HTML source code")

        # Check if we have remaining text in temp 
        # and if we do, we add new text node
        temp = temp.strip()
        if temp != "":
            tags.append(Text(temp))

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