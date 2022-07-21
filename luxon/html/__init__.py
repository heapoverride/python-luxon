from __future__ import annotations
from typing import Any
from typing import Callable

# Base class for all HTML tags
class Tag:
    def __init__(self, name: str):
        self.name: str = name
        self.attributes: dict[str, str|True] = {}
        self.classes: list[str] = []
        self.styles: dict[str, str] = {}
        self.tags: list[Tag|str] = []
        self.text: str = None
        self.before: str = None
        self.after: str = None
        self.escape: bool = True
        self.nobody: bool = False
        self.is_text: bool = False

    # Indent a line of HTML source code
    def __indent(self, depth: int) -> str:
        return "    " * depth

    # Set text and mark this element a text element
    def set_text(self, text: str):
        self.is_text = True
        self.text = text
        return self

    # Add children tags to this tag
    def add(self, *tags: Tag|list[Tag|str]|str):
        for tag in tags:
            if type(tag) == str:
                self.tags.append(Text(tag))
            elif type(tag) == list:
                self.add(*tag)
            else:
                self.tags.append(tag)

        return self

    # Set & get attribute
    def set(self, attribute: str, value: str):
        self.attributes[attribute] = value
        return self

    def get(self, attribute: str) -> str|None:
        if attribute in self.attributes:
            return self.attributes[attribute]
        return None

    # Set & get classes
    def set_classes(self, *class_names: str):
        self.classes = list(class_names)
        return self

    def add_class(self, class_name: str):
        if class_name not in self.classes:
            self.classes.append(class_name)
        return self

    def remove_class(self, class_name: str):
        if class_name in self.classes:
            self.classes.remove(class_name)
        return self

    # Set & get id attribute
    def set_id(self, id: str):
        self.set("id", id)
        return self

    def get_id(self) -> str|None:
        return self.get("id")

    # Set & get name attribute
    def set_name(self, name: str):
        self.set("name", name)
        return self

    def get_name(self) -> str|None:
        return self.get("name")

    # Set & get value attribute
    def set_value(self, value: str):
        self.set("value", value)
        return self

    def get_value(self) -> str|None:
        return self.get("value")

    # Set & get style
    def set_style(self, property: str, value: str):
        self.styles[property] = value
        return self

    def get_style(self, property: str) -> str|None:
        if property in self.styles:
            return self.styles[property]
        return None

    # Find a tag
    def find_one(self, func: Callable[[Tag], bool], recurse: bool = True, max_depth: int = None) -> Tag|None:
        if max_depth != None: max_depth -= 1

        for tag in self.tags:
            if type(tag) != Text:
                if func(tag): return tag
                if recurse and (max_depth == None or max_depth > -1): 
                    _tag = tag.find_one(func, recurse=recurse, max_depth=max_depth)
                    if _tag != None: return _tag
        return None

    @staticmethod
    def __find_many(tag: Tag, func: Callable[[Tag], bool], result: list[Tag], recurse: bool = True, max_depth: int = None):
        if max_depth != None: max_depth -= 1
        
        for _tag in tag.tags:
            if type(_tag) != Text:
                if func(_tag): result.append(_tag)
                if recurse and (max_depth == None or max_depth > -1): 
                    Tag.__find_many(_tag, func, result, recurse=recurse, max_depth=max_depth)

    # Find many tags
    def find_many(self, func: Callable[[Tag], bool], recurse: bool = True, max_depth: int = None) -> list[Tag]:
        result = []
        Tag.__find_many(self, func, result, recurse=recurse, max_depth=max_depth)
        return result

    # Escape HTML code if escape option is set
    def __escape(self, input: str, force: bool = False) -> str:
        replaces = (
            ("\"", "\\\""),
            ("<", "&lt;"),
            (">", "&gt;")
        )

        if self.escape or force:
            for old, new in replaces:
                input = input.replace(old, new)

        return input

    # Produce HTML source code
    def html(self, pretty: bool = False, depth: int = 0) -> str:
        result: list[str] = []

        # Add before element
        if self.before != None:
            if pretty and depth > 0:
                result.append("\n" + self.__indent(depth))
            result.append(self.before)

        # Check if this element is a text element
        if self.is_text:
            #if pretty and depth > 0:
            #    result.append("\n" + self.__indent(depth))
            result.append(self.__escape(self.text))
        else:
            # Add opening tag
            if pretty and depth > 0:
                result.append("\n" + self.__indent(depth))
            has_props = len(self.attributes) + len(self.classes) + len(self.styles) > 0
            result.append(f"<{self.name}" + (" " if has_props else ""))

            # Add attributes & styles
            attributes = self.attributes

            if len(self.classes) > 0:
                attributes["class"] = " ".join(self.__escape(x, force=True) for x in self.classes)

            if len(self.styles) > 0:
                styles = []
                for key, value in self.styles.items():
                    styles.append(f"{self.__escape(key, force=True)}: {self.__escape(value, force=True)}")
                attributes["style"] = "; ".join(styles)

            temp = []
            for key, value in self.attributes.items():
                if value == True:
                    temp.append(self.__escape(key))
                else:
                    temp.append(f"{self.__escape(key)}=\"{self.__escape(value, force=True)}\"")
            result.append(" ".join(temp))

            # Add child tags
            has_text = False
            if not self.nobody:
                result.append(">")
                
                new_depth = depth + 1
                for tag in self.tags:
                    if type(tag) == Text: 
                        has_text = True
                    result.append(tag.html(pretty, new_depth))

            # Add closing tag
            if not self.nobody and not has_text and len(self.tags) != 0 and pretty:
                result.append("\n" + self.__indent(depth))
            result.append(" />" if self.nobody else f"</{self.name}>")

        # Add after element
        if self.after != None:
            result.append(self.after)

        return "".join(result)

    def __str__(self):
        return self.html()
    def __repr__(self): 
        return self.__str__()

# Text element
class Text(Tag):
    def __init__(self, text: str):
        super().__init__(None)
        self.is_text = True
        self.text = text

    def __str__(self):
        return self.text
    def __repr__(self):
        return self.__str__()