from __future__ import annotations
from typing import Any, Callable

class Tag:
    """Base class for all HTML elements\n 
    All other elements inherit from this base class
    """
    def __init__(self, name: str):
        """Construct a Tag element
        
        Args:
            name (str): Tag name
        """
        self.__name: str = name.lower() if type(name) == str else name
        self.__attributes: dict[str, Any] = {}
        self.__classes: list[str] = []
        self.__styles: dict[str, str] = {}
        self.__tags: list[Tag] = []
        self.text: Any = None
        self.before: Any = None
        self.after: Any = None
        self.escape: bool = True
        self.nobody: bool = False
        self.is_text: bool = False
        self.hidden: bool = False
        self.parent: Tag = None

    def set_text(self, text: Any):
        """Set displayed text and mark this element a text element

        Args:
            text (Any): String value or other type that can be converted to string

        Returns:
            self
        """
        self.is_text = True
        self.text = text
        return self

    def add(self, *tags: Tag|list[Tag|str]|str):
        """Add child elements to this element

        Returns:
            self
        """
        for tag in tags:
            if type(tag) == str:
                self.add(Text(tag))
            elif type(tag) == list:
                self.add(*tag)
            else:
                tag.parent = self
                self.__tags.append(tag)
        return self

    def set_body(self, *tags: Tag|list[Tag|str]|str):
        """Set this element's child elements

        Returns:
            self
        """
        self.remove_all()
        self.add(*tags)
        return self

    def remove(self, tag: Tag):
        """Removes a child element from this element

        Args:
            tag (Tag): Child element to remove

        Returns:
            self
        """
        if tag in self.__tags:
            self.__tags.remove(tag)
        return self

    def remove_all(self):
        """Remove all child elements from this element

        Returns:
            self
        """
        self.__tags.clear()
        return self

    def insert(self, index: int, *tags: Tag|list[Tag|str]|str):
        """Insert child elements at specific index

        Args:
            index (int): Insert elements before this index

        Returns:
            self
        """
        for tag in tags[::-1]:
            if type(tag) == str:
                self.__tags.insert(index, Text(tag))
            elif type(tag) == list:
                self.insert(index, *tag)
            else:
                self.__tags.insert(index, tag)
        return self

    def remove_where(self, func: Callable[[Tag], bool]):
        """Remove all child elements where lambda expression or named function returns True

        Args:
            func (Callable[[Tag], bool]): Lambda expression or named function

        Returns:
            self
        """
        i = 0
        while i < len(self.__tags):
            if func(self.__tags[i]):
                del self.__tags[i]
                i -= 1
            i += 1
        return self

    def set(self, attribute: str, value: Any = True):
        """Set attribute with optional value

        Args:
            attribute (str): Attribute name
            value (Any, optional): Attribute value

        Returns:
            self
        """
        self.__attributes[attribute] = value
        return self

    def get(self, attribute: str) -> Any|None:
        """Get attribute value by it's name

        Args:
            attribute (str): Attribute name

        Returns:
            Any|None
        """
        if attribute in self.__attributes:
            return self.__attributes[attribute]
        return None

    def unset(self, *attributes: str):
        """Unset attribute by it's name

        Returns:
            self
        """
        for attribute in attributes:
            if attribute in self.__attributes:
                del self.__attributes[attribute]
        return self

    def set_classes(self, *class_names: str):
        """Set class list

        Returns:
            self
        """
        self.__classes = list(class_names)
        return self

    def add_class(self, class_name: str):
        """Add class to class list

        Args:
            class_name (str): Class name

        Returns:
            self
        """
        if class_name not in self.__classes:
            self.__classes.append(class_name)
        return self

    def unset_class(self, class_name: str):
        """Unset class from class list

        Args:
            class_name (str): Class name

        Returns:
            self
        """
        if class_name in self.__classes:
            self.__classes.remove(class_name)
        return self

    def set_id(self, id: str):
        """Set id attribute's value

        Args:
            id (str): ID

        Returns:
            self
        """
        self.set("id", id)
        return self

    def get_id(self):
        """Get id attribute's value

        Returns:
            Any|None
        """
        return self.get("id")

    def set_name(self, name: str):
        """Set name attribute's value

        Args:
            name (str): Name

        Returns:
            self
        """
        self.set("name", name)
        return self

    def get_name(self):
        """Get name attribute's value

        Returns:
            Any|None
        """
        return self.get("name")

    def set_value(self, value: Any):
        """Set value attribute's value

        Args:
            value (str): Value

        Returns:
            self
        """
        self.set("value", value)
        return self

    def get_value(self):
        """Get value attribute's value

        Returns:
            Any|None
        """
        return self.get("value")

    def set_style(self, property: str, value: str):
        """Set style property

        Args:
            property (str): Property name
            value (str): Property value

        Returns:
            self
        """
        self.__styles[property] = value
        return self

    def get_style(self, property: str) -> str|None:
        """Get style property's value

        Args:
            property (str): Property name

        Returns:
            str|None
        """
        if property in self.__styles:
            return self.__styles[property]
        return None

    def unset_style(self, property: str):
        """Unset stype property

        Args:
            property (str): Property name

        Returns:
            self
        """
        if property in self.__styles:
            del self.__styles[property]
        return self

    def find(self, func: Callable[[Tag], bool], recurse: bool = True, max_depth: int = None) -> Tag|None:
        """Find the first element where lambda expression or named function returns `True`

        Args:
            func (Callable[[Tag], bool]): Lambda expression or named function
            recurse (bool, optional): Use recursion. Defaults to `True`.
            max_depth (int, optional): Max recursion depth. Defaults to `None`.

        Returns:
            Tag|None: Found element or None if no element was found
        """
        if max_depth != None: max_depth -= 1

        for tag in self.__tags:
            if type(tag) != Text:
                if func(tag): return tag
                if recurse and (max_depth == None or max_depth > -1): 
                    _tag = tag.find(func, recurse=recurse, max_depth=max_depth)
                    if _tag != None: return _tag
        return None

    @staticmethod
    def __find_all(tag: Tag, func: Callable[[Tag], bool], result: list[Tag], recurse: bool = True, max_depth: int = None):
        if max_depth != None: max_depth -= 1
        
        for _tag in tag.__tags:
            if type(_tag) != Text:
                if func(_tag): result.append(_tag)
                if recurse and (max_depth == None or max_depth > -1): 
                    Tag.__find_all(_tag, func, result, recurse=recurse, max_depth=max_depth)

    def find_all(self, func: Callable[[Tag], bool], recurse: bool = True, max_depth: int = None) -> list[Tag]:
        """Find all elements where lambda expression or named function returns `True`

        Args:
            func (Callable[[Tag], bool]): Lambda expression or named function
            recurse (bool, optional): Use recursion. Defaults to `True`.
            max_depth (int, optional): Max recursion depth. Defaults to `None`.

        Returns:
            list[Tag]: List of found elements
        """
        result = []
        Tag.__find_all(self, func, result, recurse=recurse, max_depth=max_depth)
        return result

    def find_by_id(self, id: str):
        """Find element by id (attribute) recursively

        Args:
            id (str): ID

        Returns:
            Tag|None: Found element or None if no element was found
        """
        return self.find(lambda tag: tag.get_id() == id)

    def find_by_name(self, name: str, recurse: bool = True, max_depth: int = None):
        """Find element by name (attribute) recursively

        Args:
            name (str): Name
            recurse (bool, optional): Use recursion. Defaults to `True`.
            max_depth (int, optional): Max recursion depth. Defaults to `None`.

        Returns:
            Tag|None: Found element or None if no element was found
        """
        return self.find(lambda tag: tag.get_name() == name, 
            recurse=recurse, 
            max_depth=max_depth)

    def find_all_by_name(self, name: str, recurse: bool = True, max_depth: int = None):
        """Find all elements by name (attribute) recursively

        Args:
            name (str): Name
            recurse (bool, optional): Use recursion. Defaults to `True`.
            max_depth (int, optional): Max recursion depth. Defaults to `None`.

        Returns:
            list[Tag]: List of found elements
        """
        return self.find_all(lambda tag: tag.get_name() == name, 
            recurse=recurse, 
            max_depth=max_depth)

    def find_by_tagname(self, tagname: str, recurse: bool = True, max_depth: int = None):
        """Find element by tag name recursively

        Args:
            tagname (str): Tag name
            recurse (bool, optional): Use recursion. Defaults to `True`.
            max_depth (int, optional): Max recursion depth. Defaults to `None`.

        Returns:
            Tag|None: Found element or None if no element was found
        """
        return self.find(lambda tag: tag.name == tagname, 
            recurse=recurse, 
            max_depth=max_depth)

    def find_all_by_tagname(self, tagname: str, recurse: bool = True, max_depth: int = None):
        """Find all elements by tag name recursively

        Args:
            tagname (str): Name
            recurse (bool, optional): Use recursion. Defaults to `True`.
            max_depth (int, optional): Max recursion depth. Defaults to `None`.

        Returns:
            list[Tag]: List of found elements
        """
        return self.find_all(lambda tag: tag.name == tagname, 
            recurse=recurse, 
            max_depth=max_depth)

    def find_by_type(self, tag_type: type, recurse: bool = True, max_depth: int = None):
        """Find element by type recursively

        Args:
            tag_type (type): Tag type (e.g. Div)
            recurse (bool, optional): Use recursion. Defaults to `True`.
            max_depth (int, optional): Max recursion depth. Defaults to `None`.

        Returns:
            Tag|None: Found element or None if no element was found
        """
        return self.find(lambda tag: type(tag) == tag_type, 
            recurse=recurse, 
            max_depth=max_depth)

    def find_all_by_type(self, tag_type: type, recurse: bool = True, max_depth: int = None):
        """Find all elements by type recursively

        Args:
            tag_type (type): Tag type (e.g. Div)
            recurse (bool, optional): Use recursion. Defaults to `True`.
            max_depth (int, optional): Max recursion depth. Defaults to `None`.

        Returns:
            list[Tag]: List of found elements
        """
        return self.find_all(lambda tag: type(tag) == tag_type, 
            recurse=recurse, 
            max_depth=max_depth)

    def find_by_class(self, *class_name: str, recurse: bool = True, max_depth: int = None):
        """Find element by one or more class names recursively

        Args:
            *class_name (str): Class name(s)
            recurse (bool, optional): Use recursion. Defaults to `True`.
            max_depth (int, optional): Max recursion depth. Defaults to `None`.

        Returns:
            Tag|None: Found element or None if no element was found
        """
        return self.find(lambda tag: all(item in tag.classes for item in class_name), 
            recurse=recurse, 
            max_depth=max_depth)

    def find_all_by_class(self, *class_name: str, recurse: bool = True, max_depth: int = None):
        """Find elements by one or more class names recursively

        Args:
            *class_name (str): Class name(s)
            recurse (bool, optional): Use recursion. Defaults to `True`.
            max_depth (int, optional): Max recursion depth. Defaults to `None`.

        Returns:
            list[Tag]: List of found elements
        """
        return self.find_all(lambda tag: all(item in tag.classes for item in class_name), 
            recurse=recurse, 
            max_depth=max_depth)

    def find_by_attribute(self, attribute: str, value: Any = True, recurse: bool = True, max_depth: int = None):
        """Find element by attribute (and optionally it's value)

        Args:
            attribute (str): Attribute name
            value (str, optional): Attribute value
            recurse (bool, optional): Use recursion. Defaults to `True`.
            max_depth (int, optional): Max recursion depth. Defaults to `None`.

        Returns:
            Tag|None: Found element or None if no element was found
        """
        return self.find(lambda tag: tag.get(attribute) == value if value != True else tag.get(attribute) != None, 
            recurse=recurse, 
            max_depth=max_depth)

    def find_all_by_attribute(self, attribute: str, value: Any = True, recurse: bool = True, max_depth: int = None):
        """Find elements by attribute (and optionally it's value)

        Args:
            attribute (str): Attribute name
            value (str, optional): Attribute value
            recurse (bool, optional): Use recursion. Defaults to `True`.
            max_depth (int, optional): Max recursion depth. Defaults to `None`.

        Returns:
            list[Tag]: List of found elements
        """
        return self.find_all(lambda tag: tag.get(attribute) == value if value != True else tag.get(attribute) != None, 
            recurse=recurse, 
            max_depth=max_depth)

    def call(self, func: Callable[[Tag], None]):
        """Call a lambda expression or named method with this element as the first argument

        Args:
            func (Callable[[Tag], None]): Lambda expression or named method

        Returns:
            self
        """
        func(self)
        return self
        
    def __html(self, pretty: bool = False, depth: int = 0, extend: bool = True) -> str:
        result: str = ""

        # Return now if element is hidden
        if self.hidden: return result

        # Call update
        self.update()

        # Add before element
        if self.before != None:
            if pretty and depth > 0:
                result += "\n" + self.__indent(depth)
            result += str(self.before)

        # Check if this element is a text element
        if self.is_text:
            if pretty and depth > 0 and extend:
                result += "\n" + self.__indent(depth)
            result += self.__escape(str(self.text))
        else:
            # Add opening tag
            if pretty and depth > 0:
                result += "\n" + self.__indent(depth)
            has_props = len(self.__attributes) + len(self.__classes) + len(self.__styles) > 0
            result += f"<{self.__name}" + (" " if has_props else "")

            # Add attributes & styles
            attributes = self.__attributes

            if len(self.__classes) > 0:
                attributes["class"] = " ".join(self.__escape(x, force=True) for x in self.__classes)

            if len(self.__styles) > 0:
                styles = []
                for key, value in self.__styles.items():
                    styles.append(f"{self.__escape(key, force=True)}: {self.__escape(value, force=True)}")
                attributes["style"] = "; ".join(styles)

            temp = []
            for key, value in self.__attributes.items():
                if value == True:
                    temp.append(self.__escape(key))
                else:
                    temp.append(f"{self.__escape(key)}=\"{self.__escape(str(value), force=True)}\"")
            result += " ".join(temp)

            # Add child tags
            text_only = True
            if not self.nobody:
                result += ">"
                
                new_depth = depth + 1
                for tag in self.__tags:
                    if type(tag) != Text: 
                        text_only = False
                    result += tag.__html(pretty, depth=new_depth, extend=not text_only)

            # Add closing tag
            if not self.nobody and not text_only and len(self.__tags) != 0 and pretty:
                result += "\n" + self.__indent(depth)
            result += " />" if self.nobody else f"</{self.__name}>"

        # Add after element
        if self.after != None:
            result += str(self.after)

        return result

    def html(self, pretty: bool = False):
        """Generate this element's HTML source code

        Args:
            pretty (bool, optional): Pretty print the source code. Defaults to False.

        Returns:
            str: Generated HTML source code
        """
        return self.__html(pretty, depth=0)

    def __indent(self, depth: int) -> str:
        return "    " * depth

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

    # This method is called before HTML 
    # source code is generated and can be overloaded
    def update(self):
        pass

    # Overload slice/array access operator
    def __getitem__(self, slice: slice) -> Tag|list[Tag]:
        return self.__tags[slice]

    def __setitem__(self, slice: slice, tag: Tag):
        self.__tags[slice] = tag

    def __delitem__(self, slice: slice):  
        del self.__tags[slice]

    # Use len() to get the length of child tags
    def __len__(self):
        return len(self.__tags)

    # Overload binary operators
    def __add__(self, tag: Tag|list[Tag|str]|str):
        self.add(tag)
        return self

    # Generate this tag's HTML source code (minified)
    # when this tag is printed or converted to string using str()
    def __str__(self):
        return self.html()

    def __repr__(self): 
        return self.__str__()

class Text(Tag):
    """Text element"""
    def __init__(self, text: Any):
        """Construct a Text element

        Args:
            text (Any): String value or other type that can be converted to string
        """
        super().__init__(None)
        self.set_text(text)

    def __str__(self):
        return str(self.text)

    def __repr__(self):
        return self.__str__()