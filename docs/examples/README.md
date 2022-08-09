#### HTML source code parser
```py
from luxon.html.parser import Parser

def main():
    h1 = Parser.parse("<h1>Hello world!</h1>")
    print(h1)

if __name__ == "__main__":
    main()
```
```py
from luxon.html.parser import Parser
from luxon.html.tags import *

def main():
    html = requests.get("https://nsa.gov/").content.decode("utf-8")
    parsed = Parser.parse(html)
    texts = parsed.find_all(lambda t: type(t) == Text and type(t.parent) not in (Style, Script))
    print([repr(t) for t in texts])

if __name__ == "__main__":
    main()
```
```py
from luxon.html.parser import Parser
from luxon.html.tags import *

def main():
    html = requests.get("https://example.com/").content.decode("utf-8")
    parsed = Parser.parse(html)
    print(parsed.find_by_type(H1).read_text())

if __name__ == "__main__":
    main()
```
```py
from luxon.html.parser import Parser
from luxon.html.tags import *

def main():
    parsed1 = Parser.parse("<header/><main/><footer/>")
    # returns a Root element (because more than 1 top-level tags) 

    parsed2 = Parser.parse("<!-- Hello world! --><ul><li>Banana</li><li>Mango</li><li>Apricot</li></ul>")
    # returns a Root element

    # Find the first Main element and 
    # add Root element's children to it
    parsed1.find_by_type(Main) \
        .add(*parsed2) 
    
    # Find the first Ul element
    # and add new list item to it
    fruits: Ul = parsed1.find_by_type(Ul)
    fruits.add_item("Pear")

    # Sort child elements
    fruits.sort(key=lambda fruit: fruit.read_text())
    #sorted_fruits = sorted(fruits, key=lambda t: t.read_text())

    # Print source code
    print(parsed1.html(pretty=True))

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