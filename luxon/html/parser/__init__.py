from enum import IntEnum
from luxon.html.tags import *

class Parser:
    class State(IntEnum):
        TEXT          = 0
        QUOTES        = 1
        TAG_OPEN      = 2
        TAG_CLOSE     = 3
        ATTRIBS       = 4
        ATTRIB_NAME   = 5
        ATTRIB_VALUE  = 6

    @staticmethod
    def __match_tags(html: str) -> tuple[tuple[int, int]]:
        """Match opening (HTML) tags to their closing tags 
        and return matches as a tuple of tuples

        Args:
            html (str): HTML source code

        Raises:
            Exception: Invalid HTML source code

        Returns:
            tuple[tuple[int, int]]: Matches
        """
        matches = []
        stack = []
        i, length = 0, len(html)

        while i < length:
            # debug help
            #print(f"i={i} ({repr(html[i])})   length={length}   stack={stack}   matches={matches}")

            if html[i] == "<":
                if i < len(html)-1 and html[i+1] == "/":
                    # closing tag
                    item = stack.pop()
                    item[1] = i
                    matches.append(item)
                    i += 1
                else:
                    # opening tag
                    stack.append([i, -1])
            elif html[i] == "/" and i < len(html)-1 and html[i+1] == ">":
                # closing tag
                item = stack.pop()
                #item[1] = i
                matches.append(item)
                i += 1

            i += 1

        if len(stack) != 0:
            raise Exception("Invalid HTML source code")

        return tuple(tuple(match) for match in matches)

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
    def __init_tag(tagname: str):
        """Construct a HTML element from tag name

        Args:
            tagname (str): Tag name

        Returns:
            Tag
        """
        match tagname.lower():
            case "i": return I()

        return Tag(tagname)

    @staticmethod
    def __parse(html: str, begin: int = None, end: int = None) -> Tag|list[Tag]|None:
        """Parse HTML source code and return a tag or list of tags

        Args:
            html (str): HTML source code
            begin (int, optional): Begin index
            end (int, optional): End index

        Returns:
            Tag|list[Tag]|None: Tag or list of tags or None
        """
        if not begin: begin = 0
        if not end: end = len(html)
        state: Parser.State = Parser.State.TEXT
        stack: list[str|int] = []
        tags: list[Tag] = []
        tag: Tag = None

        # Parser logic
        i = begin
        while i < end:
            pass

        # Return a single tag or list of tags
        # depending on how many tags were parsed
        length = len(tags)
        if length > 1: return tags
        if length == 1: return tags[0]
        return None

    @staticmethod
    def parse(html: str):
        """Parse HTML source code and return a tag or list of tags

        Args:
            html (str): HTML source code

        Returns:
            Tag|list[Tag]: Tag or list of tags
        """
        return Parser.__parse(html)