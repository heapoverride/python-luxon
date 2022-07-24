# Python Luxon
This repository contains some parts of my Luxon framework (PHP) implemented using Python.

### Code examples
#### HTML source code parser
```py
from luxon.html.parser import Parser

def main():
    item = Parser.parse("<h1>Hello world!</h1>")
    print(item)

    items = Parser.parse("<h1>Hello</h1><h2>world!</h2>")
    print(items)

if __name__ == "__main__":
    main()
```
#### HTML source code generator
```py
from luxon.html.tags import *

def main():
    doc = Html().add(
        Head().add(
            Title("Example site"),
            # Style defined this way shows up as <link> tag in source code
            Style("/assets/styles/base.css")
        ),
        Body().add(
            Header(),
            Main().add(
                Img("/assets/images/catgirl.png"),
                Ul("Apple", "Mango", "Lime", "Banana")
            ),
            Footer()
        )
    )

    print(doc.html(pretty=True))

if __name__ == "__main__":
    main()
```
```py
from luxon.html.tags import *

def main():
    # Yes, you can even do this but
    # it doesn't mean you should...
    ul = Ul() \
        + (Li("Finland") \
            + (Ul() \
                + Li("Helsinki") \
                + Li("Tampere") \
                + Li("Hämeenlinna"))) \
        + (Li("Estonia") \
            + (Ul() \
                + Li("Tallinn") \
                + Li("Tartu") \
                + Li("Narva")))

    print(ul.html(pretty=True))

if __name__ == "__main__":
    main()
```
```py
from luxon.html.tags import *

class Document(Html):
    def __init__(self, title: str):
        super().__init__()

        # head
        self.head = Head()
        self.add(self.head)

        # head > title
        self.head.add(Title(title))

        # head > link
        self.head.add(Style("/assets/styles/base.css"))

        # body
        self.body = Body()
        self.add(self.body)

        # body > header
        self.header = Header()
        self.body.add(self.header)

        # body > nav
        self.nav = Nav().add(
            A("Home", "/").set("data-page", "home"),
            A("About", "/about").set("data-page", "about")
        )
        self.body.add(self.nav)

        # body > main
        self.main = Main()
        self.body.add(self.main)
        
        # body > footer
        self.footer = Footer()
        self.body.add(self.footer)
```
```py
from luxon.html.tags import *

def main():
    ul = Ul().add(
        Li("Finland").add(
            Ul("Helsinki", "Tampere", "Hämeenlinna")),
        Li("Estonia").add(
            Ul("Tallinn", "Tartu", "Narva")))

    print(ul.html(pretty=True))
    
    tags = ul.find_all(
        lambda t: type(t.parent) == Ul 
            and t.parent[0] == t 
            and type(t.parent.parent) == Li)
            
    print(tags)

if __name__ == "__main__":
    main()
```
```py
import random
from luxon.html.tags import *

class Selective(Div):
    """This is a custom element that displays randomly
    chosen content every time it's source code is generated"""
    def __init__(self):
        """Construct a Selective element"""
        super().__init__()

    def update(self):
        self.set_body(
            "I like ", 
            Span(random.choice(["cats", "dogs"]))
        )
```
```py
from luxon.html.tags import *

def main():
    fruits = Ul("Apple", "Apricot", "Banana", "Mango")
    del fruits[1::2]
    print(fruits.html(pretty=True))

if __name__ == "__main__":
    main()
```