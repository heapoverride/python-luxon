from __future__ import annotations
from typing import Any, Callable

class Tag:
    """Base class for all HTML elements\n 
    All other elements inherit from this base class
    """
    def __init__(self, tagname: str):
        """Construct a Tag element
        
        Args:
            tagname (str): Name of the HTML tag
        """
        self.__tagname: str = None
        self.__attributes: dict[str, Any] = {}
        self.__classes: list[str] = []
        self.__styles: dict[str, str] = {}
        self.__tags: list[Tag] = []
        self.__text: Any = None
        self.__before: Any = None
        self.__after: Any = None
        self.__escape: bool = True
        self.__nobody: bool = False
        self.__is_text: bool = False
        self.__hidden: bool = False
        self.__parent: Tag = None

        if type(tagname) == str:
            self.__tagname = tagname.lower()

    @property
    def tagname(self) -> str:
        """Element's tag name

        Returns:
            str: Tag name
        """
        return self.__tagname

    @property
    def before(self) -> Any:
        """Element's before element

        Returns:
            Any: Before element
        """
        return self.__before

    @before.setter
    def before(self, value: Any):
        self.__before = value

    @property
    def after(self) -> Any:
        """Element's after element

        Returns:
            Any: After element
        """
        return self.__after

    @after.setter
    def after(self, value: Any):
        self.__after = value

    @property
    def text(self) -> Any:
        """Element's text content

        Returns:
            Any: Text content
        """
        return self.__text

    @text.setter
    def text(self, value: Any):
        self.__is_text = True
        self.__text = value

    @property
    def is_text(self) -> bool:
        """Set to True if this element is a text element

        Hint:
            You can also compare tag type to Text to get if
            this element is a text element or not.

        Returns:
            bool: True if this element is a text element
        """
        return self.__is_text

    @property
    def escape(self) -> bool:
        """Set to True if element's text content should be escaped

        Returns:
            bool: True if text content should be escaped
        """
        return self.__escape

    @escape.setter
    def escape(self, value: bool):
        self.__escape = value

    @property
    def nobody(self) -> bool:
        """Element doesn't have a body

        Returns:
            bool: True if element doesn't have a body
        """
        return self.__nobody

    @nobody.setter
    def nobody(self, value: bool):
        self.__nobody = value

    @property
    def hidden(self) -> bool:
        """Element is hidden (will not be shown in output)

        Returns:
            bool: True if element is hidden
        """
        return self.__hidden

    @hidden.setter
    def hidden(self, value: bool):
        self.__hidden = value

    @property
    def parent(self) -> Tag|None:
        """Parent element

        Returns:
            Tag|None: Parent element or None if element has no parent
        """
        return self.__parent
        
    @property
    def id(self) -> Any|None:
        """Value of `id` attribute

        Returns:
            Any|None: Value of `id` attribute or None
        """
        return self.get_id()

    @id.setter
    def id(self, value: Any):
        self.set_id(value)

    @property
    def name(self) -> Any|None:
        """Value of `name` attribute

        Returns:
            Any|None: Value of `name` attribute or None
        """
        return self.get_name()

    @name.setter
    def name(self, value: Any):
        self.set_name(value)

    @property
    def value(self) -> Any|None:
        """Value of `value` attribute

        Returns:
            Any|None: Value of `value` attribute or None
        """
        return self.get_value()

    @value.setter
    def value(self, value: Any):
        self.set_value(value)

    @property
    def classes(self) -> list[str]:
        """Get class list

        Returns:
            list[str]: Class list
        """
        return self.get_classes()

    @classes.setter
    def classes(self, value: list[str]):
        self.set_classes(*value)
        
    def set_text(self, text: Any):
        """Set displayed text and mark this element a text element

        Args:
            text (Any): String value or other type that can be converted to string

        Returns:
            self
        """
        self.__is_text = True
        self.__text = text
        return self

    def read_text(self, recurse: bool = True, max_depth: int = None) -> str:
        """Read element's text content

        Args:
            recurse (bool, optional): Use recursion. Defaults to `True`.
            max_depth (int, optional): Max recursion depth. Defaults to `None`.

        Returns:
            str: Text content
        """
        return " ".join([str(t).strip() for t in self.find_all(lambda t: type(t) == Text, recurse, max_depth)]).strip()

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
                tag.__parent = self
                self.__tags.append(tag)

        self.__nobody = False
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
        self.nobody = True
        self.__tags.clear()
        return self

    def sort(self, key: Callable[[Tag], Any], reverse: bool = False):
        """Sort child elements

        Args:
            key (Callable[[Tag], Any]): Sort by key. (supports rich comparison)
            reverse (bool, optional): Reverse sort. Defaults to `False`.
        """
        self.__tags.sort(key=key, reverse=reverse)

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
        self.__classes = [*class_names]
        return self

    def get_classes(self) -> list[str]:
        """Get class list

        Returns:
            list[str]: Class list
        """
        return self.__classes

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

    def set_id(self, id: Any):
        """Set value of `id` attribute

        Args:
            id (Any): New value

        Returns:
            self
        """
        self.set("id", id)
        return self

    def get_id(self) -> Any|None:
        """Get value of `id` attribute

        Returns:
            Any|None
        """
        return self.get("id")

    def set_name(self, name: Any):
        """Set value of `name` attribute

        Args:
            name (Any): New value

        Returns:
            self
        """
        self.set("name", name)
        return self

    def get_name(self) -> Any|None:
        """Get value of `name` attribute

        Returns:
            Any|None
        """
        return self.get("name")

    def set_value(self, value: Any):
        """Set value of `value` attribute

        Args:
            value (str): New value

        Returns:
            self
        """
        self.set("value", value)
        return self

    def get_value(self) -> Any|None:
        """Get value of `value` attribute

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
            if func(tag): return tag
            if recurse and (max_depth == None or max_depth > -1): 
                _tag = tag.find(func, recurse=recurse, max_depth=max_depth)
                if _tag != None: return _tag
        return None

    @staticmethod
    def __find_all(tag: Tag, func: Callable[[Tag], bool], result: list[Tag], recurse: bool = True, max_depth: int = None):
        if max_depth != None: max_depth -= 1
        
        for _tag in tag.__tags:
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
        return self.find(lambda tag: tag.__tagname == tagname, 
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
        return self.find_all(lambda tag: tag.__tagname == tagname, 
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
        return self.find(lambda tag: all(item in tag.__classes for item in class_name), 
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
        return self.find_all(lambda tag: all(item in tag.__classes for item in class_name), 
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
        """Call a named method with this element as the first argument

        Args:
            func (Callable[[Tag], None]): Named method

        Returns:
            self
        """
        func(self)
        return self

    def update(self):
        """Called right before this element's source code is generated.\n 
        Can be overloaded and used to update this element, it's children or parent elements.
        """
        pass
        
    def __html(self, pretty: bool = False, depth: int = 0, extend: bool = True) -> str:
        result: str = ""

        # Return now if element is hidden
        if self.__hidden: return result

        if type(self) == Root:
            # This element is a Root element
            first = True

            for tag in self.__tags:
                if not first:
                    if type(tag) == Text:
                        if tag.text == " ":
                            result += " "
                            continue
                    else:
                        if pretty: result += "\n"

                first = False
                result += tag.__html(pretty)

            return result

        # Call update
        self.update()

        # Add before element
        indented_before = False
        if self.__before != None:
            if pretty and depth > 0:
                result += "\n" + self.__indent(depth)
                indented_before = True
            result += str(self.__before)

        # Check if this element is a text element
        if self.__is_text:
            if self.__text != " ":
                # Add text
                if pretty and depth > 0 and extend and not indented_before:
                    result += "\n" + self.__indent(depth)
                result += self.__escape_str(str(self.__text))
            else:
                # Add whitespace
                result += " "
        else:
            # Add opening tag
            if pretty and depth > 0:
                result += "\n" + self.__indent(depth)
            has_props = len(self.__attributes) + len(self.__classes) + len(self.__styles) > 0
            result += f"<{self.__tagname}" + (" " if has_props else "")

            # Add attributes & styles
            attributes = self.__attributes

            if len(self.__classes) > 0:
                attributes["class"] = " ".join(self.__escape_str(x, force=True) for x in self.__classes)

            if len(self.__styles) > 0:
                styles = []
                for key, value in self.__styles.items():
                    styles.append(f"{self.__escape_str(key, force=True)}: {self.__escape_str(value, force=True)}")
                attributes["style"] = "; ".join(styles)

            temp = []
            for key, value in attributes.items():
                if type(value) == bool and value == True:
                    temp.append(self.__escape_str(key))
                else:
                    temp.append(f"{self.__escape_str(key)}=\"{self.__escape_str(str(value), force=True)}\"")
            result += " ".join(temp)

            # Add child tags
            text_only = True
            if not self.__nobody:
                result += ">"
                
                new_depth = depth+1
                for tag in self.__tags:
                    if type(tag) != Text: 
                        text_only = False
                    result += tag.__html(pretty, depth=new_depth, extend=not text_only)

            # Add closing tag
            if not self.__nobody and not text_only and len(self.__tags) != 0 and pretty:
                result += "\n" + self.__indent(depth)
            result += " />" if self.__nobody else f"</{self.__tagname}>"

        # Add after element
        if self.__after != None:
            result += str(self.__after)

        return result

    def html(self, pretty: bool = False):
        """Generate this element's HTML source code

        Args:
            pretty (bool, optional): Pretty print the source code. Defaults to `False`.

        Returns:
            str: Generated HTML source code
        """
        return self.__html(pretty, depth=0)

    @staticmethod
    def __indent(depth: int) -> str:
        return "    " * depth

    def __escape_str(self, input: str, force: bool = False) -> str:
        replaces = (
            ("\"", "&quot;"),
            ("<", "&lt;"),
            (">", "&gt;")
        )

        if self.__escape or force:
            for old, new in replaces:
                input = input.replace(old, new)

        return input

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

class Root(Tag):
    def __init__(self, *content: str|Tag):
        """Construct a Root element

        Hint:
            Parser returns a Root element when the document root 
            contains multiple elements such as comments, text and other 
            misplaced tags outside <html>
        
        Args:
            *content (str|Tag): Content
        """
        super().__init__(None)
        self.add(*content)

class Text(Tag):
    """Text element"""
    def __init__(self, text: Any):
        """Construct a Text element

        Args:
            text (Any): String value or other type that can be converted to string
        """
        super().__init__(None)
        self.text = text

    def __str__(self):
        return str(self.text)

    def __repr__(self):
        return self.__str__()